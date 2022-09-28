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
```

3. Build and run the project with `docker-compose build; docker-compose up -d; docker-compose logs -f app`

## Installation (Frontend Only)

This method runs the frontend natively on your computer and does not require a running backend, which can be convenient.

1. Make sure that you have `node 16+` and either `npm 7+` or `yarn` installed.
2. Follow the [install instructions](./frontend/README.md) in the `frontend` directory.

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
