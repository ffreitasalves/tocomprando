from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import login as authlogin, authenticate
from django.contrib.auth.decorators import login_required
from models import Pedido, Empresa
from django.core.mail import send_mail
from django.utils.encoding import smart_unicode

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