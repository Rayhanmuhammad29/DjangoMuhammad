# Generated migration file

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mahasiswa', '0003_dosen_alter_mahasiswa_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='matakuliah',
            name='mahasiswa',
            field=models.ManyToManyField(blank=True, related_name='matakuliah_list', to='mahasiswa.mahasiswa'),
        ),
    ]
