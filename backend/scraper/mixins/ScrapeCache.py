"""
This module contains the ScrapeCache class, which is used to store and
retrieve scraped data from a cache.
The cache can be implemented with any database, but Redis is used by default.
"""

import redis
from typing import Literal, Union, Any, Optional


class ScrapeCache:
    def __init__(self, backend_client: Union["RedisClient", "PostgresClient"]):
        self.backend_client = backend_client

    def set_json(
        self,
        key: str,
        value: dict[str, Any],
        table: Optional[str] = None,
        expiration_time: Optional[int] = None,
    ) -> None:
        self.backend_client.set_json(  # type: ignore
            key, value, table, expiration_time
        )

    def get_json(
        self, key: str, table: Union[str, None] = None
    ) -> Optional[dict[str, Any]]:
        return self.backend_client.get_json(key, table)  # type: ignore


class RedisClient:
    def __init__(
        self, host: str = "scraper-cache", port: int = 6379, db: int = 0
    ):
        self.connection = redis.StrictRedis(host=host, port=port, db=db)

    def _encode_dict(self, value: dict[str, Any]) -> dict[str, str]:
        """Redis doesn't support storing dicts with non-string values, so we
        need to convert them to strings."""
        return {key: str(value) for key, value in value.items()}

    def set_json(
        self,
        key: str,
        value: dict[str, Any],
        table: Union[str, None] = None,
        expiration_time: Optional[int] = None,
    ) -> None:
        """
        Set a JSON value in Redis.

        Args:
            key (str): The key to store the JSON value under.
            value (dict[str, Any]): The JSON value to store.
            table (str, optional): The table name to prefix the key with.
            Defaults to None.
            expiration_time (int, optional): The expiration time in seconds.
            Defaults to None.
        """
        redis_key = key if not table else f"{table}:{key}"
        print(redis_key, self._encode_dict(value))
        self.connection.hmset(  # type: ignore
            redis_key, self._encode_dict(value)
        )
        if expiration_time:
            self.connection.expire(redis_key, expiration_time)  # type: ignore

    def get_json(
        self, key: str, table: Optional[str] = None
    ) -> Optional[dict[str, Any]]:
        """
        Get a JSON value from Redis.

        Args:
            key (str): The key of the JSON value to retrieve.
            table (str, optional): The table name to prefix the key with.
            Defaults to None.

        Returns:
            Optional[dict[str, Any]]: The retrieved JSON value, or None if not
            found.
        """
        return (
            self.connection.hgetall(key)  # type: ignore
            if not table
            else self.connection.hgetall(f"{table}:{key}")  # type: ignore
        )


class PostgresClient:
    """This is a stub for a PostgreSQL client. It is not implemented."""

    def __init__(
        self,
        host: str = "localhost",
        port: int = 5432,
        user: str = "postgres",
        password: str = "",
        database: str = "postgres",
    ):
        ...


class ScrapeCacheContainer:
    def __init__(self, db_type: Literal["REDIS", "POSTGRES"] = "REDIS"):
        if db_type == "REDIS":
            self.backend_client = RedisClient()
        else:
            self.backend_client = PostgresClient()

    def get_cache(self):
        return ScrapeCache(self.backend_client)
