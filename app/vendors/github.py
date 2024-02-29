"""
GitHub specific functionality!
"""

# pylint: disable=missing-function-docstring
#
# Copyright (c) 2024 Alexander Todorov <atodorov@otb.bg>
#
# Licensed under the AGPL-3.0: https://www.gnu.org/licenses/agpl-3.0.html
#

import os

import github
import github.Auth
import github.IssueComment
from app.vendors import TriggerEvent


class GitHubEvent(TriggerEvent):
    comment = None

    def __init__(self, file_path):
        super().__init__(file_path)

        self.api = github.Github(
            auth=github.Auth.Token(os.environ["INPUT_TOKEN"]),
            base_url=os.environ["GITHUB_API_URL"],
        )

        if self.private:
            raise RuntimeError(
                "See https://kiwitcms.org/#subscriptions for running against private repositories!"
            )

    @property
    def private(self):
        return self.payload["repository"]["private"]

    @property
    def args(self):
        if "comment" in self.payload:
            self.comment = github.IssueComment.IssueComment(
                self.api._Github__requester,  # pylint: disable=protected-access
                {},
                self.payload["comment"],
                completed=True,
            )
            return self.comment.body.strip().split()

        raise RuntimeError("unrecognized command argument")
