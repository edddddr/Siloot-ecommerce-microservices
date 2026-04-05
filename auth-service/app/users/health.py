from django.db import connection
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import serializers
import logging

logger = logging.getLogger(__name__)

class HealthCheckView(APIView):
    permission_classes = [] # Ensure K8s can reach this without a token
    authentication_classes = [] 

    @extend_schema(
        summary="Service Health Check",
        description="Checks if the service and its database are operational.",
        responses={
            200: inline_serializer(
                name='HealthSuccess',
                fields={'status': serializers.CharField(), 'database': serializers.CharField()}
            ),
            503: inline_serializer(
                name='HealthFailure',
                fields={'status': serializers.CharField(), 'error': serializers.CharField()}
            )
        }
    )
    def get(self, request):
        health_data = {"status": "ok", "database": "connected"}
        
        try:
            # Quick check to see if the DB is alive
            connection.ensure_connection()
            return Response(health_data, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.critical("Health check failed: Database unreachable", extra={"error": str(e)})
            return Response(
                {"status": "unhealthy", "error": "Database connection failed"}, 
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )