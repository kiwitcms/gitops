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

    args = []
    private = True
    reactions = {
        "begin": "eyes",
        "end-success": "+1",
        "end-failure": "-1",
    }

    def __init__(self, file_path):
        with open(file_path, "r", encoding="utf-8") as event_file:
            self.payload = json.loads(event_file.read())

    def create_reaction(self, reaction):
        raise NotImplementedError

    def quote_reply(self, text):
        raise NotImplementedError

    def __enter__(self):
        """
        Executed when processing of a command begins
        """
        self.create_reaction(self.reactions["begin"])
        return self

    def __exit__(self, exc_type, exc_value, tb):
        """
        Executed when processing of a command ends
        """
        # todo: self.quote_reply() & determine pass/fail
        self.create_reaction(self.reactions["end-success"])
