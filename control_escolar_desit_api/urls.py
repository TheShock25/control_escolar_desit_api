from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views.bootstrap import VersionView
from . import viewss
from control_escolar_desit_api.viewss import users
from control_escolar_desit_api.viewss import alumnos
from control_escolar_desit_api.viewss import maestros
from control_escolar_desit_api.viewss import materias
from control_escolar_desit_api.viewss import estadisticas
from control_escolar_desit_api.viewss import auth
from control_escolar_desit_api.viewss import bootstrap

urlpatterns = [
    #Create Admin
        path('admin/', users.AdminView.as_view()),
    #Admin Data
        path('lista-admins/', users.AdminAll.as_view()),
    #Edit Admin
        #path('admins-edit/', users.AdminsViewEdit.as_view())
     #Create Alumno
        path('alumnos/', alumnos.AlumnosView.as_view()),

        path('lista-alumnos/', alumnos.AlumnosAll.as_view()),
    #Create Maestro
        path('maestros/', maestros.MaestrosView.as_view()),
    #Maestro Data
        path('lista-maestros/', maestros.MaestrosAll.as_view()),
    #Total Users
        path('total-usuarios/', users.TotalUsers.as_view()),

        path('materias/', materias.MateriasView.as_view()),
        
        path('lista-materias/', materias.MateriasAll.as_view()),

        path('estadisticas-usuarios/', estadisticas.EstadisticasUsuariosView.as_view()),

        path('estadisticas-materias/', estadisticas.EstadisticasMateriasView.as_view()),

        path('top-profesores/', estadisticas.TopProfesoresView.as_view()),

        path('distribucion-horarios/', estadisticas.DistribucionHorariosView.as_view()),
        
    #Login
        path('login/', auth.CustomAuthToken.as_view()),
    #Logout
        path('logout/', auth.Logout.as_view()),
        #tambien ignoren los siguientes. solo es para ver si corre el backend
        path('', viewss.home, name='home'),
    path('health/', viewss.health_check, name='health_check'),
    path('admin/', admin.site.urls),
        
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
