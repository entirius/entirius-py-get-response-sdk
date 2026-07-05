# get-response-sdk

GetResponse SDK — email marketing and e-commerce (shops, products, carts, orders, contacts) over the GetResponse
REST API v3.

## Installation

```shell
pip install entirius-py-get-response-sdk
```

## Usage

```python
from get_response_sdk import GetResponseClient

client = GetResponseClient()
shops = client.get_resource("shops", api_key="...")
```

The REST API v3 is documented at [apidocs.getresponse.com](https://apidocs.getresponse.com/v3).

## Development

```shell
make install     # sync dependencies (uv)
make check       # lint + format check (ruff)
make test        # test suite (pytest)
```

Development and agent instructions: [AGENTS.md](AGENTS.md).

## License

Mozilla Public License 2.0 — see [LICENSE](LICENSE).
