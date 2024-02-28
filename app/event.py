"""
Load payload from GitHub, GitLab, Azure DevOps, etc
"""

#
# Copyright (c) 2024 Alexander Todorov <atodorov@otb.bg>
#
# Licensed under the AGPL-3.0: https://www.gnu.org/licenses/agpl-3.0.html
#

import json
import os


def load():
    """
    Sanity check the calling environment and load event payload.
    """
    if os.environ.get("GITHUB_ACTIONS") == "true":
        return GitHubEvent(os.environ["GITHUB_EVENT_PATH"])

    raise RuntimeError("Unsupported environment")


class TriggerEvent:
    private = True

    def __init__(self, file_path):
        with open(file_path, "r", encoding="utf-8") as event_file:
            self.payload = json.loads(event_file.read())


class GitHubEvent(TriggerEvent):
    def __init__(self, file_path):
        super().__init__(file_path)
        self.private = self.payload["repository"]["private"]

        if self.private:
            raise RuntimeError(
                "See https://kiwitcms.org/#subscriptions for running against private repositories!"
            )
