import json
from typing import Any


def modify_paths(body: bytes, service_name: str) -> dict[str, Any]:
    data: dict[str, Any] = json.loads(body.decode())
    modified_paths = {}
    for path, details in data["paths"].items():
        new_path = f"/{service_name}" + path
        modified_paths[new_path] = details
    data["paths"] = modified_paths
    return data
