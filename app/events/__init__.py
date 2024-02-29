"""
Convert trigger event payload into a Python object with
somewhat defined interface!
"""

# pylint: disable=missing-function-docstring
#
# Copyright (c) 2024 Alexander Todorov <atodorov@otb.bg>
#
# Licensed under the AGPL-3.0: https://www.gnu.org/licenses/agpl-3.0.html
#

import os

from app.vendors import github


def load():
    """
    Create a Python object from the execution environment or fail.
    """
    if os.environ.get("GITHUB_ACTIONS") == "true":
        return github.GitHubEvent(os.environ["GITHUB_EVENT_PATH"])

    raise RuntimeError("Unsupported environment")
