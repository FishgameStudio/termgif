"""Linux recording backend.

Currently the public API from this package is the fallback `record_window` function.
"""

from .record_win import record_window

__all__ = ["record_window"]
