from rest_framework.views import exception_handler
from rest_framework.response import Response

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        response.data = {
            "success": False,
            "status": response.status_code,
            "error": {
                "code": exc.__class__.__name__,
                "message": str(exc),
                "details": response.data  # muestra errores campo a campo
            }
        }
    else:
        # errores no controlados
        response = Response({
            "success": False,
            "status": 500,
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "Ocurrió un error inesperado"
            }
        }, status=500)

    return response