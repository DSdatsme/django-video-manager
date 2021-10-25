
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=56)),
                ('size', models.BigIntegerField(default=0)),
                ('path', models.CharField(default='', max_length=120)),
                ('duration', models.DecimalField(decimal_places=3, default=models.DecimalField(verbose_name=0.0), max_digits=20)),
                ('codec', models.CharField(default='', max_length=120)),
                ('container', models.CharField(default='', max_length=120)),
            ],
        ),
    ]
