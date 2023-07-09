# Generated by Django 4.2.3 on 2023-07-09 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("perfil", "0002_alter_conta_banco_alter_conta_tipo"),
    ]

    operations = [
        migrations.AlterField(
            model_name="conta",
            name="banco",
            field=models.CharField(
                choices=[
                    ("CA", "Carteira"),
                    ("BB", "Banco do Brasil"),
                    ("Bradesco", "Banco Bradesco"),
                    ("Caixa", "Caixa Econômica Federal"),
                    ("Itaú", "Itaú Unibanco"),
                    ("Santander", "Banco Santander"),
                    ("Safra", "Banco Safra"),
                    ("Votorantim", "Banco Votorantim"),
                    ("Inter", "Banco Inter"),
                    ("Original", "Banco Original"),
                    ("BNB", "Banco do Nordeste"),
                    ("Nubank", "Nu Pagamentos S.A."),
                    ("Stone", "Stone Pagamentos S.A."),
                    ("Neon", "Banco Neon S.A."),
                    ("Sicredi", "Sicredi"),
                    ("C6 Bank", "C6 Bank"),
                    ("Topázio", "Banco Topázio"),
                    ("Next", "Banco Next"),
                    ("Modal", "Banco Modal"),
                    ("Bradesco BBI", "Banco Bradesco BBI"),
                    ("Brasil Plural", "Brasil Plural"),
                ],
                max_length=50,
            ),
        ),
    ]