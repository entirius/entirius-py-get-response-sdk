# AGENTS.md

GetResponse email marketing & e-commerce REST API SDK — distribution `entirius-py-get-response-sdk`,
import `get_response_sdk`.

## Commands

| Command | Meaning |
|---|---|
| `make install` | sync dependencies (uv, incl. extras) |
| `make check` | lint + format-check (ruff) |
| `make fix` | auto-fix lint + format |
| `make test` | test suite (pytest) |

## Conventions

- English only: code, docs, commits, branches, PRs.
- MPL-2.0: every non-trivial source file carries the license header (pre-commit inserts it).
- Toolchain: uv + ruff + hatchling + pytest; all config in `pyproject.toml`; `uv.lock` committed.
- Git flow: `master` (production) + `develop` (integration); changes land via PR; semver tag on `master`.
- Never rename the import package `get_response_sdk` — it is a public API contract.
- Default: do not commit — git is the user's call.

## Architecture

- `get_response_sdk.py` — `GetResponseClient`: builds authorized requests to the GetResponse REST API v3
  (`X-Auth-Token: api-key <key>`); contacts, newsletters, custom fields and full e-commerce CRUD.
- `dto/` — contact and subscription-webhook payload dataclasses (`marshmallow-dataclass`).
- `validators/` — response shape validation; error messages carry the API `context` field.
- Integration tests are not shipped (they required a live API key); a local smoke test covers client construction.
