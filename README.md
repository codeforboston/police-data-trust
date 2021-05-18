# police-data-trust
## Installation

1. Make sure that [Docker](https://www.docker.com) is installed on your machine. 

2. [Fork](https://docs.github.com/en/github/getting-started-with-github/fork-a-repo) a copy of the main repo to your GitHub account. 

3. Clone this repository `git clone git@github.com:codeforboston/police-data-trust.git`

4. Create a `.env` file in the root of your local project folder, and add your preferred PostgreSQL username and password:

```
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=police_data
POSTGRES_HOST=db
```

5. Build and run the project with `docker-compose build; docker-compose up -d; docker-compose logs -f app`


# Documentation

[Docs](https://codeforboston.github.io/police-data-trust)
