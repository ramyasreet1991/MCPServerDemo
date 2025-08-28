from pathlib import Path
from pydantic import BaseSettings


class Settings(BaseSettings):
    vendors_file: Path = Path(__file__).resolve().parent.parent / "config" / "vendors.yml"
    policy_file: Path = Path(__file__).resolve().parent.parent / "config" / "policy.yml"

    class Config:
        env_prefix = "ORCH_"


settings = Settings()


def load_yaml(path: Path) -> dict:
    if not path.exists():
        return {}
    text = path.read_text()
    try:
        import json
        return json.loads(text)
    except Exception:
        pass
    data: dict = {}
    stack = [data]
    indent_levels = [0]
    for line in text.splitlines():
        if not line.strip() or line.strip().startswith("#"):
            continue
        indent = len(line) - len(line.lstrip(" "))
        key, _, value = line.strip().partition(":")
        value = value.strip()
        while indent < indent_levels[-1]:
            stack.pop()
            indent_levels.pop()
        if not value:
            new_dict = {}
            stack[-1][key] = new_dict
            stack.append(new_dict)
            indent_levels.append(indent + 2)
        else:
            if value.startswith("[") and value.endswith("]"):
                items = [i.strip().strip("'\"") for i in value[1:-1].split(",") if i.strip()]
                stack[-1][key] = items
            else:
                stack[-1][key] = value.strip("'\"")
    return data
