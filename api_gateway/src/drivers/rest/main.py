from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from config.settings import get_settings
from drivers.rest.exception_handlers.container import exception_container
from drivers.rest.middleware.middleware_container import middleware_container
from drivers.rest.routers import docs, generic, root, service_a
from drivers.rest.utils.row_json_response import RowJSONResponse

app = FastAPI(default_response_class=RowJSONResponse, openapi_url=None)

get_settings().configure_logging()

middleware_container(app)
exception_container(app)


app.mount(
    "/static", StaticFiles(directory=get_settings().base_path / "static"), name="static"
)


app.include_router(service_a.router)
app.include_router(docs.router)
app.include_router(root.router)
app.include_router(generic.router)
