class BaseError(Exception):
    """Base error."""

    pass


class NegativeValueError(BaseError):
    """Value must be non-negative."""

    pass


class NonPositiveValueError(BaseError):
    """Value must be positive."""

    pass


class MinMaxError(BaseError):
    """Minimal price cannot be greater than Maximal price."""

    pass
