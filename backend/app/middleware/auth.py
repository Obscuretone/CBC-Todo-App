import jwt
from sanic.exceptions import Unauthorized
from config import Config


async def auth_middleware(request):
    public_paths = ("/", "/auth")
    if request.method == "OPTIONS" or request.path in public_paths or request.path.startswith("/auth/"):
        return

    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise Unauthorized("Missing Authorization header")

    token_parts = auth_header.split(" ", 1)
    if len(token_parts) != 2 or token_parts[0].lower() != "bearer":
        raise Unauthorized("Invalid Authorization header format")

    token = token_parts[1]
    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
        request.ctx.user_uuid = payload["uuid"]
    except jwt.ExpiredSignatureError as e:
        raise Unauthorized(f"Token has expired {e}")
    except jwt.InvalidTokenError:
        raise Unauthorized("Invalid token")
