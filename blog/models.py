from django.conf import settings
from django.db import models 
from django.utils import timezone

# Create your models here.


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
    
    # RELACIÓN: Un proyecto tiene un usuario creador/administrador (Uno a Muchos)
    creador = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='proyectos_creados')
    
    # RELACIÓN: Un usuario puede estar en varios proyectos y un proyecto tener varios usuarios (Muchos a Muchos)
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
    estado = models.CharField(max_length=3, choices=ESTADO_CHOICES, default="PEN") # Se cambió max_length a 3 para coincidir con los códigos 'PEN', 'PRO', 'COM'
    fecha_creacion = models.DateField()
    hora_vencimiento = models.TimeField()
    completada = models.BooleanField(default=False)

    # RELACIÓN: Un proyecto tiene varias tareas (Uno a Muchos)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name='tareas')
    
    # RELACIÓN: Muchas tareas pueden ser creadas por un usuario (Uno a Muchos)
    creador = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='tareas_creadas')
    
    # RELACIÓN: Una tarea puede tener varias etiquetas y viceversa (Muchos a Muchos)
    etiquetas = models.ManyToManyField(Etiqueta, related_name='tareas', blank=True)
    
    # RELACIÓN: Tarea a Usuarios usando una TABLA INTERMEDIA personalizada (Asignacion_tarea)
    usuarios_asignados = models.ManyToManyField(Usuario, through='Asignacion_tarea', related_name='tareas_asignadas')

    def __str__(self):
        return self.titulo


# ==========================================
# 5. MODELO TABLA INTERMEDIA (Asignación de Tarea)
# ==========================================
class Asignacion_tarea(models.Model):
    # Campos relacionales obligatorios de la tabla intermedia
    tarea = models.ForeignKey(Tarea, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    
    # Tus campos adicionales existentes
    observaciones = models.TextField(max_length=150)
    fecha_asignacion = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.usuario.nombre} asignado a {self.tarea.titulo}"


# ==========================================
# 6. MODELO COMENTARIO
# ==========================================
class Comentario(models.Model):
    contenido = models.TextField(max_length=150)
    fecha_comentario = models.DateTimeField()
    
    # RELACIÓN: Cada comentario tiene un autor (Uno a Muchos)
    autor = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='comentarios')
    
    # RELACIÓN: Cada comentario está asociado a una tarea (Uno a Muchos)
    tarea = models.ForeignKey(Tarea, on_delete=models.CASCADE, related_name='comentarios')

    def __str__(self):
        return f"Comentario de {self.autor.nombre} en {self.tarea.titulo}"

