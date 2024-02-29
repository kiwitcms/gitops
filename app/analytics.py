"""
Anonymous analytics via Plausible.io
"""

#
# Copyright (c) 2024 Alexander Todorov <atodorov@otb.bg>
#
# Licensed under the AGPL-3.0: https://www.gnu.org/licenses/agpl-3.0.html
#

import os
from http import HTTPStatus

import requests
from app.utils import strtobool
from app.version import __version__


def analyze(event_id):
    """
    Decorator for collecting analytics for cli functions.
    @analyze("git/rebase")
    """

    def decorator(function):
        def wrapper(*args, **kwargs):
            post(event_id)

            return function(*args, **kwargs)

        return wrapper

    return decorator


def post(event_id):
    """
    Collect anonymous analytics via Plausible.io

    event_id - str - similar to a page URL, e.g. `pull_request_comment`
    referrer - str - e.g. https://github.com
    run_id - str or int - individual run id needed to count unique events
    """
    if not strtobool(os.environ.get("INPUT_ANONYMOUS-ANALYTICS", "true")):
        return

    run_id = os.environ["GITHUB_RUN_ID"]
    referrer = os.environ["GITHUB_SERVER_URL"]

    response = requests.post(
        "https://plausible.io/api/event",
        json={
            "name": "pageview",
            "url": f"app://kiwitcms-gitops/{event_id}",
            "referrer": referrer,
            "domain": "kiwitcms-gitops",
            "props": {
                "version": __version__,
            },
        },
        headers={
            "User-Agent": f"kiwitcms-gitops/{__version__}.{run_id}",
            "Content-Type": "application/json",
        },
        timeout=10,
    )

    if response.status_code not in [HTTPStatus.OK, HTTPStatus.ACCEPTED]:
        raise RuntimeError(
            f"Plausible.io returned {response.status_code} with \n {response.text}"
        )
