import json

import pytest

from app.handler import handler


@pytest.mark.parametrize(
    "method,path,body,expected",
    [
        ("GET", "/api/v1/health", None, 200),
        ("POST", "/api/v1/mortgage/simulate", {}, 422),
        (
            "POST",
            "/api/v1/mortgage/simulate",
            {
                "principal": "180000",
                "annual_interest_rate": "4.5",
                "term_years": 25,
                "monthly_overpayment": "200",
                "currency": "GBP",
            },
            200,
        ),
    ],
)
def test_lambda_payload_v2_uses_real_application(method, path, body, expected):
    event = {
        "version": "2.0",
        "rawPath": path,
        "rawQueryString": "",
        "headers": {
            "host": "example.lambda-url.eu-west-2.on.aws",
            "content-type": "application/json",
            "x-forwarded-proto": "https",
        },
        "requestContext": {
            "http": {
                "method": method,
                "path": path,
                "sourceIp": "127.0.0.1",
                "protocol": "HTTP/1.1",
            }
        },
        "body": json.dumps(body) if body is not None else None,
        "isBase64Encoded": False,
    }
    response = handler(event, {})
    assert response["statusCode"] == expected
    data = json.loads(response["body"])
    if path.endswith("health"):
        assert data == {"status": "ok"}
    elif expected == 200:
        assert data["baseline"]["months_to_payoff"] == 300
        assert data["with_overpayment"]["months_to_payoff"] == 221
