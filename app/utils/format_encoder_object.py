from datetime import datetime
from uuid import UUID

from bson import ObjectId


def format_encoder_object(o):
    if type(o) == ObjectId:
        return str(o)
    elif type(o) == datetime:
        return o.isoformat()
    elif type(o) == UUID:
        return str(o)
    return o.__str__
