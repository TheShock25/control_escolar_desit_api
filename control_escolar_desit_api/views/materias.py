from django.db.models import *
from django.db import transaction
from control_escolar_desit_api.serializers import MateriaSerializer
from control_escolar_desit_api.models import Materias
from rest_framework import permissions
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
import json
from django.shortcuts import get_object_or_404

class MateriasAll(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    
    def get(self, request, *args, **kwargs):
        materias = Materias.objects.all().order_by("id")
        lista = MateriaSerializer(materias, many=True).data
        
        # Procesar dias_json para convertirlo de string a lista
        for materia in lista:
            if isinstance(materia, dict) and "dias_json" in materia:
                try:
                    materia["dias_json"] = json.loads(materia["dias_json"])
                except Exception:
                    materia["dias_json"] = []
        
        return Response(lista, 200)

class MateriasView(generics.CreateAPIView):
    def get_permissions(self):
        if self.request.method in ['GET', 'PUT', 'DELETE']:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated()]  
    
    # Obtener materia por ID
    def get(self, request, *args, **kwargs):
        materia = get_object_or_404(Materias, id=request.GET.get("id"))
        materia_data = MateriaSerializer(materia, many=False).data
        
        # Procesar dias_json
        if isinstance(materia_data, dict) and "dias_json" in materia_data:
            try:
                materia_data["dias_json"] = json.loads(materia_data["dias_json"])
            except Exception:
                materia_data["dias_json"] = []
        
        return Response(materia_data, 200)
    
    # Registrar nueva materia
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        try:
            # Verificar si el NRC ya existe
            nrc_existente = Materias.objects.filter(nrc=request.data["nrc"]).first()
            if nrc_existente:
                return Response({"message": "El NRC ya existe en la base de datos"}, 400)
            
            # Crear la materia
            materia = Materias.objects.create(
                nrc=request.data["nrc"],
                nombre=request.data["nombre"],
                seccion=request.data["seccion"],
                dias_json=json.dumps(request.data["dias_json"]),
                hora_inicio=request.data["hora_inicio"],
                hora_final=request.data["hora_final"],
                salon=request.data["salon"],
                programa_educativo=request.data["programa_educativo"],
                profesor_asignado_id=request.data.get("profesor_asignado"),
                creditos=request.data["creditos"]
            )
            materia.save()
            
            return Response({"materia_created_id": materia.id}, 201)
            
        except Exception as e:
            return Response({"message": f"Error al crear la materia: {str(e)}"}, 400)
    
    # Actualizar materia
    @transaction.atomic
    def put(self, request, *args, **kwargs):
        try:
            materia = get_object_or_404(Materias, id=request.data["id"])
            if "nrc" in request.data:
                nrc_existente = Materias.objects.filter(nrc=request.data["nrc"]).exclude(id=request.data["id"]).first()
                if nrc_existente:
                    return Response({"message": "El NRC ya existe en la base de datos"}, 400)
            
            materia.nrc = request.data.get("nrc", materia.nrc)
            materia.nombre = request.data.get("nombre", materia.nombre)
            materia.seccion = request.data.get("seccion", materia.seccion)
            materia.dias_json = json.dumps(request.data.get("dias_json", []))
            materia.hora_inicio = request.data.get("hora_inicio", materia.hora_inicio)
            materia.hora_final = request.data.get("hora_final", materia.hora_final)
            materia.salon = request.data.get("salon", materia.salon)
            materia.programa_educativo = request.data.get("programa_educativo", materia.programa_educativo)
            materia.profesor_asignado_id = request.data.get("profesor_asignado")
            materia.creditos = request.data.get("creditos", materia.creditos)
            
            materia.save()
            
            return Response({"message": "Materia actualizada correctamente"}, 200)
            
        except Exception as e:
            return Response({"message": f"Error al actualizar la materia: {str(e)}"}, 400)
    
    # Eliminar materia
    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        materia = get_object_or_404(Materias, id=request.GET.get("id"))
        try:
            materia.delete()
            return Response({"details": "Materia eliminada"}, 200)
        except Exception as e:
            return Response({"details": f"Error al eliminar la materia: {str(e)}"}, 400)