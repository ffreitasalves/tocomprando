#coding: utf-8
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import login as authlogin, authenticate
from django.contrib.auth.decorators import login_required
from models import Pedido, Empresa, Pagamento
from django.core.mail import send_mail
from django.utils.encoding import smart_unicode
import logging

def index(request):
    return render_to_response(
        'index.html',
        locals(),
        context_instance = RequestContext(request),
    )

def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']

        new_user = User.objects.create_user(email,email,password)
        new_user.first_name = first_name
        new_user.last_name = last_name
        new_user.save()

        user = authenticate(username=email, password=password)
        authlogin(request, user)

        return HttpResponseRedirect(reverse('home'))

    return render_to_response(
        'index.html',
        locals(),
        context_instance = RequestContext(request),
    )

def login(request):
    if request.method == 'POST':
        username = request.POST['email']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                authlogin(request, user)
                return HttpResponseRedirect(reverse('home'))

    return render_to_response(
        'registration/login.html',
        locals(),
        context_instance = RequestContext(request),
    )

@login_required
def order(request):
    order = request.GET.get('order')
    if order:
        new_order = Pedido(user = request.user, pedido = order)
        new_order.save()

    return HttpResponseRedirect(reverse('panel'))

@login_required
def remove_order(request,id):
    order = get_object_or_404(Pedido,id=id,user=request.user)
    order.delete()

    return HttpResponseRedirect(reverse('panel'))

@login_required
def panel(request):
    pedidos = Pedido.objects.filter(user=request.user)

    return render_to_response(
        'painel.html',
        locals(),
        context_instance = RequestContext(request),
    )

def contact(request):
    if request.method == 'POST':
        try:
            send_mail(
                u"[ToComprando]Contato pelo site", #titulo
                u"""
                Mensagem Enviada pelo Site do ToComprando\n
                Nome: %s\n
                Email: %s\n
                Mensagem: %s
                """ % (
                   smart_unicode(request.POST.get("name")),
                   smart_unicode(request.POST.get("email")),
                   smart_unicode(request.POST.get("message"))
                    ), #corpo
                'no-reply@doingcast.com', #quem envia
                ('contact@doingcast.com',), #quem recebe
            )
            msg = 'Mensagem enviada com sucesso'
        except:
            pass

    return render_to_response(
        'contact.html',
        locals(),
        context_instance = RequestContext(request),
    )

@login_required
def order_detail(request,id):
    order = get_object_or_404(Pedido,id=id,user=request.user)

    return render_to_response(
        'detail.html',
        locals(),
        context_instance = RequestContext(request),
    )

@login_required
def register_company(request):
    if request.method == 'POST':

        empresa = request.POST.get('empresa')
        cnpj = request.POST.get('cnpj')
        endereco = request.POST.get('endereco')
        telefone = request.POST.get('telefone')
        site = request.POST.get('site')

        new_company = Empresa.objects.create(
            empresa = empresa,
            cnpj = cnpj,
            endereco = endereco,
            telefone = telefone,
            site = site,
            user = request.user,
            ativo = False,
        )

        new_company.save()

        return HttpResponseRedirect(reverse('planos'))

    return render_to_response(
        'registration/register_company.html',
        locals(),
        context_instance = RequestContext(request),
    )

def planos(request):

    return render_to_response(
        'planos.html',
        locals(),
        context_instance = RequestContext(request),
    )

