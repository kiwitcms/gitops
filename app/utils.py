"""
Utility functions!
"""
#
# Copyright (c) 2024 Alexander Todorov <atodorov@otb.bg>
#
# Licensed under the AGPL-3.0: https://www.gnu.org/licenses/agpl-3.0.html
#


def strtobool(val):
    """Convert a string representation of truth to True or False."""
    val = val.lower()
    if val in ("y", "yes", "t", "true", "on", "1"):
        return True

    if val in ("n", "no", "f", "false", "off", "0"):
        return False

    raise ValueError(f"invalid truth value `{val}`")
