To run backend tests locally:

## Pytest (Unit Tests)

1. Start the application cluster with `docker-compose up`

2. Start the test database with `docker-compose --profile test up`.
Yes, you should start the test database separately. It'll be more likely to boot properly this way.

3. Add a test marker to the test DB. This will allow the DB to clear itself after each test run. See instructions below.

4. Connect to the API container with `docker exec -it "police-data-trust-api-1" /bin/bash`. You can find the container name by running `docker ps`.

5. Run the tests with `python -m pytest`.

6. If you want to run a specific test file, you can do so with `python -m pytest <path_to_test_file>`. You can also run a specific test with `python -m pytest <path_to_test_file>::<test_function_name>`.


## Adding a test marker to the test database

1. With the test database running, navigate to `localhost:7474` in your browser.

2. On the Neo4J web interface, select `neo4j://127.0.0.1:7688` as the connection URL. Otherwise, you will connect to the main database.

3. Log in with the username `neo4j` and the password `test_pwd`.

4. Run the following query to add a test marker to the database:

```
MERGE (n:TestMarker {name: 'TEST_DATABASE'});
```

5. You can now run the tests. The database will clear itself after each test run.


## Flake8 (Linting)

1. Start the application cluster with `docker-compose up`

2. Connect to the API container with `docker exec -it "police-data-trust-api-1" /bin/bash`. You can find the container name by running `docker ps`.

3. Run the linter with `flake8 backend/`.
```
