# Frontend

This is a [Next.js](https://nextjs.org/) project bootstrapped with [`create-next-app`](https://github.com/vercel/next.js/tree/canary/packages/create-next-app).

_These instructions are for frontend only. If you are just getting started with the project, or need help starting the Docker environment, see the [README](../README.md) in the root directory._

## Getting Started

Change to the frontend directory and run all commands from here:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
# or
yarn install
```

If you are using Windows, configure NPM to use Git Bash when running scripts. Follow [these](https://stackoverflow.com/questions/23243353/how-to-set-shell-for-npm-run-scripts-in-windows/46006249#46006249) instructions.

**Note:** if you run into an error such as

```
/police-data-trust/frontend/node_modules/husky/lib/index.js:20
        throw new Error(`.git can't be found (see ${url})`);
        ^

Error: .git can't be found
```

you can copy the .git/ directory in the root of the project and move it to the frontend/ and try the install again and it should succeed. try the install again and remember do not commit this .git/ you may want to delete it afterwards until figured out alternative.

Run the development server:

```bash
npm run dev
# or
yarn dev
```

Open http://localhost:3000/login in your browser to view the login page. Login using the test account `test@example.com` / `password`. You can start editing the page by modifying `pages/search/index.js`. The page auto-updates as you edit the file.

## Testing

Once completed the steps above then to run tests: `yarn test`. You can use `yarn watch` to automatically run your tests as you edit files.

Bare minimum each incoming PR changes updating the UI must have UI snapshot tests. We expect tests only for project important logic but must reside in the `tests/` directory.

## Storybook

Besides testing with Jest, we also use Storybook to view UI components in isolation. Stories can be written for any visual component, and having a story for your component is a good way to show that it works. More information on how we're using it in this project can be found [here](./.storybook/USAGE.md).

## Learn More

To learn more about Next.js, take a look at the following resources:

- [Next.js Documentation](https://nextjs.org/docs) - learn about Next.js features and API.
- [Learn Next.js](https://nextjs.org/learn) - an interactive Next.js tutorial.

## What's different in Next.js from regular React?

- Next.js uses a page-based routing that will be familiar if you've used tools like Gatsby or Wordpress: A page will be created for every file with a `.js` (or any file type that compiles to JS) that goes in the `pages` folder. You can also nest routes using folders! See https://nextjs.org/docs/basic-features/pages

- Important note about pages: While there are a lot of good reasons to avoid using [default exports](https://humanwhocodes.com/blog/2019/01/stop-using-default-exports-javascript-module/), Next requires all page components to use this convention.

- All static assets must go in the `public` folder in the root of the front-end directory. It's ok to have nested folders within there, but every asset must be somewhere inside of that `public` folder. See https://nextjs.org/docs/basic-features/static-file-serving

- Next behaves mostly like React when it comes to styling applications. For full details for how the use case works (we're currently using CSS Modules), see https://nextjs.org/docs/basic-features/built-in-css-support

- Next has built-in image optimization(https://nextjs.org/docs/basic-features/image-optimization), and font optimization(https://nextjs.org/docs/basic-features/font-optimization).

- If there's data that needs to be served but that we don't necessarily need to/can serve from the Python back-end, API routes could be an option: https://nextjs.org/docs/api-routes/introduction.

- Because it's written in Node.js, you also have access to standard Node API packages such as `fs`, `path`, etc.

## Resources

- React/TS Cheatsheet: https://react-typescript-cheatsheet.netlify.app/
