from django.db.models import Count
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from control_escolar_desit_api.models import Administradores, Maestros, Alumnos, Materias, User
import logging

logger = logging.getLogger(__name__)

class EstadisticasUsuariosView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    
    def get(self, request, *args, **kwargs):
        try:
            total_admins = Administradores.objects.count()
            total_maestros = Maestros.objects.count()
            total_alumnos = Alumnos.objects.count()
            
            return Response({
                'administradores': total_admins,
                'maestros': total_maestros,
                'alumnos': total_alumnos,
                'total_usuarios': total_admins + total_maestros + total_alumnos
            }, 200)
        except Exception as e:
            return Response({"error": str(e)}, 400)

class EstadisticasMateriasView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    
    def get(self, request, *args, **kwargs):
        try:
            materias_por_programa = Materias.objects.values('programa_educativo').annotate(total=Count('id'))
            
            total_materias = Materias.objects.count()
            
            return Response({
                'total_materias': total_materias,
                'materias_por_programa': list(materias_por_programa),
            }, 200)
        except Exception as e:
            return Response({"error": str(e)}, 400)

class TopProfesoresView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    
    def get(self, request, *args, **kwargs):
        try:
            profesores_con_materias = Maestros.objects.annotate(
                total_materias=Count('materias')
            ).filter(total_materias__gt=0).order_by('-total_materias')[:5]
            
            top_profesores = []
            for profesor in profesores_con_materias:
                top_profesores.append({
                    'nombre': f"{profesor.user.first_name} {profesor.user.last_name}",
                    'total_materias': profesor.total_materias
                })
            
            return Response({
                'top_profesores': top_profesores
            }, 200)
        except Exception as e:
            return Response({"error": str(e)}, 400)

class DistribucionHorariosView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    
    def get(self, request, *args, **kwargs):
        try:
            rangos_horarios = {
                '07:00-09:00': 0,
                '09:00-11:00': 0,
                '11:00-13:00': 0,
                '13:00-15:00': 0,
                '15:00-17:00': 0,
                '17:00-19:00': 0,
                '19:00-21:00': 0
            }
            
            materias = Materias.objects.all()
            
            for materia in materias:
                if materia.hora_inicio:
                    hora = materia.hora_inicio.hour
                    
                    if 7 <= hora < 9:
                        rangos_horarios['07:00-09:00'] += 1
                    elif 9 <= hora < 11:
                        rangos_horarios['09:00-11:00'] += 1
                    elif 11 <= hora < 13:
                        rangos_horarios['11:00-13:00'] += 1
                    elif 13 <= hora < 15:
                        rangos_horarios['13:00-15:00'] += 1
                    elif 15 <= hora < 17:
                        rangos_horarios['15:00-17:00'] += 1
                    elif 17 <= hora < 19:
                        rangos_horarios['17:00-19:00'] += 1
                    elif 19 <= hora < 21:
                        rangos_horarios['19:00-21:00'] += 1
            
            return Response({
                'distribucion_horarios': rangos_horarios
            }, 200)
        except Exception as e:
            return Response({"error": str(e)}, 400)