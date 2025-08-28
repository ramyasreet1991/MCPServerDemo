from typing import Any, Dict


def redact_inputs(args: Dict[str, Any]) -> Dict[str, Any]:
    """Mask password fields in args."""
    redacted = {}
    for key, value in args.items():
        if key.lower() == "password":
            redacted[key] = "***"
        else:
            redacted[key] = value
    return redacted


def redact_outputs(result: Any) -> Any:
    return result
