from backend.auth.jwt import min_role_required
from backend.mixpanel.mix import track_to_mp
from backend.database.models.user import User, UserRole
from flask import Blueprint, abort, current_app, request,jsonify
from flask_jwt_extended import get_jwt
from flask_jwt_extended.view_decorators import jwt_required
from ..database import Partner, PartnerMember, MemberRole, db, Invitation, StagedInvitation
from ..dto import InviteUserDTO
from flask_mail import Message
from ..config import TestingConfig






from ..schemas import (
    CreatePartnerSchema,
    AddMemberSchema,
    partner_orm_to_json,
    partner_member_orm_to_json,
    partner_member_to_orm,
    partner_to_orm,
    validate,
)

bp = Blueprint("partner_routes", __name__, url_prefix="/api/v1/partners")


@bp.route("/<int:partner_id>", methods=["GET"])
@jwt_required()
@min_role_required(UserRole.PUBLIC)
@validate()
def get_partners(partner_id: int):
    """Get a single partner by ID."""

    return partner_orm_to_json(Partner.get(partner_id))


@bp.route("/create", methods=["POST"])
@jwt_required()
@min_role_required(UserRole.PUBLIC)
@validate(json=CreatePartnerSchema)
def create():
    """Create a contributing partner.

    Cannot be called in production environments
    """
    if current_app.env == "production":
        abort(418)

    try:
        partner = partner_to_orm(request.context.json)
    except Exception:
        abort(400)

    created = partner.create()
    make_admin = PartnerMember(
        partner_id=created.id,
        user_id=get_jwt()["sub"],
        role=MemberRole.ADMIN,
    )
    make_admin.create()

    track_to_mp(request, "create_partner", {
        "partner_name": partner.name,
        "partner_contact": partner.contact_email
    })
    return partner_orm_to_json(created)

    
   






@bp.route("/", methods=["GET"])
@jwt_required()
@min_role_required(UserRole.PUBLIC)
@validate()
def get_all_partners():
    """Get all partners.
    Accepts Query Parameters for pagination:
    per_page: number of results per page
    page: page number
    """
    args = request.args
    q_page = args.get("page", 1, type=int)
    q_per_page = args.get("per_page", 20, type=int)

    all_partners = db.session.query(Partner)
    results = all_partners.paginate(
        page=q_page, per_page=q_per_page, max_per_page=100
    )

    return {
        "results": [partner_orm_to_json(partner) for partner in results.items],
        "page": results.page,
        "totalPages": results.pages,
        "totalResults": results.total,
    }


@bp.route("/<int:partner_id>/members/", methods=["GET"])
@jwt_required()
@min_role_required(UserRole.PUBLIC)
@validate()
def get_partner_members(partner_id: int):
    """Get all members of a partner.
    Accepts Query Parameters for pagination:
    per_page: number of results per page
    page: page number
    """
    args = request.args
    q_page = args.get("page", 1, type=int)
    q_per_page = args.get("per_page", 20, type=int)

    # partner = Partner.get(partner_id)
    all_members = db.session.query(PartnerMember).filter(
        PartnerMember.partner_id == partner_id
    )
    results = all_members.paginate(
        page=q_page, per_page=q_per_page, max_per_page=100)

    return {
        "results": [
            partner_member_orm_to_json(member)
            for member in results.items
        ],
        "page": results.page,
        "totalPages": results.pages,
        "totalResults": results.total,
    }


""" This class currently doesn't work with the `partner_member_to_orm`
    class AddMemberSchema(BaseModel):
    user_email: str
    role: Optional[MemberRole] = PartnerMember.get_default_role()
    is_active: Optional[bool] = True

    class Config:
        extra = "forbid"
        schema_extra = {
            "example": {
                "user_email": "member@partner.org",
                "role": "ADMIN",
            }
        } """


@bp.route("/<int:partner_id>/members/add", methods=["POST"])
@jwt_required()
@min_role_required(UserRole.PUBLIC)
@validate(json=AddMemberSchema)
def add_member_to_partner(partner_id: int):
    """Add a member to a partner.

    TODO: Allow the API to accept a user email instad of a user id
    TODO: Use the partner ID from the API path instead of the request body
    The `partner_member_to_orm` function seems very picky about the input.
    I wasn't able to get it to accept a dict or a PartnerMember object.

    Cannot be called in production environments
    """
    if current_app.env == "production":
        abort(418)

    # Ensure that the user has premission to add a member to this partner.
    jwt_decoded = get_jwt()

    current_user = User.get(jwt_decoded["sub"])
    association = db.session.query(PartnerMember).filter(
        PartnerMember.user_id == current_user.id,
        PartnerMember.partner_id == partner_id,
    ).first()

    if (
        association is None
        or not association.is_administrator()
        or not association.partner_id == partner_id
    ):
        abort(403)

    # TODO: Allow the API to accept a user email instad of a user id
    # user_obj = User.get_by_email(request.context.json.user_email)
    # if user_obj is None:
    #     abort(400)

    # new_member = PartnerMember(
    #     partner_id=partner_id,
    #     user_id=user_obj.id,
    #     role=request.context.json.role,
    # )

    try:
        partner_member = partner_member_to_orm(request.context.json)
    except Exception:
        abort(400)

    created = partner_member.create()

    track_to_mp(request, "add_partner_member", {
        "partner_id": partner_id,
        "user_id": partner_member.user_id,
        "role": partner_member.role,
    })
    return partner_member_orm_to_json(created)






