# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from typing import Any

import requests

from get_response_sdk.validators.response import validate_get_response


class GetResponseClient:
    subdomain: str
    api_key: str

    def __init__(self) -> None:
        self.header_content = None
        self.header_content_value = None
        self.token = None
        self.base_url = "https://api.getresponse.com/v3"
        self.prefix = "api-key"
        self.auth_header = "X-Auth-Token"

    def generate_resource_url(self, resource) -> str:
        return f"{self.base_url}/{resource}"

    def generate_auth_headers(self, api_key) -> dict:
        self.header_content = "Content-Type"
        self.header_content_value = "application/json"

        self.auth_header = "X-Auth-Token"
        self.prefix = "api-key"
        self.token = api_key
        return {self.header_content: self.header_content_value, self.auth_header: f"{self.prefix} {self.token}"}

    def get_resource(self, resource: str, api_key, params={}):
        url = self.generate_resource_url(resource)
        headers = self.generate_auth_headers(api_key)

        response = requests.get(url=url, headers=headers, params=params)
        validate_get_response(response=response)
        data = response.json()
        return data

    def delete_resource_instance(self, resource: str, api_key) -> tuple[int, str]:
        url = self.generate_resource_url(resource)
        headers = self.generate_auth_headers(api_key=api_key)

        response = requests.delete(
            url=url,
            headers=headers,
        )

        validate_get_response(response=response)
        success_msg = f"Profile {resource} deleted"
        return response.status_code, success_msg

    def post_resource_instance(self, instance: dict, resource: str, api_key) -> tuple[int, str | Any] | tuple[int, str]:
        url = self.generate_resource_url(resource)
        headers = self.generate_auth_headers(api_key)
        body = instance
        response = requests.post(url=url, headers=headers, json=body)
        validate_get_response(response=response)
        success_msg = f"New {resource} created"
        return response.status_code, success_msg

    def create_profile(self, instance: dict, resource: str, api_key):
        status_code, response = self.post_resource_instance(instance, resource, api_key)
        return status_code, response

    def delete_profile(self, resource: str, api_key):
        status_code, response = self.delete_resource_instance(resource, api_key)
        return status_code, response

    def get_campaign_list(self, api_key) -> list:
        return self.get_resource("campaigns", api_key)

    def get_campaign_contact(self, campaign_id, api_key, query: dict = {}, sort: dict = {}) -> dict:
        resource = f"campaigns/{campaign_id}/contacts"
        params = {
            **{f"query[{key}]": value for key, value in query.items()},
            **{f"sort[{key}]": value for key, value in query.items()},
        }
        data = self.get_resource(resource=resource, api_key=api_key, params=params)
        return data

    def get_detail_contact(self, contact_id, api_key) -> dict:
        resource = f"contacts/{contact_id}/"
        data = self.get_resource(resource=resource, api_key=api_key)
        return data

    # Category Management Methods
    def get_shop_categories(self, shop_id: str, api_key: str, query: dict = None) -> list:
        """
        Get list of categories for a shop.

        Args:
            shop_id: GetResponse shop ID
            api_key: API authentication key
            query: Optional query parameters (name, parentId, externalId, etc.)

        Returns:
            List of category dictionaries
        """
        resource = f"shops/{shop_id}/categories"
        params = {}

        if query:
            for key, value in query.items():
                params[f"query[{key}]"] = value

        data = self.get_resource(resource=resource, api_key=api_key, params=params)
        return data if isinstance(data, list) else []

    def get_category(self, shop_id: str, category_id: str, api_key: str) -> dict:
        """
        Get single category by ID.

        Args:
            shop_id: GetResponse shop ID
            category_id: GetResponse category ID
            api_key: API authentication key

        Returns:
            Category dictionary
        """
        resource = f"shops/{shop_id}/categories/{category_id}"
        data = self.get_resource(resource=resource, api_key=api_key)
        return data

    def create_category(self, shop_id: str, category_data: dict, api_key: str) -> tuple[int, dict]:
        """
        Create new category in shop.

        Args:
            shop_id: GetResponse shop ID
            category_data: Category data (name required, parentId/externalId/url/isDefault optional)
            api_key: API authentication key

        Returns:
            Tuple of (status_code, response_data)

        Example category_data:
            {
                "name": "Electronics",
                "externalId": "cat_123",
                "parentId": "gr_parent_id",  # optional
                "url": "https://shop.com/electronics",  # optional
                "isDefault": False  # optional
            }
        """
        resource = f"shops/{shop_id}/categories"
        url = self.generate_resource_url(resource)
        headers = self.generate_auth_headers(api_key)

        response = requests.post(url=url, headers=headers, json=category_data)
        validate_get_response(response=response)

        response_data = response.json() if response.content else {}
        return response.status_code, response_data

    def update_category(self, shop_id: str, category_id: str, category_data: dict, api_key: str) -> tuple[int, dict]:
        """
        Update existing category (POST).

        Args:
            shop_id: GetResponse shop ID
            category_id: GetResponse category ID
            category_data: Fields to update (send only changed fields)
            api_key: API authentication key

        Returns:
            Tuple of (status_code, response_data)
        """
        resource = f"shops/{shop_id}/categories/{category_id}"
        url = self.generate_resource_url(resource)
        headers = self.generate_auth_headers(api_key)

        response = requests.post(url=url, headers=headers, json=category_data)
        validate_get_response(response=response)

        response_data = response.json() if response.content else {}
        return response.status_code, response_data

    # Shop Management Methods
    def get_shops(self, api_key: str, query: dict = None) -> list:
        """
        Get list of shops.

        Args:
            api_key: API authentication key
            query: Optional query parameters (e.g., {"name": "My Shop"})

        Returns:
            List of shop dictionaries
        """
        resource = "shops"
        params = {}
        if query:
            for key, value in query.items():
                params[f"query[{key}]"] = value

        data = self.get_resource(resource=resource, api_key=api_key, params=params)
        return data if isinstance(data, list) else []

    def get_shop(self, shop_id: str, api_key: str) -> dict:
        """
        Get single shop details.

        Args:
            shop_id: GetResponse shop ID
            api_key: API authentication key

        Returns:
            Shop dictionary
        """
        resource = f"shops/{shop_id}"
        data = self.get_resource(resource=resource, api_key=api_key)
        return data

    def create_shop(self, shop_data: dict, api_key: str) -> tuple[int, dict]:
        """
        Create new shop in GetResponse.

        Args:
            shop_data: Shop data dictionary with keys: name, locale, currency
            api_key: API authentication key

        Returns:
            Tuple of (status_code, response_data with shopId)
        """
        resource = "shops"
        url = self.generate_resource_url(resource)
        headers = self.generate_auth_headers(api_key)

        response = requests.post(url=url, headers=headers, json=shop_data)
        validate_get_response(response=response)

        response_data = response.json() if response.content else {}
        return response.status_code, response_data

    def update_shop(self, shop_id: str, shop_data: dict, api_key: str) -> tuple[int, dict]:
        """
        Update existing shop (PATCH).

        Args:
            shop_id: GetResponse shop ID
            shop_data: Fields to update (send only changed fields)
            api_key: API authentication key

        Returns:
            Tuple of (status_code, response_data)
        """
        resource = f"shops/{shop_id}"
        url = self.generate_resource_url(resource)
        headers = self.generate_auth_headers(api_key)

        response = requests.patch(url=url, headers=headers, json=shop_data)
        validate_get_response(response=response)

        response_data = response.json() if response.content else {}
        return response.status_code, response_data

    # Product Management Methods
    def get_products(self, shop_id: str, api_key: str, query: dict = None) -> list:
        """
        Get list of products for a shop.

        Args:
            shop_id: GetResponse shop ID
            api_key: API authentication key
            query: Optional query parameters (name, externalId, etc.)

        Returns:
            List of product dictionaries
        """
        resource = f"shops/{shop_id}/products"
        params = {}

        if query:
            for key, value in query.items():
                params[f"query[{key}]"] = value

        data = self.get_resource(resource=resource, api_key=api_key, params=params)
        return data if isinstance(data, list) else []

    def get_product(self, shop_id: str, product_id: str, api_key: str) -> dict:
        """
        Get single product by ID.

        Args:
            shop_id: GetResponse shop ID
            product_id: GetResponse product ID
            api_key: API authentication key

        Returns:
            Product dictionary
        """
        resource = f"shops/{shop_id}/products/{product_id}"
        data = self.get_resource(resource=resource, api_key=api_key)
        return data

    def create_product(self, shop_id: str, product_data: dict, api_key: str) -> tuple[int, dict]:
        """
        Create new product in shop.

        Args:
            shop_id: GetResponse shop ID
            product_data: Product data (name, type, variants required)
            api_key: API authentication key

        Returns:
            Tuple of (status_code, response_data)

        Example product_data:
            {
                "name": "Product Name",
                "type": "physical",
                "url": "https://shop.com/product",
                "vendor": "Brand Name",
                "categories": ["cat_id_1", "cat_id_2"],
                "variants": [
                    {
                        "sku": "PROD-001",
                        "name": "Variant Name",
                        "price": 99.99,
                        "quantity": 10,
                        "externalId": "var_123"
                    }
                ],
                "externalId": "prod_123"
            }
        """
        resource = f"shops/{shop_id}/products"
        url = self.generate_resource_url(resource)
        headers = self.generate_auth_headers(api_key)

        response = requests.post(url=url, headers=headers, json=product_data)
        validate_get_response(response=response)

        response_data = response.json() if response.content else {}
        return response.status_code, response_data

    def update_product(self, shop_id: str, product_id: str, product_data: dict, api_key: str) -> tuple[int, dict]:
        """
        Update existing product (POST).

        Args:
            shop_id: GetResponse shop ID
            product_id: GetResponse product ID
            product_data: Fields to update (send only changed fields)
            api_key: API authentication key

        Returns:
            Tuple of (status_code, response_data)
        """
        resource = f"shops/{shop_id}/products/{product_id}"
        url = self.generate_resource_url(resource)
        headers = self.generate_auth_headers(api_key)

        response = requests.post(url=url, headers=headers, json=product_data)
        validate_get_response(response=response)

        response_data = response.json() if response.content else {}
        return response.status_code, response_data

    def delete_product(self, shop_id: str, product_id: str, api_key: str) -> tuple[int, str]:
        resource = f"shops/{shop_id}/products/{product_id}"
        url = self.generate_resource_url(resource)
        headers = self.generate_auth_headers(api_key)
        response = requests.delete(url=url, headers=headers)
        validate_get_response(response=response)
        return response.status_code, f"Product {product_id} deleted"

    def delete_category(self, shop_id: str, category_id: str, api_key: str) -> tuple[int, str]:
        resource = f"shops/{shop_id}/categories/{category_id}"
        url = self.generate_resource_url(resource)
        headers = self.generate_auth_headers(api_key)
        response = requests.delete(url=url, headers=headers)
        validate_get_response(response=response)
        return response.status_code, f"Category {category_id} deleted"

    # Cart Management Methods
    def get_carts(self, shop_id: str, api_key: str, query: dict = None) -> list:
        """Get list of carts for a shop."""
        resource = f"shops/{shop_id}/carts"
        params = self._build_query_params(query)
        data = self.get_resource(resource=resource, api_key=api_key, params=params)
        return data if isinstance(data, list) else []

    def _build_query_params(self, query: dict = None) -> dict:
        params = {}
        if query:
            for key, value in query.items():
                params[f"query[{key}]"] = value
        return params

    def get_cart(self, shop_id: str, cart_id: str, api_key: str) -> dict:
        """Get single cart details."""
        resource = f"shops/{shop_id}/carts/{cart_id}"
        data = self.get_resource(resource=resource, api_key=api_key)
        return data

    def create_cart(self, shop_id: str, cart_data: dict, api_key: str) -> tuple[int, dict]:
        """Create new cart."""
        resource = f"shops/{shop_id}/carts"
        url = self.generate_resource_url(resource)
        headers = self.generate_auth_headers(api_key)
        response = requests.post(url=url, headers=headers, json=cart_data)
        validate_get_response(response=response)
        response_data = response.json() if response.content else {}
        return response.status_code, response_data

    def update_cart(self, shop_id: str, cart_id: str, cart_data: dict, api_key: str) -> tuple[int, dict]:
        """Update existing cart."""
        resource = f"shops/{shop_id}/carts/{cart_id}"
        url = self.generate_resource_url(resource)
        headers = self.generate_auth_headers(api_key)
        response = requests.post(url=url, headers=headers, json=cart_data)
        validate_get_response(response=response)
        response_data = response.json() if response.content else {}
        return response.status_code, response_data

    def delete_cart(self, shop_id: str, cart_id: str, api_key: str) -> tuple[int, str]:
        """Delete cart."""
        resource = f"shops/{shop_id}/carts/{cart_id}"
        url = self.generate_resource_url(resource)
        headers = self.generate_auth_headers(api_key)
        response = requests.delete(url=url, headers=headers)
        validate_get_response(response=response)
        return response.status_code, f"Cart {cart_id} deleted"

    # Order Management Methods
    def get_orders(self, shop_id: str, api_key: str, query: dict = None) -> list:
        """Get list of orders for a shop."""
        resource = f"shops/{shop_id}/orders"
        params = self._build_query_params(query)
        data = self.get_resource(resource=resource, api_key=api_key, params=params)
        return data if isinstance(data, list) else []

    def get_order(self, shop_id: str, order_id: str, api_key: str) -> dict:
        """Get single order details."""
        resource = f"shops/{shop_id}/orders/{order_id}"
        data = self.get_resource(resource=resource, api_key=api_key)
        return data

    def create_order(self, shop_id: str, order_data: dict, api_key: str) -> tuple[int, dict]:
        """Create new order."""
        resource = f"shops/{shop_id}/orders"
        url = self.generate_resource_url(resource)
        headers = self.generate_auth_headers(api_key)
        response = requests.post(url=url, headers=headers, json=order_data)
        validate_get_response(response=response)
        response_data = response.json() if response.content else {}
        return response.status_code, response_data

    def update_order(self, shop_id: str, order_id: str, order_data: dict, api_key: str) -> tuple[int, dict]:
        """Update existing order."""
        resource = f"shops/{shop_id}/orders/{order_id}"
        url = self.generate_resource_url(resource)
        headers = self.generate_auth_headers(api_key)
        response = requests.post(url=url, headers=headers, json=order_data)
        validate_get_response(response=response)
        response_data = response.json() if response.content else {}
        return response.status_code, response_data

    def delete_order(self, shop_id: str, order_id: str, api_key: str) -> tuple[int, str]:
        """Delete order."""
        resource = f"shops/{shop_id}/orders/{order_id}"
        url = self.generate_resource_url(resource)
        headers = self.generate_auth_headers(api_key)
        response = requests.delete(url=url, headers=headers)
        validate_get_response(response=response)
        return response.status_code, "Order deleted"

    # Custom Field Methods
    def get_custom_fields(self, api_key: str, query_params: dict = None) -> tuple[int, list]:
        """
        Get list of custom fields.

        Args:
            api_key: GetResponse API key
            query_params: Optional query parameters (e.g., {"query[name]": "field_name"})

        Returns:
            Tuple of (status_code, list of custom fields)
        """
        resource = "custom-fields"
        url = self.generate_resource_url(resource)
        headers = self.generate_auth_headers(api_key)
        response = requests.get(url=url, headers=headers, params=query_params or {})
        validate_get_response(response=response)
        response_data = response.json() if response.content else []
        return response.status_code, response_data

    def create_custom_field(self, custom_field_data: dict, api_key: str) -> tuple[int, dict]:
        """
        Create new custom field.

        Args:
            custom_field_data: Custom field payload
                {
                    "name": "customer_type",
                    "type": "string",
                    "format": "text",
                    "hidden": "false",
                    "values": []
                }
            api_key: GetResponse API key

        Returns:
            Tuple of (status_code, response_data)
        """
        resource = "custom-fields"
        url = self.generate_resource_url(resource)
        headers = self.generate_auth_headers(api_key)
        response = requests.post(url=url, headers=headers, json=custom_field_data)
        validate_get_response(response=response)
        response_data = response.json() if response.content else {}
        return response.status_code, response_data

    def upsert_contact_custom_fields(self, contact_id: str, custom_fields_data: dict, api_key: str) -> tuple[int, dict]:
        """
        Upsert custom fields for a contact.

        Args:
            contact_id: GetResponse contact ID
            custom_fields_data: Payload with customFieldValues
                {
                    "customFieldValues": [
                        {"customFieldId": "abc", "value": ["new"]},
                        {"customFieldId": "def", "value": ["5"]}
                    ]
                }
            api_key: GetResponse API key

        Returns:
            Tuple of (status_code, response_data)
        """
        resource = f"contacts/{contact_id}/custom-fields"
        url = self.generate_resource_url(resource)
        headers = self.generate_auth_headers(api_key)
        response = requests.post(url=url, headers=headers, json=custom_fields_data)
        validate_get_response(response=response)
        response_data = response.json() if response.content else {}
        return response.status_code, response_data
