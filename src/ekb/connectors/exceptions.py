"""Connector exceptions."""


class ConnectorError(Exception):
    """Base exception for all connectors."""


class RemoteServiceError(ConnectorError):
    """Remote service returned an unexpected response."""


class ResourceNotFoundError(ConnectorError):
    """Requested legal resource does not exist."""