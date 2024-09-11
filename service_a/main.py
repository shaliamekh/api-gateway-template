import os
from datetime import datetime, timezone, timedelta

from fastapi import FastAPI, Depends
from fastapi.security import HTTPBearer
from pydantic import BaseModel, EmailStr, Field
from jose import jwt
import aiohttp


app = FastAPI(title="Service A", version="0.1.0", docs_url=None, redoc_url=None)


auth_scheme = HTTPBearer(
    auto_error=False,
    scheme_name="JWT Auth",
    description="Please use **/auth/login** endpoint to obtain a valid JWT",
)


@app.get("/hello", dependencies=[Depends(auth_scheme)], tags=["Hello"])
async def hello():
    return {"message": "Hello from Service A"}


class LoginInput(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)


@app.post("/auth/login", tags=["Auth"])
async def login(data: LoginInput):
    expire_at = datetime.now(tz=timezone.utc) + timedelta(minutes=30)
    payload = {"aud": data.email, "exp": expire_at}
    token = jwt.encode(payload, os.getenv("JWT_SECRET_KEY"), algorithm="HS256")
    return {"token": token}


@app.get("/cross-service-hello", dependencies=[Depends(auth_scheme)], tags=["Hello"])
async def cross_service_hello():
    async with aiohttp.ClientSession() as session:
        async with session.get("http://service-b:8080/internal/hello") as resp:
            response = await resp.json()
    return {"message": f"Hello from Service A and {response["message"]}"}
