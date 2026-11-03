from django.urls import path
from . import views


urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("proyectos/", views.lista_proyectos, name="lista_proyectos"),
    path("proyectos/<int:proyecto_id>/tareas/", views.tareas_de_proyecto, name="tareas_de_proyecto"),
    path("tareas/<int:tarea_id>/usuarios/", views.usuarios_de_tarea, name="usuarios_de_tarea"),
    path("tareas/observaciones/<str:texto>/", views.tareas_por_observacion, name="tareas_por_observacion"),
    path("tareas/completadas/<int:anio_inicio>/<int:anio_fin>/", views.tareas_completadas_entre_anios, name="tareas_completadas_entre_anios"),
    path("proyectos/<int:proyecto_id>/ultimo-comentarista/", views.ultimo_usuario_comentarista, name="ultimo_usuario_comentarista"),
    path("tareas/<int:tarea_id>/comentarios/<str:palabra>/<int:anio>/", views.comentarios_por_palabra_y_anio, name="comentarios_por_palabra_y_anio"),
    path("proyectos/<int:proyecto_id>/etiquetas/", views.etiquetas_de_proyecto, name="etiquetas_de_proyecto"),
    path("usuarios/sin-tareas/", views.usuarios_sin_tareas_asignadas, name="usuarios_sin_tareas_asignadas"),
]