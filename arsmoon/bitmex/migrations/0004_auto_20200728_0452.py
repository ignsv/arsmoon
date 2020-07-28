# Generated by Django 3.0.8 on 2020-07-28 04:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bitmex', '0003_clientaccountcounter_task_id'),
    ]

    def add_dump_task_ids(apps, schema):
        ClientAccountCounter = apps.get_model('bitmex', 'ClientAccountCounter')

        for counter in ClientAccountCounter.objects.all():
            counter.task_id = 'dumpy'
            counter.save()

    def reverse_add_dump_task_ids(apps, schema):
        pass

    operations = [
        migrations.RunPython(add_dump_task_ids, reverse_code=reverse_add_dump_task_ids),
        migrations.AlterField(
            model_name='clientaccountcounter',
            name='task_id',
            field=models.CharField(help_text='Maximum length is 255 symbols', max_length=255, verbose_name='Task_id'),
        ),
    ]