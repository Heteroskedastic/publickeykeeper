import os
import sys

from datetime import datetime

from sqlalchemy.orm import exc
from werkzeug.exceptions import abort


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, datetime):
        serial = obj.isoformat()
        return serial
    raise TypeError("Type not serializable")

sys.path.insert(0, os.path.dirname(os.path.abspath(os.path.dirname(__file__))))


def get_object_or_404(model, *criterion):
    try:
        rv = model.query.filter(*criterion).one()
    except (exc.NoResultFound, exc.MultipleResultsFound):
        abort(404)
    else:
        return rv
