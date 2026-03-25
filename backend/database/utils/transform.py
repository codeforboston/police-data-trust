from neo4j.time import (
    Date as Neo4jDate,
    DateTime as Neo4jDateTime,
)


# Convert date/datetime properties in dictionaries to ISO format strings
def transform_dates_in_dict(data: dict) -> dict:
    for key, value in data.items():
        if isinstance(value, Neo4jDate):
            data[key] = value.to_native().isoformat()
        elif isinstance(value, Neo4jDateTime):
            data[key] = value.to_native().isoformat()
        elif isinstance(value, dict):
            data[key] = transform_dates_in_dict(value)
        elif isinstance(value, list):
            data[key] = [
                transform_dates_in_dict(item) if isinstance(item, dict)
                else item for item in value]
    return data
