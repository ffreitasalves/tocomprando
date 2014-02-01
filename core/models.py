# coding: utf-8
from django.db import models
from django.contrib.auth.models import User

class Pedido(models.Model):
    user = models.ForeignKey(User)
    pedido = models.CharField(max_length=200)

    def __unicode__(self):
        return unicode(self.pedido)

    def nro_cotacoes(self):
        return 1

class Empresa(models.Model):
    PLANO_CHOICES = (
        ('Mensal','Mensal'),
        ('Unico','Unico'),
    )
    user = models.ForeignKey(User,unique=True)
    empresa = models.CharField(u'Nome da Empresa',max_length=200)
    cnpj = models.CharField('CNPJ',max_length=18,blank=True,null=True)
    endereco = models.CharField(u'Endereço',max_length=200,blank=True,null=True)
    telefone = models.CharField(u'Telefone',max_length=25)
    site = models.URLField(u'Site',blank=True,null=True)
    ativo = models.BooleanField()
    plano = models.CharField(max_length=200,choices=PLANO_CHOICES,blank=True,null=True)

    data_criacao = models.DateTimeField(auto_now_add=True)
    ultima_modificacao = models.DateTimeField(auto_now=True)

    data_expiracao = models.DateField(u'Data de Expiração do Plano',blank=True,null=True)

    def __unicode__(self):
        return unicode(self.empresa)

class Pagamento(models.Model):
    user = models.ForeignKey(User,unique=True)
    id_paypal = models.CharField(max_length=200,blank=True,null=True)
    token = models.CharField(max_length=200,blank=True,null=True)
    payer_id = models.CharField(max_length=200,blank=True,null=True)
    status = models.CharField(max_length=200,blank=True,null=True)
    log = models.TextField(blank=True,null=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    ultima_modificacao = models.DateTimeField(auto_now=True)