@login_required
def plano_socio(request):

    import paypalrestsdk

    paypalrestsdk.configure({
      "mode": "sandbox", # sandbox or live
      "client_id": "AeHUbBChEO4KrVQAmsqDBcJ3eiEd-Hn-G5GpSwn3ilbNdFQnqC0_wMZfe9pP",
      "client_secret": "ELmLURA14iGL6IUh5y8XJLvVN8O_keUgCeFZwBBLR92rY98GQeMUJDqFTawe" })

    logging.basicConfig(level=logging.INFO)

    payment = paypalrestsdk.Payment({
      "intent": "sale",
      "payer": {
        "payment_method": "paypal",},
      "redirect_urls": {
        "return_url": "http://localhost:8000/ok",
        "cancel_url": "http://localhost:8000/cancel" },
      "transactions": [{
        "item_list": {
          "items": [{
            "name": "item",
            "sku": "item",
            "price": "350.00",
            "currency": "BRL",
            "quantity": 1 }]},
        "amount": {
          "total": "350.00",
          "currency": "BRL" },
        "description": u"ToComprando - Plano Sócio" }]})

    # Create Payment and return status
    novo_pagamento = Pagamento(user = request.user)
    if payment.create():
      print("Payment[%s] created successfully"%(payment.id))
      novo_pagamento.id_paypal = payment.id
      # Redirect the user to given approval url
      for link in payment.links:
        if link.method == "REDIRECT":
          redirect_url = link.href
          token = redirect_url[redirect_url.find('token=')+6:]
          novo_pagamento.token = token
          novo_pagamento.log = str(payment)
          novo_pagamento.save()
          return HttpResponseRedirect(redirect_url)
    else:
      print("Error while creating payment:")
      print(payment.error)
      novo_pagamento.log = str(payment)
      novo_pagamento.save()

    return render_to_response(
        'planos.html',
        locals(),
        context_instance = RequestContext(request),
    )

@login_required
def plano_mensal(request):

    import paypalrestsdk

    paypalrestsdk.configure({
      "mode": "sandbox", # sandbox or live
      "client_id": "AeHUbBChEO4KrVQAmsqDBcJ3eiEd-Hn-G5GpSwn3ilbNdFQnqC0_wMZfe9pP",
      "client_secret": "ELmLURA14iGL6IUh5y8XJLvVN8O_keUgCeFZwBBLR92rY98GQeMUJDqFTawe" })

    logging.basicConfig(level=logging.INFO)

    payment = paypalrestsdk.Payment({
      "intent": "sale",
      "payer": {
        "payment_method": "paypal",},
      "redirect_urls": {
        "return_url": "http://localhost:8000/ok",
        "cancel_url": "http://localhost:8000/cancel" },
      "transactions": [{
        "item_list": {
          "items": [{
            "name": "item",
            "sku": "item",
            "price": "350.00",
            "currency": "BRL",
            "quantity": 1 }]},
        "amount": {
          "total": "15.00",
          "currency": "BRL" },
        "description": u"ToComprando - Plano Mensal" }]})

    # Create Payment and return status
    novo_pagamento = Pagamento(user = request.user)
    if payment.create():
      print("Payment[%s] created successfully"%(payment.id))
      novo_pagamento.id_paypal = payment.id
      # Redirect the user to given approval url
      for link in payment.links:
        if link.method == "REDIRECT":
          redirect_url = link.href
          token = redirect_url[redirect_url.find('token=')+6:]
          novo_pagamento.token = token
          novo_pagamento.log = str(payment)
          novo_pagamento.save()
          return HttpResponseRedirect(redirect_url)
    else:
      print("Error while creating payment:")
      print(payment.error)
      novo_pagamento.log = str(payment)
      novo_pagamento.save()

    return render_to_response(
        'planos.html',
        locals(),
        context_instance = RequestContext(request),
    )

def ok(request):
    token = request.GET.get('token')
    payerid = request.GET.get('PayerID')

    import paypalrestsdk

    paypalrestsdk.configure({
      "mode": "sandbox", # sandbox or live
      "client_id": "AeHUbBChEO4KrVQAmsqDBcJ3eiEd-Hn-G5GpSwn3ilbNdFQnqC0_wMZfe9pP",
      "client_secret": "ELmLURA14iGL6IUh5y8XJLvVN8O_keUgCeFZwBBLR92rY98GQeMUJDqFTawe" })

    pagamento = get_object_or_404(Pagamento,token=token,user=request.user)
    payment = paypalrestsdk.Payment.find(pagamento.id_paypal)
    payment.execute({"payer_id": payerid})

    pagamento.payer_id = payerid
    pagamento.state = payment.state
    pagamento.log = str(payment)

    return render_to_response(
        'ok.html',
        locals(),
        context_instance = RequestContext(request),
    )

def cancel(request):
    token = request.GET.get('token')
    pagamento = get_object_or_404(Pagamento,token=token,user=request.user)
    pagamento.state = u'canceled'

    return render_to_response(
        'cancel.html',
        locals(),
        context_instance = RequestContext(request),
    )