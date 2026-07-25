# Introduction

A webapp version of Terraforming Mars, for education and fun.

# Setup

Install `uv` with

```sh
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Install `bun` with

```sh
npm install -g bun
```

Finally, install project dependencies, by running the following from project root:

```sh
uv sync
bun install
```

# Development

The project is organized as a SvelteKit project; see [here](https://svelte.dev/docs/kit/project-structure)
to read about the way SvelteKit projects are set up.

The frontend server pages can be found in `src/routes`, while the Python/FastAPI backend server
lives in `src/server`. We share types across the backend and frontend using OpenAPI, using
`src/server/scripts/gen_schema.py` to generate a YAML schema from the FastAPI server
(see [here](https://fastapi.tiangolo.com/tutorial/response-model/?h=response_model) for details
on how you tell FastAPI what the API response types are), and `openapi-typescript` to generate
Typescript types (in `src/lib/schema.d.ts`) from the YAML.

## Local deployment

To run the backend server, run

```sh
PYTHONPATH=./src/lib/server uv run fastapi dev
```

To run the frontend server, run

```sh
bun run dev
```

Note that the backend server deploys to port 8000 while the frontend server deploys to port 5173;
in dev, frontend server then uses vite to also proxy the backend server through the frontend
server's address so we don't need to do anything about CORS.

## Synchronizing types

To synchronize API response types, you can run:

```sh
bun run openapi-sync
```

## Code

It may be helpful to add Svelte, Typescript, and Python language support to your editor.

### Formatting and linting

- **oxfmt** formats TS/Svelte/JSON/CSS/MD (config: `.oxfmtrc.json`)
- **oxlint** lints TS/JS and the `<script>` blocks of Svelte files (config: `.oxlintrc.json`)
- **ruff** formats and lints Python (config: `[tool.ruff]` in `pyproject.toml`)
- **svelte-check** typechecks `.svelte` and `.ts` files (`bun run check`)
- **pyright** typechecks Python (`uv run pyright`)

To run format/lint manually over the whole repo:

```sh
bun run check  # svelte-check + pyright
bun run format # oxfmt + ruff format
bun run lint # oxlint + ruff check
```

We've set up git hooks to automatically format and lint code with each commit. They are managed
by [lefthook](https://lefthook.dev) (see `lefthook.yml`) and installed automatically when you run
`bun install`:

- **pre-commit** formats and lint-fixes staged files and re-stages the results; only unfixable
  lint errors block the commit.
- **pre-push** runs the slower typechecks (`svelte-check` and `pyright`).
