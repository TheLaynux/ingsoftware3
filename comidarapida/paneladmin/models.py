from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Producto(models.Model):
    categoria = models.CharField(max_length=100)
    nombre = models.CharField(max_length=200)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    image = models.ImageField(upload_to='productos/')

    def __str__(self):
        return self.nombre


class Perfil(models.Model):

    ROLES = [
        ('administrador', 'Administrador'),
        ('vendedor', 'Vendedor'),
    ]

    usuario = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    rol = models.CharField(
        max_length=20,
        choices=ROLES
    )

    def __str__(self):
        return f"{self.usuario.username} - {self.rol}"

class Venta(models.Model):

    vendedor = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    fecha = models.DateTimeField(
        auto_now_add=True
    )

    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    def __str__(self):
        return f"Venta #{self.id}"

class DetalleVenta(models.Model):

    venta = models.ForeignKey(
        Venta,
        on_delete=models.CASCADE,
        related_name='detalles'
    )

    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE
    )

    cantidad = models.PositiveIntegerField()

    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def __str__(self):
        return self.producto.nombre