# police-data-trust

To get started:

1. [Fork](https://docs.github.com/en/github/getting-started-with-github/fork-a-repo) a copy of the main repo to your GitHub account.

2. Clone your fork: `git clone git@github.com:YOUR_GITHUB_NAME/police-data-trust.git`

3. Add the main repo to your remotes

```
cd police-data-trust
git remote add upstream https://github.com/codeforboston/police-data-trust.git
git fetch upstream
```

Now, whenever new code is merged you can pull in changes to your local repository:

```
git checkout main
git pull upstream main
```

## Installation (Full Application)

This method uses Docker to run the complete application stack.

1. Make sure that [Docker](https://www.docker.com) is installed on your machine.

2. Create a `.env` file in the root of your local project folder, and add your preferred PostgreSQL username and password:

```
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=police_data
POSTGRES_HOST=db
POSTGRES_PORT=5432
PDT_API_PORT=5000
MIXPANEL_TOKEN=your_mixpanel_token
```

> **Note**
> When running locally, you may need to update one of the ports in the `.env` file if it conflicts with another application on your machine.

3. Build and run the project with `docker-compose build && docker-compose up -d && docker-compose logs -f`

## Installation (Frontend Only)

This method runs the frontend natively on your computer and does not require a running backend, which can be convenient.

1. Make sure that you have `node 16+` and either `npm 7+` or `yarn` installed.
2. Follow the [install instructions](./frontend/README.md) in the `frontend` directory.

## Testing with Docker

All code must pass the unit tests and style checks before it can be merged into the main branch. You can run the tests locally by opening up a comand line interface to a docker container while it's running the application:


```
docker exec -it "police-data-trust-api-1" /bin/bash

```

You'll need to replace `police-data-trust-api-1` with the name of the container you'd like tro connect to. You can see the names of all currently running containers by running `docker container ls`

```bash
docker container ls
CONTAINER ID   IMAGE                   COMMAND                  CREATED              STATUS              PORTS                    NAMES
c0cf********   police-data-trust-api   "/bin/sh -c '/wait &…"   About a minute ago   Up About a minute   0.0.0.0:5001->5001/tcp   police-data-trust-api-1
5e6f********   postgres:16.1           "docker-entrypoint.s…"   3 days ago           Up About a minute   0.0.0.0:5432->5432/tcp   police-data-trust-db-1
dacd********   police-data-trust-web   "docker-entrypoint.s…"   3 days ago           Up About a minute   0.0.0.0:3000->3000/tcp   police-data-trust-web-1
```

### Backend Tests

The current backend tests can be found in the GitHub Actions workflow file [python-tests.yml](https://github.com/codeforboston/police-data-trust/blob/0488d03c2ecc01ba774cf512b1ed2f476441948b/.github/workflows/python-tests.yml)

To run the tests locally, first start the application with docker-compose. Then open up a command line interface to the running container:

```
docker exec -it "police-data-trust-api-1" /bin/bash
```

Then run the tests:

```
flake8 backend/
python -m pytest
```

### Front End Tests

The current frontend tests can be found in the GitHub Actions workflow file [frontend-checks.yml](https://github.com/codeforboston/police-data-trust/blob/0488d03c2ecc01ba774cf512b1ed2f476441948b/.github/workflows/frontend-checks.yml)

To run the tests locally, first start the application with docker-compose. Then open up a command line interface to the running container:

```
docker exec -it "police-data-trust-web-1" /bin/bash
```

Then run the tests:

```
npm run lint
npm run check-formatting
npm run test
npm run check-types
```

# Documentation

[Docs](https://codeforboston.github.io/police-data-trust)

# Code Standards

## Typescript Style Guide

This style guide is intended to act as a quick reference for the most common scenarios

### Custom Types

For this codebase, we are using [interfaces](https://www.typescriptlang.org/docs/handbook/2/everyday-types.html#interfaces) instead of [type aliases](https://www.typescriptlang.org/docs/handbook/2/everyday-types.html#type-aliases).

### Utilizing Types

- We are aiming for a loose standard of explicitly typing as little as possible (relying on type inference or third-party library typing files to do the work whenever convenient), but as much as necessary (function params/args are a good example of what the compiler is bad at inferring). Erring on the side of 'stricter than absolutely necessary' definitely works for us!

- The [`any`](https://www.typescriptlang.org/docs/handbook/2/everyday-types.html#any) type should never be utilized here. Prefer [union types](https://www.typescriptlang.org/docs/handbook/2/everyday-types.html#union-types) in the case of values that are initially `null` (such as values that come from API calls), or [`unknown`](https://www.typescriptlang.org/docs/handbook/2/functions.html#unknown) in case of a type being truly impossible to discern ahead of time.

- When typing primitive values declared with `const`, explicitly typing them will be necessary to prevent their type from being implied as the literal value of said primitive, rather than it's corresponding data type.

## Functions

- Always use explicit typing in the case of function params and return types.

- If function parameters don't get modified by the function, strongly consider making them `readonly` to prevent mutation and have clearer code.

## React

- Prefer the `.tsx` file extension when JSX is involved, and `.ts` when it isn't.

### Props

- Refer to the [React/TypeScript Cheatsheet](https://react-typescript-cheatsheet.netlify.app/docs/basic/getting-started/basic_type_example) for examples of common propTypes.

- In the case of components that accept other React components as props, prefer typing those as `React.ReactNode`.

### Hooks

- Prefer type inference for `useState` for simple cases. If the hook initializes with a nullish value, strongly consider a union type.

- Since `useEffect` and `useLayoutEffect` don't return values, typing them is not necessary.

- When typing `useRef`, refer to the React/TypeScript cheatsheet for guidance on [your specific situation](https://react-typescript-cheatsheet.netlify.app/docs/basic/getting-started/hooks#useref).

### Forms & Events

- Type inference should be sufficient in the case of inline event handlers.

- IDE tooling (such as VSCode autocomplete) will offer helpful suggestions for specific event handler types.

- The React/TypeScript cheatsheet has a list of [specific event types](https://react-typescript-cheatsheet.netlify.app/docs/basic/getting-started/forms_and_events#list-of-event-types).

## Organization of props and attributes

Ordering of components —

- Class definitions
- Component / imports
- Event handlers inside class

HTML Props/attributes order:

- id, class, attributes
- Like properties alphabetized (?)

Directory structure:

- Pages: routable containers
- Shared: components being used/planned to be used in multiple places
- Compositions: components that have a single/limited specific context
