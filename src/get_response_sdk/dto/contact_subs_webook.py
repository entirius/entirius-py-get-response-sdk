# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from marshmallow_dataclass import add_schema, dataclass


@add_schema
@dataclass
class Campaign:
    campaignId: str
    name: str
    href: str


@add_schema
@dataclass
class Contact:
    contactId: str
    email: str
    name: str
    campaign: Campaign
    ip: str
    origin: str
    href: str


@add_schema
@dataclass
class Account:
    accountId: str


@add_schema
@dataclass
class Event:
    occurredAt: str


@add_schema
@dataclass
class ContactAddedEvent:
    type: str
    contact: Contact
    account: Account
    event: Event


# https://apidocs.getresponse.com/v3/payloads#contact-subscribed
# json_data = {
#     "type": "contact_added",
#     "contact": {
#         "contactId": "abc123",
#         "email": "example@example.com",
#         "name": "Friend",
#         "campaign": {
#             "campaignId": "bcd234",
#             "name": "my_first_campaign",
#             "href": "https://api.getresponse.com/v3/campaigns/bcd234"
#         },
#         "ip": "1.2.3.4",
#         "origin": "api",
#         "href": "https://api.getresponse.com/v3/contacts/abc123"
#     },
#     "account": {
#         "accountId": "def456"
#     },
#     "event": {
#         "occurredAt": "2021-04-27T12:56:00+00:00"
#     }
# }
