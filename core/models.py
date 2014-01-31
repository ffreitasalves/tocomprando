from django.db import models
from django.contrib.auth.models import User

class Pedido(models.Model):
    user = models.ForeignKey(User)
    pedido = models.CharField(max_length=200)

    def __unicode__(self):
        return unicode(self.pedido)

    def nro_cotacoes(self):
        return 1