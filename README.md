# entirius-py-get-response-sdk

A Python client for the GetResponse email marketing REST API, part of Entirius, the open-source modular ecommerce platform.
It covers contacts, campaigns, custom fields and the ecommerce resources (shops, categories, products, carts, orders)
behind one `GetResponseClient` class.

[![PyPI](https://img.shields.io/pypi/v/entirius-py-get-response-sdk.svg)](https://pypi.org/project/entirius-py-get-response-sdk/)
[![Python](https://img.shields.io/pypi/pyversions/entirius-py-get-response-sdk.svg)](https://pypi.org/project/entirius-py-get-response-sdk/)
[![License: MPL-2.0](https://img.shields.io/badge/license-MPL--2.0-blue.svg)](https://github.com/entirius/entirius-py-get-response-sdk/blob/develop/LICENSE)

## What it does

- Lists campaigns and their contacts and reads one contact (`get_campaign_list()`, `get_campaign_contact()`, `get_detail_contact()`).
- Reads, creates and updates shops and their categories (`get_shops()`, `create_shop()`, `create_category()`).
- Reads, creates, updates and deletes products (`get_products()`, `create_product()`, `delete_product()`).
- Syncs carts and orders of a shop (`create_cart()`, `update_cart()`, `create_order()`, `update_order()`).
- Manages custom fields and sets them on a contact (`get_custom_fields()`, `create_custom_field()`, `upsert_contact_custom_fields()`).
- Reaches any other resource through the generic calls (`get_resource()`, `post_resource_instance()`).

## Installation

```shell
uv add entirius-py-get-response-sdk
pip install entirius-py-get-response-sdk
```

The import name is `get_response_sdk`.

## Quick start

```python
from get_response_sdk import GetResponseClient

client = GetResponseClient()
shops = client.get_shops(api_key="...")
```

The API key is passed per call, so one client serves several GetResponse accounts.

## Requirements

- Python 3.11 or newer.
- `requests` and `marshmallow-dataclass` (installed as dependencies).
- A GetResponse account (API key).

## Documentation

- Entirius documentation: https://docs.entirius.com/
- Changelog: https://github.com/entirius/entirius-py-get-response-sdk/blob/develop/CHANGELOG.md
- GetResponse REST API v3 reference: https://apidocs.getresponse.com/v3

## Part of Entirius

This SDK is one of the marketing integration clients used by the Entirius backend service (Volkanos).

- Backend service: https://github.com/entirius/entirius-service-volkanos
- Docker harness: https://github.com/entirius/entirius-zeno
- GetResponse module: https://github.com/entirius/entirius-django-getresponse
- Sibling marketing SDKs: https://github.com/entirius/entirius-py-edrone-sdk, https://github.com/entirius/entirius-py-salesmanago-sdk, https://github.com/entirius/entirius-py-synerise-sdk

## Development

```shell
make install     # sync dependencies (uv)
make check       # lint + format check (ruff)
make test        # test suite (pytest)
```

Development and agent instructions: https://github.com/entirius/entirius-py-get-response-sdk/blob/develop/AGENTS.md

## License

Mozilla Public License 2.0 (MPL-2.0) — see https://github.com/entirius/entirius-py-get-response-sdk/blob/develop/LICENSE.
