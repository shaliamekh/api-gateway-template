from fastapi.security import HTTPBearer

oauth_scheme = auth_scheme = HTTPBearer(auto_error=False, scheme_name="JWT Auth")
