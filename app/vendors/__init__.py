"""
Convert trigger event payload into a Python object with
somewhat defined interface!
"""

# Copyright (c) 2024 Alexander Todorov <atodorov@otb.bg>
#
# Licensed under GNU Affero General Public License v3 or later (AGPLv3+)
# https://www.gnu.org/licenses/agpl-3.0.html

# pylint: disable=missing-function-docstring

import json
import os

import click
from app.utils import strtobool


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
    stdout = []

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
        for line in self.stdout:
            click.echo(line)

        if strtobool(os.environ.get("INPUT_REPLY-TO-COMMENTS", "true")):
            self.quote_reply("\n".join(self.stdout))
        self.stdout = []

        if exc_type or exc_value or tb:
            self.create_reaction(self.reactions["end-failure"])
        else:
            self.create_reaction(self.reactions["end-success"])
