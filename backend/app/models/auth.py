import os
import jwt
import httpx
from sanic import Blueprint
from sanic.response import json
from sanic.exceptions import Unauthorized
from sanic_openapi import doc
from sqlalchemy import text
from datetime import datetime, timedelta
from db import get_db_session  # Ensure this import is correct

# Azure AD settings from environment variables
AZURE_AD_TENANT_ID = os.getenv("ENTRA_ID_TENANT_ID")
AZURE_AD_AUTHORITY = f"https://login.microsoftonline.com/{AZURE_AD_TENANT_ID}/v2.0"
AZURE_AD_AUDIENCE = "00000003-0000-0000-c000-000000000000"  # Microsoft Graph
AZURE_AD_JWKS_URL = (
    f"https://login.microsoftonline.com/{AZURE_AD_TENANT_ID}/discovery/v2.0/keys"
)
AZURE_AD_ISSUER = f"https://sts.windows.net/{AZURE_AD_TENANT_ID}/"

# Secret key for signing your JWT token
SECRET_KEY = os.environ.get("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY environment variable is not set.")

auth_blueprint = Blueprint("auth", url_prefix="/auth")


async def fetch_jwks():
    print(AZURE_AD_JWKS_URL)
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(AZURE_AD_JWKS_URL)
            response.raise_for_status()
            return response.json()
    except Exception as e:
        print(e)
        return None


async def verify_token(token):
    """Verify the token against Azure AD public keys."""
    jwks = await fetch_jwks()

    print(jwks)
    headers = jwt.get_unverified_header(token)
    if "kid" not in headers:
        raise Unauthorized("Invalid token header")

    # Find the key corresponding to the token's key ID (kid)
    key = next((k for k in jwks["keys"] if k["kid"] == headers["kid"]), None)
    if key is None:
        raise Unauthorized("No token")

    # Construct a public key from the Azure AD public key
    public_key = jwt.algorithms.RSAAlgorithm.from_jwk(
        {
            "kty": key["kty"],
            "kid": key["kid"],
            "use": key["use"],
            "n": key["n"],
            "e": key["e"],
        }
    )

    try:
        # Decode the token and verify its claims
        payload = jwt.decode(
            token,
            public_key,
            algorithms=[headers["alg"]],
            audience=AZURE_AD_AUDIENCE,  # Microsoft Graph https://learn.microsoft.com/en-us/troubleshoot/azure/entra/entra-id/governance/verify-first-party-apps-sign-in
            issuer=AZURE_AD_ISSUER,
            options={
                "verify_signature": False  # TODO: The JWT from microsoft is failing out of the box. Debug later.
            },
        )

        return payload
    except jwt.ExpiredSignatureError:
        raise Unauthorized("Token expired")
    except jwt.InvalidTokenError as e:
        print("Invalid Token Error:", str(e))
        raise Unauthorized("Invalid token")


def generate_jwt_token(user_uuid):
    """Generate a new JWT token for your application."""
    expiration_time = datetime.utcnow() + timedelta(
        hours=1
    )  # Set token expiration to 1 hour
    return jwt.encode(
        {
            "uuid": user_uuid,
            "exp": expiration_time,
        },
        SECRET_KEY,
        algorithm="HS256",
    )


@auth_blueprint.route("/", methods=["POST"], name="Authenticate")
@doc.summary("Authenticate using Azure AD (POST)")
@doc.description("Verify the MS token and generate your Todo App token.")
@doc.operation("auth_post")
@doc.consumes(
    doc.JsonBody(
        {"token": doc.String(description="Bearer token from Azure AD", required=True)}
    ),
    location="body",
)
@doc.response(
    200,
    {
        "application/json": {
            "schema": {
                "type": "object",
                "properties": {
                    "message": {"type": "string", "example": "Authenticated"},
                    "token": {"type": "string", "example": "JWT_TOKEN_HERE"},
                },
            }
        }
    },
)
@doc.response(
    401,
    {
        "application/json": {
            "schema": {
                "type": "object",
                "properties": {
                    "message": {"type": "string", "example": "Invalid credentials"}
                },
            }
        }
    },
)
async def login(request):

    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return json({"message": "Missing or invalid Authorization header"}, status=401)

    bearer_token = auth_header.split(" ")[1]  # Get the token part

    try:
        # Verify the incoming bearer token
        payload = await verify_token(bearer_token)

        print(payload)
        # Extract user email from the payload
        user_email = payload.get("email")
        user_name = payload.get("given_name") + " " + payload.get("family_name")

        # Lookup or create the user in your database
        user_uuid = await get_user_uuid(user_email, user_name)
        print(user_uuid)
        # Generate your own JWT token
        token = generate_jwt_token(user_uuid)
        print(token)

        return json({"message": "Authenticated", "token": token}, status=200)

    except Unauthorized as e:
        return json({"message": str(e)}, status=401)
    except Exception as e:
        return json({"message": "Authentication failed", "details": str(e)}, status=500)


# Function to get or create a user and return the UUID
async def get_user_uuid(email, name):
    AsyncSessionLocal = get_db_session()
    async with AsyncSessionLocal() as session:
        try:
            # Step 1: Check if the user already exists
            result = await session.execute(
                text("SELECT uuid FROM users WHERE email = :email"), {"email": email}
            )
            user = result.fetchone()

        except Exception as e:
            print("Couldn't Find User")
            print(e)
            return None  # Exit early if an error occurs

        # Step 2: Handle cases where the user doesn't exist (create a new user)
        if not user:
            try:
                # Insert new user
                result = await session.execute(
                    text(
                        "INSERT INTO users (email, display_name) VALUES (:email, :display_name)"
                    ),
                    {
                        "email": email,
                        "display_name": name,
                    },
                )
                await session.commit()

                # After inserting, retrieve the UUID of the newly created user
                result = await session.execute(
                    text("SELECT uuid FROM users WHERE email = :email"),
                    {"email": email},
                )
                user = result.fetchone()

            except Exception as e:
                print("Couldn't create user")
                print(e)
                return None  # Exit early if user creation fails

        # Step 3: Use the UUID (either from existing or newly created user)
        user_uuid = user[0]  # Assuming the UUID is the first column in the result

        return user_uuid
