# Creación de URLs, Vistas y QuerySets

## 1. Descripción de la actividad

En esta actividad se desarrolla una aplicación de gestión de tareas mediante la creación de diferentes URLs y vistas que permiten consultar información de los modelos de la aplicación.

El objetivo es trabajar con las consultas ORM de Django, los filtros, las relaciones entre modelos, la ordenación de resultados y la optimización de consultas.

También se trabaja con la organización de plantillas HTML mediante herencia y la creación de páginas de error personalizadas.

## 2. Ejercicios realizados

### Ejercicio 1. Página de inicio

Se crea una página principal con enlaces para acceder a los diferentes ejercicios de la actividad.

### Ejercicio 2. Mostrar todos los proyectos

**URL:** `/proyectos/`

Se muestran todos los proyectos almacenados en la base de datos, incluyendo sus datos y el nombre de su creador.

Se utiliza `select_related('creador')` para optimizar la consulta y evitar consultas adicionales al recuperar los datos del creador.

### Ejercicio 3. Tareas de un proyecto

**URL:** `/proyectos/<proyecto_id>/tareas/`

Se muestran todas las tareas pertenecientes a un proyecto determinado.

Los resultados se ordenan por fecha de creación descendente mediante `order_by('-fecha_creacion')`.

### Ejercicio 4. Usuarios asignados a una tarea

**URL:** `/tareas/<tarea_id>/usuarios/`

Se muestran los usuarios asignados a una tarea, junto con su fecha de asignación y observaciones.

Los resultados se ordenan por fecha de asignación ascendente.

Se utiliza `select_related('usuario')` para optimizar la consulta.

### Ejercicio 5. Tareas por observaciones

**URL:** `/tareas/observaciones/<texto>/`

Se obtienen las tareas cuyas observaciones de asignación contienen el texto indicado en la URL.

Se utiliza `icontains` para realizar búsquedas sin distinguir entre mayúsculas y minúsculas y `distinct()` para evitar resultados duplicados.

### Ejercicio 6. Tareas completadas entre dos años

**URL:** `/tareas/completadas/<anio_inicio>/<anio_fin>/`

Se muestran las tareas cuyo estado sea completado y cuya fecha de creación esté comprendida entre los dos años indicados.

Se utilizan los filtros `range` y `estado='COM'`.

### Ejercicio 7. Último usuario comentarista de un proyecto

**URL:** `/proyectos/<proyecto_id>/ultimo-comentarista/`

Se obtiene el comentario más reciente realizado en cualquiera de las tareas de un proyecto.

Se utiliza `order_by('-fecha_comentario').first()` para recuperar el último comentario y mostrar los datos de su autor.

### Ejercicio 8. Comentarios por palabra y año

**URL:** `/tareas/<tarea_id>/comentarios/<palabra>/<anio>/`

Se obtienen los comentarios de una tarea cuyo contenido comienza por la palabra indicada y que pertenecen al año especificado.

Se utilizan los filtros `istartswith` y `year`.

### Ejercicio 9. Etiquetas de un proyecto

**URL:** `/proyectos/<proyecto_id>/etiquetas/`

Se muestran las etiquetas utilizadas en las tareas de un proyecto determinado.

Se utiliza `distinct()` para evitar que aparezcan etiquetas repetidas.

### Ejercicio 10. Usuarios sin tareas asignadas

**URL:** `/usuarios/sin-tareas/`

Se muestran los usuarios que no tienen ninguna tarea asignada.

Se utiliza `isnull=True` sobre la relación inversa `tareas_asignadas`.

### Ejercicio 11. Páginas de error personalizadas

Se crean cuatro plantillas para gestionar los siguientes errores:

- `400.html`: solicitud incorrecta.
- `403.html`: acceso prohibido.
- `404.html`: página no encontrada.
- `500.html`: error interno del servidor.

Estas páginas mantienen la estructura y el diseño general de la aplicación.

## 3. Consultas ORM utilizadas

Durante la actividad se han utilizado diferentes métodos y filtros del ORM de Django:

