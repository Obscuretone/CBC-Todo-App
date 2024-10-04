import jwt

from sanic import Sanic
from sanic.response import json
from sanic.request import Request
from sanic_openapi import doc, openapi2_blueprint
from sanic_cors import CORS
from sanic.exceptions import Unauthorized
from datetime import datetime
import os
import sys

from models.tasks import task_blueprint
from models.auth import auth_blueprint
from config import Config

app = Sanic("cbc-todo-api")

CORS_URL = os.environ.get("CORS_ORIGIN", "http://localhost:3000")
CORS(app, origins=[CORS_URL], supports_credentials=True)

# Load config
app.config.update({k: v for k, v in Config.__dict__.items() if not k.startswith("__")})

# Register the Swagger/OpenAPI blueprint
# app.blueprint(openapi2_blueprint, url_prefix="/docs")

# Register blueprints
app.blueprint(task_blueprint)
app.blueprint(auth_blueprint)

# TODO: move this to a config
# print(app.router.routes_all)
# Load secret key and check if it's set
SECRET_KEY = os.environ.get("SECRET_KEY")
if SECRET_KEY is None:
    print("Error: SECRET_KEY environment variable not set.")
    sys.exit(1)  # Exit the program if SECRET_KEY is not set


# Define a basic route with OpenAPI documentation
@app.route("/")
@doc.response(200, str, description="Welcome message")
async def index(request: Request):
    """
    CBC Todo API v1
    """
    return json({"message": "Welcome to CBC Todo App!"}, status=200)


# Check the token on every request
@app.middleware("request")
async def check_jwt(request):
    exempt_path = "/auth/"

    print(request.path)

    # Skip the middleware for the exempt paths
    if request.path == exempt_path:
        return

    # Get the Authorization header
    auth_header = request.headers.get("Authorization")

    if not auth_header:
        raise Unauthorized("Missing Authorization header")

    # Extract the token from the Authorization header
    token_parts = auth_header.split("Bearer ")

    # Ensure we have a token
    if len(token_parts) != 2:
        raise Unauthorized("Invalid Authorization header format")

    token = token_parts[1]

    try:
        # Decode the JWT token (verify the signature)
        payload = jwt.decode(
            token, SECRET_KEY, algorithms=["HS256"]
        )  # Verify the signature using your secret key

        # Check Expiry
        if "exp" in payload and payload["exp"] < datetime.utcnow().timestamp():
            raise Unauthorized("Token has expired")

        # Add payload (user data) to the request object
        request.ctx.user_uuid = payload["uuid"]

    except jwt.ExpiredSignatureError:
        raise Unauthorized("Token has expired")
    except jwt.InvalidTokenError:
        raise Unauthorized("Invalid token")


DEBUG = os.environ.get("SANIC_DEBUG", "False") == "True"
AUTO_RELOAD = os.environ.get("SANIC_DEBUG", "False") == "True"

if __name__ == "__main__":
    # Run the app
    app.run(host="0.0.0.0", port=8000, debug=DEBUG, auto_reload=AUTO_RELOAD)
