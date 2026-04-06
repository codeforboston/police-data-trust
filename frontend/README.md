# Frontend

This directory contains the NPDC web app built with Next.js App Router, React 19, TypeScript, and MUI.

## Stack

- Next.js 15
- React 19
- TypeScript
- MUI 7
- Vitest for component and provider tests
- Playwright for end-to-end tests

## Directory Overview

- `app/`: route entry points and page-level UI
- `components/`: shared UI and page compositions
- `providers/`: app-wide auth and search state
- `hooks/`: data-fetching hooks for detail pages
- `utils/`: API helpers, route constants, shared types, and auth helpers
- `tests/`: Playwright end-to-end tests
- `public/`: static assets

## Main Routes

- `/`: homepage with search entry point
- `/search`: search results
- `/officer/[uid]`: officer detail page
- `/agency/[uid]`: agency detail page
- `/unit/[uid]`: unit detail page
- `/profile`: current user profile
- `/profile/edit`: edit profile flow
- `/login`: sign-in page
- `/register`: registration flow
- `/forgot-password`: forgot password flow
- `/logout`: logout page

Some navigation links in the UI currently point to routes that are not implemented yet. Check the code before assuming every visible link has a backing page.

## Getting Started

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

By default the app runs on port `3000`. You can override that with `NPDI_WEB_PORT`.

## Environment

The frontend reads from these local env files for environment-specific builds:

- `.env.development`
- `.env.production`
- `.env.staging`
- `.env.ui`

The main runtime variable used in code is:

- `NEXT_PUBLIC_API_BASE_URL`: base URL for the backend API

If `NEXT_PUBLIC_API_BASE_URL` is not set, the app falls back to:

```text
http://localhost:5001/api/v1
```

## Scripts

- `npm run dev`: start the Next.js dev server with Turbopack
- `npm run build`: production build
- `npm run start`: start the production server
- `npm run lint`: run Next.js linting
- `npm run fix-lint`: auto-fix lint issues where possible
- `npm run check-formatting`: run Prettier in check mode
- `npm run fix-formatting`: format files with Prettier
- `npm run check-types`: run TypeScript without emitting output
- `npm run test:unit`: run Vitest tests
- `npm run test:e2e`: run Playwright tests
- `npm run test:e2e:ui`: run Playwright with the UI

## Testing

Run unit tests:

```bash
npm run test:unit
```

Run type checks:

```bash
npm run check-types
```

Run lint:

```bash
npm run lint
```

Run end-to-end tests:

```bash
npm run test:e2e
```

Playwright starts the local dev server automatically outside CI using `NPDI_WEB_PORT` or port `3000`.

## Architecture Notes

- Authentication is handled client-side through `AuthProvider`.
- Search state, pagination, and URL synchronization are handled in `SearchProvider`.
- Most data fetching for profile and detail pages is currently done from client components via `apiFetch`.
- Shared API route builders live in `utils/apiRoutes.ts`.
- Shared frontend data types live in `utils/api.ts`.

## Docker

This frontend can also run as part of the full application stack from the repository root. See the root [`README.md`](../README.md) for the Docker-based setup.
