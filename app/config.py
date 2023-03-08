import json
from pathlib import Path
from typing import Optional

BASE_URL = Path(__file__).resolve().parent.parent


def get_secret(
    Key: str,
    defalut_value: Optional[str] = None,
    json_path: str = str(BASE_URL / "secrets.json"),
):
    with open(json_path) as f:
        secrets = json.loads(f.read())
    try:
        return secrets[Key]
    except KeyError:
        if defalut_value:
            return defalut_value
        raise EnvironmentError(f"Set the {Key} environment variable.")

MONGO_DB_NAME = get_secret("MONGO_DB_NAME")
MONGO_URL = get_secret("MONGO_URL")
NAVER_API_ID = get_secret("NAVER_API_ID")
NAVER_API_SECRET = get_secret("NAVER_API_SECRET")

if __name__ == "__main__":
    world = get_secret("hello")
    print(world)
