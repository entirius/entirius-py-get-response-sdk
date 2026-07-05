# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from requests import Response


def validate_get_response(response: Response) -> (bool, dict):
    try:
        response_body = response.json()
    except Exception:
        response_body = response.text

    if response.status_code == 200:
        return True, response_body

    if response.status_code == 201:
        return True, response_body

    if response.status_code == 302:
        return True, response_body

    if response.status_code == 400:
        validation, error_message = validate_get_response_body_when_error(response_body)
        if validation:
            raise ValueError(error_message)
        else:
            raise ValueError("Unknown message in 400 HTTP CODE")

    if response.status_code == 401:
        validation, error_message = validate_get_response_body_when_error(response_body)
        if validation:
            raise ConnectionError(error_message)

    if response.status_code == 404:
        validation, error_message = validate_get_response_body_when_error(response_body)
        if validation:
            raise ValueError(error_message)

    if response.status_code == 429:
        validation, error_message = validate_get_response_body_when_error(response_body)
        if validation:
            raise TimeoutError(error_message)

    return False, response_body


def validate_get_response_body_when_error(response_body: dict):
    if "httpStatus" in response_body:
        error_message = response_body.get("message")
        if error_message is None:
            error_message = "An undefined problem was encountered"

        # Include context if available for detailed error info
        context = response_body.get("context")
        if context:
            error_message = f"{error_message}. Context: {context}"

        return True, f"{error_message}"
    return False, ""
