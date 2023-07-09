from datetime import datetime
from django.db import models
from .utils import calcula_total

# Create your models here.


class Categoria(models.Model):
    categoria = models.CharField(max_length=50)
    essencial = models.BooleanField(default=False)
    valor_planejamento = models.FloatField(default=0)

    def __str__(self):
        return self.categoria

    def total_gasto(self):
        from extrato.models import Valores
        valores = Valores.objects.filter(categoria__id=self.id).filter(
            data__month=datetime.now().month).filter(tipo='S')

        total_valor = calcula_total(valores, 'valor')

        return total_valor

    def calcula_percentual_gasto_por_categoria(self):
        # Adicione o try para evitar o ZeroDivisionError (Erro de divisão por zero)
        try:
            return int((self.total_gasto() * 100) / self.valor_planejamento)
        except:
            return 0


class Conta(models.Model):
    lista_bancos = (
        ('BB', 'Banco do Brasil'),
        ('Bradesco', 'Banco Bradesco'),
        ('Caixa', 'Caixa Econômica Federal'),
        ('Itaú', 'Itaú Unibanco'),
        ('Santander', 'Banco Santander'),
        ('Safra', 'Banco Safra'),
        ('Votorantim', 'Banco Votorantim'),
        ('Inter', 'Banco Inter'),
        ('Original', 'Banco Original'),
        ('BNB', 'Banco do Nordeste'),
        ('Nubank', 'Nu Pagamentos S.A.'),
        ('Stone', 'Stone Pagamentos S.A.'),
        ('Neon', 'Banco Neon S.A.'),
        ('Sicredi', 'Sicredi'),
        ('C6 Bank', 'C6 Bank'),
        ('Topázio', 'Banco Topázio'),
        ('Next', 'Banco Next'),
        ('Modal', 'Banco Modal'),
        ('Bradesco BBI', 'Banco Bradesco BBI'),
        ('Brasil Plural', 'Brasil Plural')
    )

    tipo_choices = (
        ('pf', 'Pessoa Física'),
        ('pj', 'Pessoa Jurídica'),
    )

    apelido = models.CharField(max_length=50)
    banco = models.CharField(max_length=50, choices=lista_bancos)
    tipo = models.CharField(max_length=2, choices=tipo_choices)
    valor = models.FloatField()
    icone = models.ImageField(upload_to='icones')

    def __str__(self):
        return self.apelido
