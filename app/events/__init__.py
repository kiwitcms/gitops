"""
Convert trigger event payload into a Python object with
somewhat defined interface!
"""

# Copyright (c) 2024 Alexander Todorov <atodorov@otb.bg>
#
# Licensed under GNU Affero General Public License v3 or later (AGPLv3+)
# https://www.gnu.org/licenses/agpl-3.0.html

# pylint: disable=missing-function-docstring

import os

from app.vendors import github


def load():
    """
    Create a Python object from the execution environment or fail.
    """
    if os.environ.get("GITHUB_ACTIONS") == "true":
        return github.GitHubEvent(os.environ["GITHUB_EVENT_PATH"])

    raise RuntimeError("Unsupported environment")
