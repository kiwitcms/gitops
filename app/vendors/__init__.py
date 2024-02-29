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

import json


class TriggerEvent:
    """
    Represents an event which was triggered via comment, push, etc.
    Details for specific environments should be implemented in overriden
    classes.
    """

    argv = []
    private = True

    def __init__(self, file_path):
        with open(file_path, "r", encoding="utf-8") as event_file:
            self.payload = json.loads(event_file.read())
