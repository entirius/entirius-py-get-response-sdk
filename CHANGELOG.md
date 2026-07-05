# Changelog

All notable changes to this project are documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [3.0.0] - 2026-07-05

Initial public release.

### Added

- `GetResponseClient` — GetResponse REST API v3 client (contacts, newsletters, custom fields).
- E-commerce API: shops, categories, products, carts and orders (full CRUD), plus contact custom fields
  (`get_custom_fields`, `create_custom_field`, `upsert_contact_custom_fields`).
- DTOs for contact and subscription webhook payloads; response validators (error messages include the API `context`).
- Bundled OpenAPI v3 specification (`open-api.json`).
- Toolchain: uv (env + lock), ruff (lint + format), hatchling (build), pytest;
  MPL-2.0 with per-file headers; pre-commit + CI (lint, test, secret-scan).
