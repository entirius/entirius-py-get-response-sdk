# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from get_response_sdk import GetResponseClient


def test_client_defaults():
    client = GetResponseClient()
    assert client.base_url == "https://api.getresponse.com/v3"


def test_generate_resource_url():
    client = GetResponseClient()
    assert client.generate_resource_url("shops") == "https://api.getresponse.com/v3/shops"


def test_generate_auth_headers():
    client = GetResponseClient()
    headers = client.generate_auth_headers("test-key")
    assert headers["X-Auth-Token"] == "api-key test-key"
    assert headers["Content-Type"] == "application/json"
