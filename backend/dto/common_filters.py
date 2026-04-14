from backend.database.models.agency import State


def normalize_string_or_list(value):
    if value is None:
        return None

    if isinstance(value, list):
        normalized = [" ".join(str(item).split()) for item in value]
        normalized = [item for item in normalized if item]
        return normalized or None

    normalized = " ".join(str(value).split())
    return normalized or None


def normalize_upper_string(value):
    if value is None:
        return None
    return str(value).strip().upper() or None


def validate_state_code(value):
    if value and value not in State.choices():
        raise ValueError(f"Invalid state: {value}")
    return value
