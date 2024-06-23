from fastapi import FastAPI, Depends
from fastapi.security import HTTPBearer

app = FastAPI(title="Service B", docs_url=None, redoc_url=None)


auth_scheme = HTTPBearer(
    auto_error=False,
    scheme_name="JWT Auth",
    description="Please use **/auth/login** endpoint to obtain a valid JWT",
)


@app.get("/hello", dependencies=[Depends(auth_scheme)], tags=["Hello"])
async def hello():
    return {"message": "Hello from Service B"}


@app.get("/internal/hello", include_in_schema=False)
async def internal_hello():
    return {"message": "internal hello from Service B"}
