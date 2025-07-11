from django.http import JsonResponse
from django.db import connection

from django.db.utils import OperationalError

def health_check(request):
    # Default values
    db_status = "ok"

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")  # lightweight check
            cursor.fetchone()
    except OperationalError:
        db_status = "unhealthy"

    return JsonResponse({
        "status": "ok",
        "database": db_status,
    })
