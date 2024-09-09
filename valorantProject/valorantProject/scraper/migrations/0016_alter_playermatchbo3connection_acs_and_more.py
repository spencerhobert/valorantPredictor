# Generated by Django 5.1.1 on 2024-09-09 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0015_alter_playermatchbo3connection_kast_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playermatchbo3connection',
            name='acs',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='playermatchbo3connection',
            name='adr',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='playermatchbo3connection',
            name='assists',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='playermatchbo3connection',
            name='deaths',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='playermatchbo3connection',
            name='fd',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='playermatchbo3connection',
            name='fk',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='playermatchbo3connection',
            name='fkfd',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='playermatchbo3connection',
            name='hsp',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='playermatchbo3connection',
            name='kd',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='playermatchbo3connection',
            name='kills',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='playermatchbo5connection',
            name='acs',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='playermatchbo5connection',
            name='adr',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='playermatchbo5connection',
            name='assists',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='playermatchbo5connection',
            name='deaths',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='playermatchbo5connection',
            name='fd',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='playermatchbo5connection',
            name='fk',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='playermatchbo5connection',
            name='fkfd',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='playermatchbo5connection',
            name='hsp',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='playermatchbo5connection',
            name='kd',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='playermatchbo5connection',
            name='kills',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
