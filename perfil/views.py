from django.shortcuts import render, redirect
from django.db.models import Sum
from extrato.models import Valores
from .models import Conta, Categoria
from django.contrib import messages
from django.contrib.messages import constants
from .utils import calcula_total, calcula_equilibrio_financeiro
from datetime import datetime

# Create your views here.


def home(request):
    contas = Conta.objects.all().order_by('-valor')
    total_contas = calcula_total(contas, 'valor')

    entradas = Valores.objects.filter(tipo='E')
    total_entradas = calcula_total(entradas, 'valor')

    saidas = Valores.objects.filter(tipo='S')
    total_saidas = calcula_total(saidas, 'valor')

    entradas_mes = Valores.objects.filter(
        data__month=datetime.now().month).filter(tipo='E')
    saidas_mes = Valores.objects.filter(
        data__month=datetime.now().month).filter(tipo='S')
    total_entradas_mes = calcula_total(entradas_mes, 'valor')
    total_saidas_mes = calcula_total(saidas_mes, 'valor')

    saldo_mes = total_entradas_mes - total_saidas_mes

    percentual_gastos_essenciais, percentual_gastos_nao_essenciais = calcula_equilibrio_financeiro()

    return render(request, 'perfil/home.html', {'contas': contas, 'total_contas': total_contas, 'total_entradas': total_entradas, 'total_saidas': total_saidas, 'total_saidas_mes': total_saidas_mes, 'total_entradas_mes': total_entradas_mes, 'saldo_mes': saldo_mes, 'percentual_gastos_essenciais': int(percentual_gastos_essenciais), 'percentual_gastos_nao_essenciais': int(percentual_gastos_nao_essenciais)})


def gerenciar(request):
    contas = Conta.objects.all().order_by('-valor')
    categorias = Categoria.objects.all().order_by('-essencial', 'categoria')
    # total_contas = contas.aggregate(Sum('valor'))
    total_contas = calcula_total(contas, 'valor')

    lista_bancos = Conta.lista_bancos

    print(total_contas)
    return render(request, 'perfil/gerenciar.html', {'contas': contas, 'total_contas': total_contas, 'categorias': categorias, 'lista_bancos': lista_bancos})


def cadastrar_banco(request):
    apelido = request.POST.get('apelido')
    banco = request.POST.get('banco')
    tipo = request.POST.get('tipo')
    valor = float(str(request.POST.get('valor')).replace(',', '.'))
    icone = request.FILES.get('icone')

    if len(apelido.strip()) == 0 or valor == "0":
        messages.add_message(request, constants.ERROR,
                             'Preencha todos os campos')
        return redirect('/perfil/gerenciar/')

    if not apelido.strip():
        messages.add_message(request, constants.ERROR,
                             'O apelido não pode ser vazio ou conter apenas espaços')
        return redirect('/perfil/gerenciar/')

    if Conta.objects.filter(apelido=apelido).exists():
        messages.add_message(request, constants.ERROR,
                             'O apelido já está sendo utilizado. Por favor, escolha outro')
        return redirect('/perfil/gerenciar/')

    conta = Conta(
        apelido=apelido,
        banco=banco,
        tipo=tipo,
        valor=valor,
        icone=icone
    )

    conta.save()
    messages.add_message(request, constants.SUCCESS,
                         'Conta cadastrada com sucesso')
    return redirect('/perfil/gerenciar/')


def deletar_banco(request, id):
    conta = Conta.objects.get(id=id)
    conta.delete()

    messages.add_message(request, constants.SUCCESS,
                         'Conta removida com sucesso')
    return redirect('/perfil/gerenciar/')


def cadastrar_categoria(request):
    categoria = request.POST.get('categoria')
    essencial = bool(request.POST.get('essencial'))

    if not categoria.strip():
        messages.add_message(request, constants.ERROR,
                             'Erro! A categoria não pode ser vazia ou conter apenas espaços')
        return redirect('/perfil/gerenciar/')

    if Categoria.objects.filter(categoria=categoria).exists():
        messages.add_message(request, constants.INFO,
                             'Essa categoria já está cadastrada')
        return redirect('/perfil/gerenciar/')

    categoria = Categoria(
        categoria=categoria,
        essencial=essencial
    )

    categoria.save()

    messages.add_message(request, constants.SUCCESS,
                         'Categoria cadastrada com sucesso')
    return redirect('/perfil/gerenciar/')


def update_categoria(request, id):
    categoria = Categoria.objects.get(id=id)

    categoria.essencial = not categoria.essencial

    categoria.save()

    messages.add_message(request, constants.INFO,
                         'Categoria alterada')

    return redirect('/perfil/gerenciar/')
    # return render(request, 'perfil/gerenciar.html')


def dashboard(request):
    dados = {}
    categorias = Categoria.objects.all()

    for categoria in categorias:
        dados[categoria.categoria] = Valores.objects.filter(
            categoria=categoria).aggregate(Sum('valor'))['valor__sum']

    return render(request, 'perfil/dashboard.html', {'labels': list(dados.keys()), 'values': list(dados.values())})
