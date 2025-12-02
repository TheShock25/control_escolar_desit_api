#este archivo ignorenlo, solo es para probar que el backend funciona en el link
# En control_escolar_desit_api/views.py
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone
from django.db import connection

@api_view(['GET'])
def home(request):
    """Endpoint raíz"""
    return Response({
        "service": "Control Escolar API",
        "status": "online",
        "version": "1.0.0",
        "documentation": "API REST para sistema de control escolar",
        "endpoints": {
            "health": "/health/",
            "admin": "/admin/",
            "api": "/api/",
        },
        "frontend": "https://control-escolar-desit-webapp-64p8.vercel.app",
        "timestamp": timezone.now().isoformat()
    })

@api_view(['GET'])
def health_check(request):
    """Verificación de salud del servicio"""
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT version()")
            db_version = cursor.fetchone()
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"
        db_version = None
    
    return Response({
        "status": "healthy",
        "service": "Control Escolar API",
        "database": {
            "status": db_status,
            "engine": "PostgreSQL",
            "version": db_version[0] if db_version else "unknown"
        },
        "environment": "production",
        "timestamp": timezone.now().isoformat()
    })