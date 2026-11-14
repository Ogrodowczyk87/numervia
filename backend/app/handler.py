"""AWS Lambda entry point: app.handler.handler (HTTP payload version 2.0)."""

from mangum import Mangum

from app.main import app


def handler(event, context):
    # Constructing Mangum also restores the event loop when a previous caller
    # closed it. Python 3.14 no longer creates a loop implicitly.
    # There are currently no startup/shutdown resources in this application.
    return Mangum(app, lifespan="off")(event, context)
