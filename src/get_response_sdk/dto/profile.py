# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from dataclasses import dataclass

from get_response_sdk.dto import DTO


@dataclass
class Profile(DTO):
    email: str
    phone: str | None = None
    area_code: str | None = None
    agreements: dict | None = None
    uuid: str | None = None
