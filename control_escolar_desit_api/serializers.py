from django.contrib.auth.models import User
from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('id','first_name','last_name', 'email')

class AdminSerializer(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)
    class Meta:
        model = Administradores
        fields = '__all__'
        
class AlumnoSerializer(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)
    class Meta:
        model = Alumnos
        fields = "__all__"

class MaestroSerializer(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)
    class Meta:
        model = Maestros
        fields = '__all__'

class MateriaSerializer(serializers.ModelSerializer):
    profesor_info = serializers.SerializerMethodField()
    
    class Meta:
        model = Materias
        fields = '__all__'
    
    def get_profesor_info(self, obj):
        if obj.profesor_asignado:
            return {
                'id': obj.profesor_asignado.id,
                'nombre': f"{obj.profesor_asignado.user.first_name} {obj.profesor_asignado.user.last_name}"
            }
        return None