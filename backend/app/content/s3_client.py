
from functools import lru_cache
from typing import Any

import boto3
from botocore.config import Config


@lru_cache(maxsize=1)
def get_s3_client() -> Any:
    return boto3.client(
        "s3",
        config=Config(
            connect_timeout=2,
            read_timeout=3,
            retries={
                "mode": "standard",
                "total_max_attempts": 1,
            },
        ),
    )