| Método o filtro | Utilidad |
|---|---|
| `all()` | Obtener todos los registros. |
| `filter()` | Filtrar registros según condiciones. |
| `order_by()` | Ordenar los resultados. |
| `first()` | Obtener el primer resultado. |
| `distinct()` | Evitar registros duplicados. |
| `select_related()` | Optimizar consultas de relaciones ForeignKey. |
| `range` | Filtrar valores comprendidos entre dos límites. |
| `icontains` | Buscar texto sin distinguir mayúsculas y minúsculas. |
| `istartswith` | Buscar textos que comienzan por una palabra. |
| `isnull` | Comprobar si una relación está vacía. |
| `year` | Filtrar fechas por año. |

## 4. Optimización de consultas

Durante el desarrollo se ha utilizado Django Debug Toolbar para comprobar el número de consultas SQL realizadas en cada vista.

Se detectaron consultas adicionales al acceder a información de modelos relacionados.

Para mejorar el rendimiento se incorporó `select_related()` en los ejercicios 2 y 4.

Ejemplo del ejercicio 2:

```python
proyectos = Proyecto.objects.select_related('creador').all()
```

Ejemplo del ejercicio 4:

```python
usuarios = Asignacion_tarea.objects.filter(tarea_id=tarea_id).select_related('usuario').order_by('fecha_asignacion')
```

Estas modificaciones permiten recuperar los objetos relacionados mediante una misma consulta SQL, reduciendo las consultas adicionales.

## 5. Consultas SQL RAW

Como alternativa a las consultas ORM, se han incluido consultas SQL RAW comentadas en las vistas.

Se utiliza el método `raw()` para realizar consultas SQL directamente sobre la base de datos.

Estas consultas se mantienen comentadas y no se ejecutan durante el funcionamiento normal de la aplicación.

El acceso principal a los datos se realiza mediante el ORM de Django.

## 6. Plantillas HTML y herencia

Todas las plantillas se encuentran dentro de:

```text
blog/templates/blog/
```

Se ha creado una plantilla principal llamada `base.html`, que contiene la estructura común de todas las páginas:

- Cabecera.
- Menú de navegación.
- Contenido principal.
- Pie de página.
- Estilos CSS generales.

Las demás plantillas utilizan la herencia mediante:

```django
{% extends 'blog/base.html' %}
```

Para introducir el contenido específico de cada página se utiliza el bloque:

```django
{% block content %}
    <!-- Contenido de cada página -->
{% endblock %}
```

### Ventajas de la herencia

- Evita repetir la misma estructura HTML.
- Facilita el mantenimiento del código.
- Permite modificar el diseño general desde un único archivo.
- Mantiene una apariencia común en todas las páginas.

## 7. Organización de los estilos CSS

Los estilos generales se encuentran definidos dentro de la etiqueta `<style>` de `base.html`.

De esta manera, todas las plantillas que heredan de la plantilla principal comparten automáticamente los mismos estilos.

Se han definido estilos para:

- Cabecera y navegación.
- Contenedores.
- Tablas de resultados.
- Tarjetas.
- Botones y enlaces.
- Mensajes informativos.
- Páginas de error.
- Pie de página.

Al centralizar los estilos en `base.html`, cualquier modificación del diseño general se aplica automáticamente al resto de páginas.

## 8. Ejecución de la actividad

Para ejecutar la aplicación:

```bash
python manage.py migrate
python manage.py runserver
```

La página principal estará disponible en:

```text
http://127.0.0.1:8000/
```


**Nota:** La base de datos local está excluida del repositorio mediante `.gitignore`. Por tanto, para comprobar los resultados de los ejercicios será necesario disponer de registros de prueba relacionados entre los diferentes modelos.

## 9. Conclusión

En esta actividad se han trabajado las relaciones entre modelos, las consultas ORM, los filtros y la ordenación de resultados.

También se ha mejorado el rendimiento de determinadas consultas mediante `select_related()` y se ha organizado la presentación de las páginas utilizando herencia de plantillas y estilos CSS compartidos.