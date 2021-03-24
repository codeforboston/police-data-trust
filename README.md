# police-data-trust
# Installation

1. Make sure that you have [Python 3.8](https://www.python.org/), [Git](https://git-scm.com/), and [PostgreSQL](https://www.postgresql.org/) are installed on your machine.

2. Clone this repository `git clone git@github.com:codeforboston/police-data-trust.git`

3. Create a `.env` file in the root of your local project folder, and add your preferred PostgreSQL username and password:

```
POSTGRES_USER=<YOUR_USERNAME>
POSTGRES_PASSWORD=<YOUR_PASSWORD>
```

4. Login into your local PostgreSQL instance using the preferred user from the previous step using the SQL Shell or the following command:

`psql -U postgres` 

and run the command: `CREATE DATABASE police_data;`

5. Test application by running either the `run_unix.sh` or `run_windows.bat` executable from the root of the application as appropriate for your operating system.


# Documentation

[Docs](https://codeforboston.github.io/police-data-trust)
