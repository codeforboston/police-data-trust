from backend.database.models.attachment import Attachment
from backend.database.models.civilian import Civilian
from backend.database.models.complaint import (
    Allegation,
    Complaint,
    Investigation,
    Location,
    Penalty,
)
from backend.database.models.officer import Officer
from backend.database.models.source import Source
from backend.database.models.user import User
from backend.dto.complaint import (
    CreateAllegation,
    CreateCivilian,
    CreateInvestigation,
    CreatePenalty,
)
from backend.utils.citations import make_citation_diff


class ComplaintService:
    def _get_complaint_or_raise(self, complaint_uid: str) -> Complaint:
        complaint = Complaint.nodes.get_or_none(uid=complaint_uid)
        if complaint is None:
            raise LookupError("Complaint not found")
        return complaint

    def _get_allegation_or_raise(
        self,
        complaint: Complaint,
        allegation_uid: str,
    ) -> Allegation:
        allegation = Allegation.nodes.get_or_none(uid=allegation_uid)
        if allegation is None:
            raise LookupError("Allegation not found")
        if not complaint.allegations.filter(
            "a.uid = $allegation_uid",
            allegation_uid=allegation_uid,
        ).exists():
            raise LookupError("Allegation not found for this complaint")
        return allegation

    def _get_investigation_or_raise(
        self,
        complaint: Complaint,
        investigation_uid: str,
    ) -> Investigation:
        investigation = Investigation.nodes.get_or_none(uid=investigation_uid)
        if investigation is None:
            raise LookupError("Investigation not found")
        if not complaint.investigations.filter(
            "i.uid = $investigation_uid",
            investigation_uid=investigation_uid,
        ).exists():
            raise LookupError("Investigation not found for this complaint")
        return investigation

    def _get_penalty_or_raise(
        self,
        complaint: Complaint,
        penalty_uid: str,
    ) -> Penalty:
        penalty = Penalty.nodes.get_or_none(uid=penalty_uid)
        if penalty is None:
            raise LookupError("Penalty not found")
        if not complaint.penalties.filter(
            "p.uid = $penalty_uid",
            penalty_uid=penalty_uid,
        ).exists():
            raise LookupError("Penalty not found for this complaint")
        return penalty

    def _get_source_with_publish_access(
        self,
        source_uid: str | None,
        current_user: User,
        action: str,
    ) -> Source:
        if not source_uid:
            raise ValueError("source_uid is required")

        source = Source.nodes.get_or_none(uid=source_uid)
        if source is None:
            raise ValueError("Invalid Complaint: Source not found")
        if not source.members.is_connected(current_user):
            raise PermissionError(
                f"User does not have permission to {action} this complaint for the provided source."
            )

        membership = source.members.relationship(current_user)
        if not membership.may_publish():
            raise PermissionError(
                f"User does not have permission to {action} this complaint for the provided source."
            )
        return source

    def _create_location(self, location_data: dict | None) -> Location:
        if not location_data:
            raise ValueError("Invalid Complaint: Location is required")
        return Location.from_dict(location_data)

    def _upsert_location(
        self,
        complaint: Complaint,
        location_data: dict | None,
    ) -> tuple[dict | None, dict | None]:
        if location_data is None:
            return None, None

        current_location = complaint.location.single()
        if current_location:
            old_values = {
                key: getattr(current_location, key, None)
                for key in location_data.keys()
            }
            current_location = Location.from_dict(
                location_data,
                current_location.uid,
            )
            if not complaint.location.is_connected(current_location):
                complaint.location.connect(current_location)
            new_values = {
                key: getattr(current_location, key, None)
                for key in location_data.keys()
            }
            return old_values, new_values

        new_location = Location.from_dict(location_data)
        complaint.location.connect(new_location)
        new_values = {
            key: getattr(new_location, key, None)
            for key in location_data.keys()
        }
        return {}, new_values

    def _create_allegation(
        self,
        complaint: Complaint,
        allegation_input: CreateAllegation,
        civilian: Civilian | None = None,
    ) -> Allegation:
        a_data = allegation_input.model_dump(exclude_unset=True)
        officer_uid = a_data.pop("accused_uid", None)
        complainant_data = a_data.pop("complainant", None)

        if not officer_uid:
            raise ValueError("Officer UID is required for the allegation")

        officer = Officer.nodes.get_or_none(uid=officer_uid)
        if officer is None:
            raise ValueError(f"Officer with UID {officer_uid} not found")

        allegation = None
        try:
            allegation = Allegation(**a_data).save()
            allegation.accused.connect(officer)
            allegation.complaint.connect(complaint)
        except Exception as e:
            if allegation:
                allegation.delete()
            raise AttributeError(f"Failed to create allegation: {e}")

        try:
            if civilian:
                allegation.complainant.connect(civilian)
            elif complainant_data:
                civ_id = complainant_data.get("civ_id")
                if not civ_id:
                    raise ValueError(
                        "civ_id must be provided in complainant_data"
                    )
                new_civilian = Civilian(**complainant_data).save()
                allegation.complainant.connect(new_civilian)
        except Exception:
            if not civilian and "new_civilian" in locals():
                new_civilian.delete()
            raise

        return allegation

    def _update_allegation(
        self,
        allegation: Allegation,
        allegation_input: CreateAllegation,
    ) -> Allegation:
        a_data = allegation_input.model_dump(exclude_unset=True)
        officer_uid = a_data.pop("accused_uid", None)
        complainant_data = a_data.pop("complainant", None)

        if officer_uid:
            officer = Officer.nodes.get_or_none(uid=officer_uid)
            if officer is None:
                raise ValueError(f"Officer with UID {officer_uid} not found")
            allegation.accused.replace(officer)

        if complainant_data:
            complainant = allegation.complainant.single()
            if complainant:
                for key, value in complainant_data.items():
                    setattr(complainant, key, value)
                complainant.save()
            else:
                complainant = Civilian(**complainant_data).save()
                allegation.complainant.connect(complainant)

        try:
            allegation = Allegation.from_dict(a_data, allegation.uid)
        except Exception as e:
            raise AttributeError(f"Failed to update allegation: {e}")
        return allegation

    def _create_penalty(
        self,
        complaint: Complaint,
        penalty_input: CreatePenalty,
    ) -> Penalty:
        p_data = penalty_input.model_dump(exclude_unset=True)
        officer_uid = p_data.pop("officer_uid", None)
        if not officer_uid:
            raise ValueError("Officer UID is required for the penalty")

        officer = Officer.nodes.get_or_none(uid=officer_uid)
        if officer is None:
            raise ValueError(f"Officer with UID {officer_uid} not found")

        penalty = None
        try:
            penalty = Penalty(**p_data).save()
            penalty.complaint.connect(complaint)
            penalty.officer.connect(officer)
        except Exception as e:
            if penalty:
                penalty.delete()
            raise AttributeError(f"Failed to create penalty: {e}")
        return penalty

    def _update_penalty(
        self,
        penalty: Penalty,
        penalty_input: CreatePenalty,
    ) -> Penalty:
        p_data = penalty_input.model_dump(exclude_unset=True)
        officer_uid = p_data.pop("officer_uid", None)

        if officer_uid:
            officer = Officer.nodes.get_or_none(uid=officer_uid)
            if officer is None:
                raise ValueError(f"Officer with UID {officer_uid} not found")
            current_officer = penalty.officer.single()
            if current_officer:
                penalty.officer.reconnect(current_officer, officer)
            else:
                penalty.officer.connect(officer)

        try:
            penalty = Penalty.from_dict(p_data, penalty.uid)
        except Exception as e:
            raise AttributeError(f"Failed to update penalty: {e}")
        return penalty

    def _create_investigation(
        self,
        complaint: Complaint,
        investigation_input: CreateInvestigation,
    ) -> Investigation:
        i_data = investigation_input.model_dump(exclude_unset=True)
        investigator_uid = i_data.pop("investigator_uid", None)
        try:
            investigation = Investigation(**i_data).save()
            investigation.complaint.connect(complaint)
        except Exception as e:
            raise AttributeError(f"Failed to create investigation: {e}")

        if investigator_uid:
            investigator = Officer.nodes.get_or_none(uid=investigator_uid)
            if investigator:
                investigation.investigator.connect(investigator)
        return investigation

    def _update_investigation(
        self,
        investigation: Investigation,
        investigation_input: CreateInvestigation,
    ) -> Investigation:
        i_data = investigation_input.model_dump(exclude_unset=True)
        investigator_uid = i_data.pop("investigator_uid", None)

        if investigator_uid:
            investigator = Officer.nodes.get_or_none(uid=investigator_uid)
            if investigator is None:
                raise ValueError(
                    f"Officer with UID {investigator_uid} not found"
                )
            investigation.investigator.replace(investigator)

        try:
            investigation = Investigation.from_dict(i_data, investigation.uid)
        except Exception as e:
            raise AttributeError(f"Failed to update investigation: {e}")
        return investigation

    def _create_nested_records(
        self,
        complaint: Complaint,
        attachments: list,
        allegations: list,
        investigations: list,
        penalties: list,
        civilian_witnesses: list,
        police_witnesses: list,
    ) -> None:
        if attachments:
            for attachment in attachments:
                a = Attachment.from_dict(attachment)
                complaint.attachments.connect(a)

        if allegations:
            civ_map = {}
            for allegation in allegations:
                complainant_data = allegation.get("complainant")
                civilian_node = None

                if complainant_data:
                    ext_civ_id = complainant_data.get("civ_id")
                    if ext_civ_id in civ_map:
                        civilian_node = civ_map[ext_civ_id]
                    else:
                        civ_count = len(civ_map) + 1
                        internal_civ_id = f"{complaint.uid}-{civ_count}"
                        complainant_data["civ_id"] = internal_civ_id
                        civilian_node = Civilian(**complainant_data).save()
                        if ext_civ_id:
                            civ_map[ext_civ_id] = civilian_node

                self._create_allegation(
                    complaint,
                    CreateAllegation(**allegation),
                    civilian_node,
                )

        if penalties:
            for penalty in penalties:
                self._create_penalty(complaint, CreatePenalty(**penalty))

        if investigations:
            for investigation in investigations:
                self._create_investigation(
                    complaint,
                    CreateInvestigation(**investigation),
                )

        if civilian_witnesses:
            for civilian in civilian_witnesses:
                complaint.civilian_witnesses.connect(
                    Civilian(**civilian).save()
                )

        if police_witnesses:
            for officer_uid in police_witnesses:
                officer = Officer.nodes.get_or_none(uid=officer_uid)
                if officer is None:
                    raise LookupError(f"Officer {officer_uid} not found")
                complaint.police_witnesses.connect(officer)

    def create_complaint(
        self,
        payload: dict,
        current_user: User,
    ) -> dict:
        source_details = payload.pop("source_details", None)
        location_data = payload.pop("location", None)
        attachments = payload.pop("attachments", [])
        allegations = payload.pop("allegations", [])
        investigations = payload.pop("investigations", [])
        penalties = payload.pop("penalties", [])
        civilian_witnesses = payload.pop("civilian_witnesses", [])
        police_witnesses = payload.pop("police_witnesses", [])
        source_uid = payload.pop("source_uid", None)

        source = self._get_source_with_publish_access(source_uid, current_user, "create")
        if source_details is None:
            raise ValueError("Invalid Complaint: Source details are required")

        location = self._create_location(location_data)
        complaint = Complaint.from_dict(payload)
        complaint.location.connect(location)
        complaint.source_org.connect(source, source_details)

        self._create_nested_records(
            complaint,
            attachments,
            allegations,
            investigations,
            penalties,
            civilian_witnesses,
            police_witnesses,
        )

        diff = make_citation_diff(
            {},
            {
                "complaint": {
                    key: getattr(complaint, key, None)
                    for key in payload.keys()
                    if getattr(complaint, key, None) is not None
                },
                "location": {
                    key: value
                    for key, value in (location_data or {}).items()
                    if value is not None
                },
            },
        )
        if diff:
            complaint.add_citation(source, current_user, diff)
        return complaint.to_dict()

    def update_complaint(
        self,
        complaint_uid: str,
        payload: dict,
        current_user: User,
    ) -> dict:
        source_uid = payload.pop("source_uid", None)
        source = self._get_source_with_publish_access(source_uid, current_user, "update")

        complaint = Complaint.nodes.get_or_none(uid=complaint_uid)
        if complaint is None:
            raise LookupError("Complaint not found")

        location_data = payload.pop("location", None)
        old_values = {
            key: getattr(complaint, key, None)
            for key in payload.keys()
        }

        complaint = Complaint.from_dict(payload, complaint_uid)
        complaint.refresh()

        complaint_diff = make_citation_diff(
            old_values,
            {
                key: getattr(complaint, key, None)
                for key in payload.keys()
            },
        )
        old_location_values, new_location_values = self._upsert_location(
            complaint,
            location_data,
        )

        diff = make_citation_diff(
            {
                "complaint": old_values,
                "location": old_location_values,
            },
            {
                "complaint": {
                    key: getattr(complaint, key, None)
                    for key in payload.keys()
                },
                "location": new_location_values,
            },
        )
        if diff:
            complaint.add_citation(source, current_user, diff)

        return complaint.to_dict()

    def create_allegation_record(
        self,
        complaint_uid: str,
        allegation_input: CreateAllegation,
    ) -> Allegation:
        complaint = self._get_complaint_or_raise(complaint_uid)
        civilian = None
        complainant_data = allegation_input.complainant

        if complainant_data:
            civ_id = complainant_data.civ_id
            if civ_id:
                civilian = Civilian.nodes.get_or_none(civ_id=civ_id)
                if civilian is None:
                    raise LookupError(
                        f"Civilian with civ_id {civ_id} not found"
                    )
            else:
                civ_count = len(complaint.complainants.all())
                complainant_data = complainant_data.model_copy(update={
                    "civ_id": f"{complaint.uid}-{civ_count + 1}"
                })
                allegation_input = allegation_input.model_copy(update={
                    "complainant": complainant_data
                })

        return self._create_allegation(complaint, allegation_input, civilian)

    def update_allegation_record(
        self,
        complaint_uid: str,
        allegation_uid: str,
        allegation_input: CreateAllegation,
    ) -> Allegation:
        complaint = self._get_complaint_or_raise(complaint_uid)
        allegation = self._get_allegation_or_raise(complaint, allegation_uid)
        allegation = self._update_allegation(allegation, allegation_input)
        allegation.refresh()
        return allegation

    def create_investigation_record(
        self,
        complaint_uid: str,
        investigation_input: CreateInvestigation,
    ) -> Investigation:
        complaint = self._get_complaint_or_raise(complaint_uid)
        return self._create_investigation(complaint, investigation_input)

    def update_investigation_record(
        self,
        complaint_uid: str,
        investigation_uid: str,
        investigation_input: CreateInvestigation,
    ) -> Investigation:
        complaint = self._get_complaint_or_raise(complaint_uid)
        investigation = self._get_investigation_or_raise(
            complaint,
            investigation_uid,
        )
        investigation = self._update_investigation(
            investigation,
            investigation_input,
        )
        investigation.refresh()
        return investigation

    def create_penalty_record(
        self,
        complaint_uid: str,
        penalty_input: CreatePenalty,
    ) -> Penalty:
        complaint = self._get_complaint_or_raise(complaint_uid)
        return self._create_penalty(complaint, penalty_input)

    def get_allegation_record(
        self,
        complaint_uid: str,
        allegation_uid: str,
    ) -> Allegation:
        complaint = self._get_complaint_or_raise(complaint_uid)
        return self._get_allegation_or_raise(complaint, allegation_uid)

    def get_investigation_record(
        self,
        complaint_uid: str,
        investigation_uid: str,
    ) -> Investigation:
        complaint = self._get_complaint_or_raise(complaint_uid)
        return self._get_investigation_or_raise(complaint, investigation_uid)

    def get_penalty_record(
        self,
        complaint_uid: str,
        penalty_uid: str,
    ) -> Penalty:
        complaint = self._get_complaint_or_raise(complaint_uid)
        return self._get_penalty_or_raise(complaint, penalty_uid)

    def update_penalty_record(
        self,
        complaint_uid: str,
        penalty_uid: str,
        penalty_input: CreatePenalty,
    ) -> Penalty:
        complaint = self._get_complaint_or_raise(complaint_uid)
        penalty = self._get_penalty_or_raise(complaint, penalty_uid)
        penalty = self._update_penalty(penalty, penalty_input)
        penalty.refresh()
        return penalty
