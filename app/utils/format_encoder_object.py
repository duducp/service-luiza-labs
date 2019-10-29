from datetime import datetime
from uuid import UUID

from bson import ObjectId


def format_encoder_object(o):
    if type(o) in (ObjectId, UUID):
        return str(o)
    elif type(o) == datetime:
        return o.isoformat()
    return o
