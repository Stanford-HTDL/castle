__author__ = "Richard Correro (richard@richardcorrero.com)"

import random
import string
from typing import Optional


def generate_uid(uid_len: Optional[int] = 12):
    uid: str = ''.join(
        random.SystemRandom().choice(
            string.ascii_lowercase + string.digits
        ) for _ in range(uid_len)
    )

    return uid
