# Práctica: Tarea de Creación de Modelos e Integridad de Datos

Este repositorio contiene la resolución práctica para el escenario de una **Aplicación de Gestión de Tareas y Proyectos Cooperativos** implementada en **Django 6**. Contiene la definición de modelos relacionales avanzados, tablas intermedias personalizadas, corrección de restricciones de base de datos y la carga inicial de datos de prueba mediante fixtures.

---

## 📖 1. Escenario y Requisitos del Sistema

El sistema representa una plataforma web donde los usuarios administran proyectos, asignan tareas de forma unívoca o compartida, clasifican elementos mediante etiquetas y colaboran insertando comentarios. 

### 🗂️ Entidades y Restricciones Solicitadas:
*   **Usuario:** Identificador único por correo electrónico y marcas temporales de registro.
*   **Proyecto:** Planificación temporal de objetivos con un Administrador/Creador único y un equipo de colaboradores adjuntos.
*   **Tarea:** Ciclos de vida controlados por estados (`Pendiente`, `Progreso`, `Completada`), hora estricta de vencimiento y prioridad numérica.
*   **Etiqueta:** Indexación por términos semánticos únicos.
*   **Asignación de Tarea:** Historial explícito de auditoría del flujo de trabajo de los operarios.
*   **Comentario:** Hilo de discusión conversacional anidado por tarea.

---

## 🛠️ 2. Arquitectura de Modelos (`blog/models.py`)

Se han implementado las relaciones solicitadas mediante claves foráneas (`ForeignKey`), relaciones muchos-a-muchos (`ManyToManyField`) y la declaración de la tabla intermedia explícita `Asignacion_tarea` usando el atributo `through`.

```python
from django.conf import settings
from django.db import models 
from django.utils import timezone

# ==========================================
# 1. MODELO USUARIO
# ==========================================
class Usuario(models.Model):
    nombre = models.CharField(max_length=50)
    correo = models.EmailField(max_length=50, unique=True)
    contraseña = models.CharField(max_length=128)
    fecha_registro = models.DateTimeField()

    def __str__(self):
        return self.nombre


# ==========================================
# 2. MODELO PROYECTO
# ==========================================
class Proyecto(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField(max_length=150)
    duracion_estimada = models.FloatField()
    fecha_inicio = models.DateField()
    fecha_finalizacion = models.DateField()
    
    # RELACIÓN: Creador/Administrador (Uno a Muchos)
    creador = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='proyectos_creados')
    
    # RELACIÓN: Colaboradores del proyecto (Muchos a Muchos)
    colaboradores = models.ManyToManyField(Usuario, related_name='proyectos_asignados', blank=True)

    def __str__(self):
        return self.nombre


# ==========================================
# 3. MODELO ETIQUETA
# ==========================================
class Etiqueta(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre


# ==========================================
# 4. MODELO TAREA
# ==========================================
class Tarea(models.Model):
    ESTADO_CHOICES = [
        ("PEN", "Pendiente"),
        ("PRO", "Progreso"),
        ("COM", "Completada"),
    ]   

    titulo = models.CharField(max_length=50)
    descripcion = models.TextField(max_length=150)
    prioridad = models.IntegerField()
    estado = models.CharField(max_length=3, choices=ESTADO_CHOICES, default="PEN")
    fecha_creacion = models.DateField()
    hora_vencimiento = models.TimeField()
    completada = models.BooleanField(default=False)

    # RELACIÓN: Un proyecto tiene varias tareas (Uno a Muchos)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name='tareas')
    
    # RELACIÓN: Tarea creada por un usuario (Uno a Muchos)
    creador = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='tareas_creadas')
    
    # RELACIÓN: Etiquetas de la tarea (Muchos a Muchos)
    etiquetas = models.ManyToManyField(Etiqueta, related_name='tareas', blank=True)
    
    # RELACIÓN: Tarea a Usuarios usando TABLA INTERMEDIA personalizada
    usuarios_asignados = models.ManyToManyField(Usuario, through='Asignacion_tarea', related_name='tareas_asignadas')

    def __str__(self):
        return self.titulo


# ==========================================
# 5. MODELO TABLA INTERMEDIA (Asignación de Tarea)
# ==========================================
class Asignacion_tarea(models.Model):
    tarea = models.ForeignKey(Tarea, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    observaciones = models.TextField(max_length=150)
    
    # Ajuste crítico: null=True, blank=True para compatibilidad con librerías externas de Seeding
    fecha_asignacion = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.usuario.nombre} asignado a {self.tarea.titulo}"


# ==========================================
# 6. MODELO COMENTARIO
# ==========================================
class Comentario(models.Model):
    contenido = models.TextField(max_length=150)
    fecha_comentario = models.DateTimeField()
    
    # RELACIÓN: Autor del comentario (Uno a Muchos)
    autor = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='comentarios')
    
    # RELACIÓN: Tarea asociada (Uno a Muchos)
    tarea = models.ForeignKey(Tarea, on_delete=models.CASCADE, related_name='comentarios')

    def __str__(self):
        return f"Comentario de {self.autor.nombre} en {self.tarea.titulo}"
```

---

## ⚙️ 3. Guía de Despliegue y Activación del Entorno

Sigue los siguientes comandos secuenciales en la terminal para limpiar las restricciones del sistema global (PEP 668) y levantar el entorno de desarrollo:

### 1. Preparar el Entorno Virtual Limpio
```bash
# Desactivar entornos corruptos previos si los hubiera
deactivate 2>/dev/null

# Crear y activar el entorno virtual local 'venv'
python3 -m venv venv
source venv/bin/activate
```

### 2. Instalar las Dependencias obligatorias
```bash
# Instalar el listado de requisitos del proyecto
pip install -r requirements.txt
```

### 3. Aplicar Migraciones Estructurales
```bash
python manage.py makemigrations
python manage.py migrate
```

---

## 📊 4. Generación Automática de Datos (Seeder)

Para cumplir con el requerimiento de poblar **30 registros distribuidos por cada tabla**, se utiliza la librería `django-seed`.

> **Nota de Integridad:** Se modificó el campo `fecha_asignacion` del modelo `Asignacion_tarea` a `null=True` debido a que el motor automático del Seeder no es capaz de computar marcas de tiempo aleatorias concurrentes en tablas pivote manuales, lanzando una excepción `NOT NULL constraint failed`.

Comando de ejecución del generador:
```bash
python manage.py seed blog --number=30
```

---

## 💾 5. Copias de Seguridad y Restauración con Fixtures

El estado consolidado de la base de datos se almacena en ficheros serialization JSON que guardan las dependencias cruzadas e índices semánticos en perfecto orden en español.

El archivo está ubicado en `blog/Fixtures/datos.json`.

### Comandos de Operación:

*   **Cargar la copia de seguridad de la práctica :**
    ```bash
    python manage.py loaddata datos.json
    ```
*   **Generar un nuevo volcado/respaldo (Backup manual):**
    ```bash
    python manage.py dumpdata blog --indent=2 > blog/Fixtures/backup_actual.json
    ```

---