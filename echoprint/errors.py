"""Errors raised by EchoPrint, so callers can tell a bad file from a bug."""

class EchoPrintError(Exception):
    """Base class for all EchoPrint errors."""


class AudioError(EchoPrintError):
    """The audio file could not be read, or is empty / silent."""


class DatabaseError(EchoPrintError):
    """The fingerprint database could not be loaded or saved."""


class TrackNotFoundError(EchoPrintError):
    """A requested track id is not in the library / database."""
