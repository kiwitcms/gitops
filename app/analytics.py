"""
Anonymous analytics via Plausible.io
"""

# Copyright (c) 2024 Alexander Todorov <atodorov@otb.bg>
#
# Licensed under GNU Affero General Public License v3 or later (AGPLv3+)
# https://www.gnu.org/licenses/agpl-3.0.html

import math
import os
import time
from functools import wraps
from hashlib import sha256
from http import HTTPStatus

import click
import requests
from app.utils import strtobool
from app.version import __version__


def analyze(event_id):
    """
    Decorator for collecting analytics for cli functions.
    @analyze("git/rebase")
    """

    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            start = time.time()
            result = function(*args, **kwargs)
            duration_in_secs = math.ceil(time.time() - start)

            # record the analytics *after* a function is done
            post(event_id, duration_in_secs)
            return result

        return wrapper

    return decorator


def post(event_id, duration_in_secs):
    """
    Collect anonymous analytics via Plausible.io

    event_id - str - similar to a page URL, e.g. `pull_request_comment`
    duration_in_secs - int - rounded up duration of this event
    """
    if not strtobool(os.environ.get("INPUT_ANONYMOUS-ANALYTICS", "true")):
        if strtobool(os.environ.get("INPUT_DEBUG", "false")):
            click.echo(f"INFO: Anonymous analytics has been disabled for /{event_id}")
        return

    # this has to be unique b/c the IP address is fixed. Both together represent
    # a unique user ID for Plausible
    actor_id = int.from_bytes(
        sha256(
            os.environ.get("GITHUB_TRIGGERING_ACTOR", "").encode(),
            usedforsecurity=False,
        ).digest()
    )

    # Record only the domain name, not any specific paths
    referrer = os.environ["GITHUB_SERVER_URL"]

    # Plausible.io rejects GitHub's original IP address b/c it is listed as a
    # datacenter address and we don't have information about the actual address of the
    # user who triggered our application. Instead just use a public address that
    # isn't going to be rejected
    ip_address = "176.12.5.83"

    response = requests.post(
        "https://plausible.io/api/event",
        json={
            "name": "pageview",
            "url": f"app://kiwitcms-gitops/{event_id}",
            "referrer": referrer,
            "domain": "kiwitcms-gitops",
            "props": {
                "duration": duration_in_secs,
                "version": __version__,
                "repository_type": os.environ.get("_APP_REPOSITORY_TYPE"),
            },
        },
        headers={
            "User-Agent": f"kiwitcms-gitops/{actor_id}",
            "X-Forwarded-For": ip_address,
            "Content-Type": "application/json",
        },
        timeout=10,
    )

    if response.status_code not in [HTTPStatus.OK, HTTPStatus.ACCEPTED]:
        raise RuntimeError(
            f"Plausible.io returned {response.status_code} with \n {response.text}"
        )

    if strtobool(os.environ.get("INPUT_DEBUG", "false")):
        click.echo(f"INFO: Analytics for /{event_id}: {response.text}")
        click.echo(response.headers)
        click.echo("===== end =====")
