"""
GitHub specific functionality!
"""

# Copyright (c) 2024 Alexander Todorov <atodorov@otb.bg>
#
# Licensed under GNU Affero General Public License v3 or later (AGPLv3+)
# https://www.gnu.org/licenses/agpl-3.0.html

# pylint: disable=missing-function-docstring

import os

import github
from app.vendors import TriggerEvent


class GitHubEvent(TriggerEvent):
    comment = None

    def __init__(self, file_path):
        super().__init__(file_path)

        self.api = github.Github(
            auth=github.Auth.Token(os.environ["INPUT_TOKEN"]),
            base_url=os.environ["GITHUB_API_URL"],
        )

        if (
            os.environ.get("GITHUB_SERVER_URL", "") != "https://github.com"
            or self.private
        ) and not self.can_run(self.payload["repository"]["html_url"]):
            raise RuntimeError(
                "See https://kiwitcms.org/#subscriptions for running against private repositories!"
            )

        self.repository = github.Repository.Repository(
            self.api._Github__requester,  # pylint: disable=protected-access
            {},
            self.payload["repository"],
            completed=False,
        )
        self.pr = self.repository.get_pull(self.payload["issue"]["number"])

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
            return self.comment.body.strip().lower().split()

        raise RuntimeError("unrecognized command argument")

    def create_reaction(self, reaction):
        self.comment.create_reaction(reaction)

    def quote_reply(self, text):
        response = f"""> {self.comment.body}

```
{text}
```"""

        self.pr.as_issue().create_comment(response)
