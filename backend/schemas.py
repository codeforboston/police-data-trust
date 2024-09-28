from __future__ import annotations
from functools import wraps
from flask import request, jsonify
from pydantic import BaseModel, ValidationError

import textwrap
from spectree import SecurityScheme, SpecTree
from spectree.models import Server


spec = SpecTree(
    "flask",
    title="National Police Data Collaborative Index",
    description=textwrap.dedent(
        """
        This API provides federated sharing of police data using a searchable
        index of police records. The index only contains information necessary
        for search and aggregation. NPDC partners contribute to the index while
        maintaining ownership over the full record. Partners can use the API to
        authorize users to access the full records on their systems. This thus
        facilitates federated access control and data ownership.
        """
    ),
    # The version of the API. 0.X.Y is initial development with breaking changes
    # allowed on minor version changes.
    version="0.1.0",
    # Version of the `/apidoc/openapi.json` format
    # https://swagger.io/specification/
    openapi_version="3.0.3",
    # Only document routes decorated with validators
    mode="strict",
    # By default, all routes require either cookie or bearer auth
    security={"cookieAuth": [], "bearerAuth": []},
    servers=[
        Server(
            url="",
            description="This Origin",
        ),
        Server(
            url="https://dev-api.nationalpolicedata.org",
            description="Development environment",
        ),
        Server(
            url="https://stage-api.nationalpolicedata.org",
            description="Staging environment",
        ),
        Server(
            url="https://api.nationalpolicedata.org",
            description="Production environment",
        ),
    ],
    security_schemes=[
        # Cookie auth is used by browsers for GET requests
        SecurityScheme(
            name="cookieAuth",
            data={
                "type": "apiKey",
                "name": "access_token_cookie",
                "in": "cookie",
            },
        ),
        # Bearer auth is used by other API consumers
        SecurityScheme(
            name="bearerAuth",
            data={
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT",
            },
        ),
    ],
)


# A decorator to validate request bodies using Pydantic models
def validate_request(model: BaseModel):
    """
    Validate the request body using a Pydantic model.

    Args:
        model (BaseModel): The Pydantic model to use for validation.

    Returns:
        function: A decorator function that validates the request body.
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                body = model(**request.json)
            except ValidationError as e:
                return jsonify({
                    "status": "Unprocessable Entity",
                    "message": "Invalid request body",
                    "errors": e.errors(),
                }), 422

            request.validated_body = body
            return f(*args, **kwargs)
        return decorated_function
    return decorator
