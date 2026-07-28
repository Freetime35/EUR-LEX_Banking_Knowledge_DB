class CellarClientError(Exception):
    """Base exception for Cellar client."""


class InvalidCelexError(CellarClientError):
    """Raised when a CELEX identifier is invalid."""


class NoticeDownloadError(CellarClientError):
    """Raised when a metadata notice cannot be downloaded."""