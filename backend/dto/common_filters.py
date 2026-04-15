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


def normalize_upper_string_or_list(value):
    if value is None:
        return None

    if isinstance(value, list):
        normalized = [str(item).strip().upper() for item in value]
        normalized = [item for item in normalized if item]
        return normalized or None

    return normalize_upper_string(value)


def validate_state_code(value):
    if isinstance(value, list):
        validated = [item for item in value if item]
        invalid = [item for item in validated if item not in State.choices()]
        if invalid:
            raise ValueError(f"Invalid state: {', '.join(invalid)}")
        return validated or None

    if value and value not in State.choices():
        raise ValueError(f"Invalid state: {value}")
    return value
