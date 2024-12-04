"""Item management functionality for Bitwarden to KeePass conversion.

Provides classes and functions for handling different types of Bitwarden items
when converting them to KeePass entries.
"""

from enum import IntEnum
from urllib.parse import parse_qsl, urlsplit


class ItemType(IntEnum):
    """Enumeration of Bitwarden item types.

    Attributes:
        LOGIN: Login credentials
        SECURE_NOTE: Secure note
        CARD: Credit/debit card
        IDENTITY: Identity information
    """

    LOGIN = 1
    SECURE_NOTE = 2
    CARD = 3
    IDENTITY = 4


class CustomFieldType(IntEnum):
    """Enumeration of Bitwarden custom field types.

    Attributes:
        TEXT: Plain text field
        HIDDEN: Hidden/masked field
        BOOLEAN: Boolean/checkbox field
    """

    TEXT = 0
    HIDDEN = 1
    BOOLEAN = 2


class Item:
    """Wrapper for Bitwarden vault items.

    Provides methods to access and format item data for conversion to KeePass.
    """

    def __init__(self, item):
        """Initialize a new item wrapper.

        Args:
            item: Raw Bitwarden item data
        """
        self.item = item

    def get_id(self) -> str:
        """Get item's unique identifier.

        Returns:
            Bitwarden item ID
        """
        return self.item["id"]

    def get_name(self) -> str:
        """Get item's display name.

        Returns:
            Item name/title
        """
        return self.item["name"]

    def get_folder_id(self) -> str:
        """Get ID of folder containing this item.

        Returns:
            Bitwarden folder ID
        """
        return self.item["folderId"]

    def get_username(self) -> str:
        """Get username for login items.

        Returns:
            Username string or empty string if not a login
        """
        if "login" not in self.item:
            return ""

        return self.item["login"]["username"] if self.item["login"]["username"] else ""

    def get_password(self) -> str:
        """Get password for login items.

        Returns:
            Password string or empty string if not a login
        """
        if "login" not in self.item:
            return ""

        return self.item["login"]["password"] if self.item["login"]["password"] else ""

    def get_notes(self):
        """Get item's notes field.

        Returns:
            Notes text
        """
        return self.item["notes"]

    def get_uris(self):
        """Get URIs associated with login items.

        Returns:
            List of URI objects
        """
        if "login" not in self.item or "uris" not in self.item["login"]:
            return []

        for uri in self.item["login"]["uris"]:
            uri["uri"] = uri["uri"] if uri["uri"] is not None else ""

        return self.item["login"]["uris"]

    def get_custom_fields(self):
        """Get item's custom fields.

        Returns:
            List of custom field objects
        """
        if "fields" not in self.item:
            return []

        for field in self.item["fields"]:
            field["name"] = field["name"] if field["name"] is not None else ""
            field["value"] = field["value"] if field["value"] is not None else ""
            field["type"] = CustomFieldType(field["type"])

        return self.item["fields"]

    def get_attachments(self):
        """Get item's attachments.

        Returns:
            List of attachment objects
        """
        if "attachments" not in self.item:
            return []

        return self.item["attachments"]

    def get_totp(self):
        """Get TOTP configuration for login items.

        Returns:
            Tuple of (secret, settings) or (None, None) if not configured
        """
        if "login" not in self.item:
            return None, None

        if not self.item["login"]["totp"]:
            return None, None

        params = urlsplit(self.item["login"]["totp"]).query
        params = dict(parse_qsl(params))
        period = params.get("period", 30)
        digits = params.get("digits", 6)
        secret = params.get("secret", self.item["login"]["totp"])

        return secret, f"{period};{digits}"
