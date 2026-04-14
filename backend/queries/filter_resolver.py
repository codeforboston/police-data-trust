from neomodel import db


class FilterResolver:
    def _as_list(self, value: str | list[str] | None) -> list[str]:
        if value is None:
            return []
        if isinstance(value, list):
            return value
        return [value]

    def resolve_city_uids(
        self,
        *,
        city: str | list[str] | None = None,
        city_uid: str | list[str] | None = None,
        state: str | None = None,
    ) -> list[str]:
        city_values = self._as_list(city)
        city_uid_values = self._as_list(city_uid)
        resolved_uids: list[str] = []

        if city_uid_values:
            query = """
            MATCH (city:CityNode)
            WHERE city.uid IN $city_uids
            RETURN DISTINCT city.uid
            """
            rows, _ = db.cypher_query(query, {"city_uids": city_uid_values})
            resolved_uids.extend(row[0] for row in rows)

        if not city_values and not state:
            return list(dict.fromkeys(resolved_uids))

        if city_values and state:
            query = """
            MATCH (city:CityNode)-[:WITHIN_COUNTY]->
                (:CountyNode)-[:WITHIN_STATE]
                ->(state:StateNode {abbreviation: $state})
            WHERE toLower(city.name) IN $cities
            RETURN DISTINCT city.uid
            """
            params = {
                "cities": [value.lower() for value in city_values],
                "state": state,
            }
        elif city_values:
            query = """
            MATCH (city:CityNode)
            WHERE toLower(city.name) IN $cities
            RETURN DISTINCT city.uid
            """
            params = {"cities": [value.lower() for value in city_values]}
        else:
            query = """
            MATCH (city:CityNode)-[:WITHIN_COUNTY]->
                (:CountyNode)-[:WITHIN_STATE]
                ->(state:StateNode {abbreviation: $state})
            RETURN DISTINCT city.uid
            """
            params = {"state": state}

        rows, _ = db.cypher_query(query, params)
        resolved_uids.extend(row[0] for row in rows)
        return list(dict.fromkeys(resolved_uids))

    def resolve_source_uids(
        self,
        *,
        source: str | list[str] | None = None,
        source_uid: str | list[str] | None = None,
    ) -> list[str]:
        source_uid_values = self._as_list(source_uid)
        source_name_values = self._as_list(source)

        resolved_uids: list[str] = []

        if source_uid_values:
            query = """
            MATCH (s:Source)
            WHERE s.uid IN $source_uids
            RETURN DISTINCT s.uid
            """
            rows, _ = db.cypher_query(query, {"source_uids": source_uid_values})
            resolved_uids.extend(row[0] for row in rows)

        if source_name_values:
            query = """
            MATCH (s:Source)
            WHERE toLower(s.name) IN $source_names
            RETURN DISTINCT s.uid
            """
            rows, _ = db.cypher_query(
                query,
                {
                    "source_names": [
                        value.lower() for value in source_name_values
                    ]
                },
            )
            resolved_uids.extend(row[0] for row in rows)

        return list(dict.fromkeys(resolved_uids))