@bp.route("/invite",methods=["POST"])
@jwt_required()
@min_role_required(UserRole.PUBLIC)
@validate(auth=True,json=InviteUserDTO)
def invite_user():
    

    #TODO : Only Admins of an organization can invite
    """
    Testing scenarios

    1) Should not work for user that is not an Admin
    2) Should work for someone who is an Admin of an organization


    3) (TESTED) If a user already exists and is invited to an organization, message should be appropriate 
    4) (TESTED) If a user does not exist and is not invited to an organization, message should be appropriate 

    5)Make sure all db changes Invitations, and Staged Invitations are happening as expected



    """


    
    
    body: InviteUserDTO = request.context.json
    mail = current_app.extensions.get('mail')

        

    user = User.query.filter_by(email=body.email).first()
    
    # if user is already registered with NPDC, add them to Invitations Table, and send out an email notification
    if user is not None:
        

        try:        
            new_invitation= Invitation(partner_id=body.partner_id, user_id=user.id,role=body.role)
            db.session.add(new_invitation)
            db.session.commit()
            
            msg = Message("Invitation to join NPDC partner organization!", sender=TestingConfig.MAIL_USERNAME, recipients=['paul@mailtrap.io'])
            msg.body = "You are a registered user of NPDC and were invited to a partner organization. Please log on to accept or decline the invitation."
            mail.send(msg)
            return {
            "status": "ok",
            "message": "User notified of their invitation through email!"
        }, 200
            
        except:
            return {
                "status":"error",
                "message":"Something went wrong! Please try again!"
            },500

             
        # new_invitation= Invitation(partner_id=body.partner_id, user_id=user.id,role=body.role)
        # # new_invitation.create()
        # db.session.add(new_invitation)
        # db.session.commit()
        
        # msg = Message("Invitation to join NPDC partner organization!", sender=TestingConfig.MAIL_USERNAME, recipients=['paul@mailtrap.io'])
        # msg.body = "You are a registered user of NPDC and were invited to a partner organization. Please log on to accept or decline the invitation."
        # mail.send(msg)
        # return {
        # "status": "ok",
        # "message": "User notified of their invitation through email!"
        # }, 200
        
    

       
    #if user not registered with NPDC, add the invitation for them in StagedInvitations Table, and send out an email notification
    else:
        try:

            new_staged_invite = StagedInvitation(partner_id=body.partner_id,email=body.email,role=body.role)
            db.session.add(new_staged_invite)
            db.session.commit()
            msg = Message("Invitation to join NPDC index!",sender=TestingConfig.MAIL_USERNAME ,
                        recipients=['paul@mailtrap.io'])
            msg.body = ("You are not a registered user of NPDC and were invited to a partner organization. Please register with NPDC index.")
            mail.send(msg)

            return {
                "status": "ok",
                "message": "User is not registered with the NPDC index. Email sent to user notifying them to register."
            }, 200
        
        except:
            return {
                "status":"error",
                "message":"Something went wrong! Please try again!"
            },500

        

        # new_staged_invite = StagedInvitation(partner_id=body.partner_id,email=body.email,role=body.role)
        
        # db.session.add(new_staged_invite)
        # db.session.commit()
        # msg = Message("Invitation to join NPDC index!",sender=TestingConfig.MAIL_USERNAME ,
        #             recipients=['paul@mailtrap.io'])
        # msg.body = ("You are not a registered user of NPDC and were invited to a partner organization. Please register with NPDC index.")
        # mail.send(msg)

        # return {
        #     "status": "ok",
        #     "message": "User is not registered with the NPDC index. Email sent to user notifying them to register."
        # }, 200
        
       


@bp.route("/invitations",methods=["GET"])
@jwt_required()
@validate()
#only defined for testing environment
def get_invitations():
    if current_app.env == "production":
        abort(418)
    invitation_found = Invitation.query.filter_by(email="harsharauniyar1@gmail.com",partner_id=10)

    if invitation_found is not None:
        return "Found in DB"
    elif invitation_found is None:
        return "Did not find in DB"


@bp.route("/stagedinvitations",methods=["GET"])
@jwt_required()
@validate()
#only defined for testing environment
def stagedinvitations():
    if current_app.env == "production":
        abort(418)
    staged_invitations = StagedInvitation.query.all()

   
    invitations_data = [
        {
            'id': staged_invitation.id,
            'email': staged_invitation.email,
            'role': staged_invitation.role, 
            'partner_id':staged_invitation.partner_id,
        }
        for staged_invitation in staged_invitations
    ]

    return jsonify({'staged_invitations': invitations_data})



