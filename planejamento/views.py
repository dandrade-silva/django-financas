from django.shortcuts import render, redirect
from perfil.models import Categoria
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib import messages
from django.contrib.messages import constants

# Create your views here.


def definir_planejamento(request):
    categorias = Categoria.objects.all()

    return render(request, 'planejamento/definir_planejamento.html', {'categorias': categorias})


@csrf_exempt
def update_valor_categoria(request, id):
    novo_valor = json.load(request)['novo_valor']
    categoria = Categoria.objects.get(id=id)
    categoria.valor_planejamento = novo_valor
    categoria.save()

    return JsonResponse({'Status': 'Sucesso'})


def ver_planejamento(request):
    categorias = Categoria.objects.all()

    return render(request, 'planejamento/ver_planejamento.html', {'categorias': categorias})
