from django.contrib.auth import decorators
from django.views.decorators.http import require_http_methods


def permission_required(perm, raise_exception=True):
    """Require a request's user to hold certain permissions."""
    return decorators.permission_required(
        perm,
        login_url=None,
        raise_exception=raise_exception,
    )


require_GET_POST = require_http_methods(["GET", "POST"])
require_GET_POST.__doc__ = "Require a view to only accepts GET and POST methods."
