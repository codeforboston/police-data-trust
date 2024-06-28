# Police Data Index Backend

This is the backend for the National Police Data Index project. It is a Python Flask application that serves as the API for the front end.

## Database

The backend uses a PostgreSQL database to store data. The database schema is defined in [database/models](https://github.com/codeforboston/police-data-trust/tree/a743c232b5737b193086264e1364b1475873a884/backend/database/models).

You can access the database using the credentials you stored in the `.env` file. With those credentials, you can connect to the database and interact with it using SQL commands. You can do this by either using the command line or a GUI tool.

### Command Line

To connect to the database using the command line, you can use the `psql` command. You can run the following command to connect to the database:
```bash
psql -h localhost -U your_username -d your_database
```

### GUI Tool
We recommend using PGAdmin to interact with the database. You can download it [here](https://www.pgadmin.org/download/).

You can connect to the database by creating a new server and entering the credentials you stored in the `.env` file.

## Authentication

Before you can send requests to the API, you must first authenticate. Each API request must include an `Authorization` header with a valid JWT token. To obtain this, we'll be creating a user account and then logging in to get the token. 

### Create a User

To create a user account, send a POST request to the [`/register`](https://github.com/codeforboston/police-data-trust/blob/a743c232b5737b193086264e1364b1475873a884/backend/routes/auth.py#L62) endpoint with the correct payload. 

The response will include the User information as well as a JWT token that you can use to authenticate your API requests.

### Login

To login, send a POST request to the [`/login`](https://github.com/codeforboston/police-data-trust/blob/a743c232b5737b193086264e1364b1475873a884/backend/routes/auth.py#L20) endpoint with the correct payload.

The response will include a JWT token that you can use to authenticate your API requests.

### Using the Token

To authenticate your API requests, include the JWT token in the `Authorization` header. The header should look like this:
```
Authorization: Bearer <your_token>
```
