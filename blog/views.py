from django.shortcuts import render, get_object_or_404
from datetime import date
from .models import Proyecto, Tarea, Usuario, Asignacion_tarea, Comentario, Etiqueta


# EJERCICIO 1: Página de inicio
def inicio(request):
    return render(request, 'blog/inicio.html', {})


# EJERCICIO 2: Mostrar todos los proyectos
def lista_proyectos(request):
    proyectos = Proyecto.objects.select_related('creador').all()
    # SQL RAW:
    # proyectos = Proyecto.objects.raw("SELECT p.*, u.id AS creador_id FROM blog_proyecto p JOIN blog_usuario u ON p.creador_id = u.id")
    return render(request, 'blog/proyectos.html', {'datos': proyectos})


# EJERCICIO 3: Mostrar las tareas de un proyecto ordenadas por fecha
def tareas_de_proyecto(request, proyecto_id):
    tareas = Tarea.objects.filter(proyecto_id=proyecto_id).order_by('-fecha_creacion')
    # SQL RAW:
    # tareas = Tarea.objects.raw("SELECT * FROM blog_tarea WHERE proyecto_id = %s ORDER BY fecha_creacion DESC", [proyecto_id])
    return render(request, 'blog/tareas_proyecto.html', {'datos': tareas})


# EJERCICIO 4: Mostrar los usuarios asignados a una tarea ordenados por fecha
def usuarios_de_tarea(request, tarea_id):
    usuarios = Asignacion_tarea.objects.filter(tarea_id=tarea_id).select_related('usuario').order_by('fecha_asignacion')
    # SQL RAW:
    # usuarios = Asignacion_tarea.objects.raw("SELECT a.*, u.id AS usuario_id FROM blog_asignacion_tarea a JOIN blog_usuario u ON a.usuario_id = u.id WHERE a.tarea_id = %s ORDER BY a.fecha_asignacion ASC", [tarea_id])
    return render(request, 'blog/usuarios_tarea.html', {'datos': usuarios})


# EJERCICIO 5: Mostrar tareas que tengan un texto en las observaciones
def tareas_por_observacion(request, texto):
    tareas = Tarea.objects.filter(asignacion_tarea__observaciones__icontains=texto).distinct()
    # SQL RAW:
    # tareas = Tarea.objects.raw("SELECT DISTINCT t.* FROM blog_tarea t JOIN blog_asignacion_tarea a ON t.id = a.tarea_id WHERE LOWER(a.observaciones) LIKE LOWER(%s)", ['%' + texto + '%'])
    return render(request, 'blog/tareas_observaciones.html', {'datos': tareas})


# EJERCICIO 6: Mostrar tareas completadas entre dos años
def tareas_completadas_entre_anios(request, anio_inicio, anio_fin):
    tareas = Tarea.objects.filter(fecha_creacion__range=(date(anio_inicio, 1, 1), date(anio_fin, 12, 31)), estado='COM')
    # SQL RAW:
    # tareas = Tarea.objects.raw("SELECT * FROM blog_tarea WHERE fecha_creacion BETWEEN %s AND %s AND estado = %s", [date(anio_inicio, 1, 1), date(anio_fin, 12, 31), 'COM'])
    return render(request, 'blog/tareas_completadas.html', {'datos': tareas})


# EJERCICIO 7: Mostrar el último usuario que ha comentado en un proyecto
def ultimo_usuario_comentarista(request, proyecto_id):
    comentario = Comentario.objects.filter(tarea__proyecto_id=proyecto_id).order_by('-fecha_comentario').first()
    # SQL RAW:
    # usuario = Usuario.objects.raw("SELECT u.* FROM blog_usuario u JOIN blog_comentario c ON u.id = c.autor_id JOIN blog_tarea t ON c.tarea_id = t.id WHERE t.proyecto_id = %s ORDER BY c.fecha_comentario DESC LIMIT 1", [proyecto_id])
    return render(request, 'blog/ultimo_comentarista.html', {'datos': [comentario] if comentario else []})


# EJERCICIO 8: Mostrar comentarios que empiezan por una palabra y son de un año concreto
def comentarios_por_palabra_y_anio(request, tarea_id, palabra, anio):
    comentarios = Comentario.objects.filter(tarea_id=tarea_id, contenido__istartswith=palabra, fecha_comentario__year=anio)
    # SQL RAW:
    # comentarios = Comentario.objects.raw("SELECT * FROM blog_comentario WHERE tarea_id = %s AND LOWER(contenido) LIKE LOWER(%s) AND fecha_comentario >= %s AND fecha_comentario < %s", [tarea_id, palabra + '%', date(anio, 1, 1), date(anio + 1, 1, 1)])
    return render(request, 'blog/comentarios.html', {'datos': comentarios})


# EJERCICIO 9: Mostrar todas las etiquetas utilizadas en las tareas de un proyecto
def etiquetas_de_proyecto(request, proyecto_id):
    etiquetas = Etiqueta.objects.filter(tareas__proyecto_id=proyecto_id).distinct()
    # SQL RAW:
    # etiquetas = Etiqueta.objects.raw("SELECT DISTINCT e.* FROM blog_etiqueta e JOIN blog_tarea_etiquetas te ON e.id = te.etiqueta_id JOIN blog_tarea t ON te.tarea_id = t.id WHERE t.proyecto_id = %s", [proyecto_id])
    return render(request, 'blog/etiquetas.html', {'datos': etiquetas})


# EJERCICIO 10: Mostrar usuarios que no tienen tareas asignadas
def usuarios_sin_tareas_asignadas(request):
    usuarios = Usuario.objects.filter(tareas_asignadas__isnull=True).distinct()
    # SQL RAW:
    # usuarios = Usuario.objects.raw("SELECT u.* FROM blog_usuario u LEFT JOIN blog_asignacion_tarea a ON u.id = a.usuario_id WHERE a.id IS NULL")
    return render(request, 'blog/usuarios_sin_tareas.html', {'datos': usuarios})


# EJERCICIO 11: Páginas de error
def error_400(request, exception):
    return render(request, 'blog/400.html', {}, status=400)


def error_403(request, exception):
    return render(request, 'blog/403.html', {}, status=403)


def error_404(request, exception):
    return render(request, 'blog/404.html', {}, status=404)


def error_500(request):
    return render(request, 'blog/500.html', {}, status=500)