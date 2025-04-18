
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Guest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=255)),
                ('position_with_company', models.CharField(max_length=255)),
                ('photo_url', models.URLField(blank=True, null=True)),
                ('linkedin_url', models.URLField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('category', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('event_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('register_deadline', models.DateTimeField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('slots', models.PositiveIntegerField()),
                ('register_link', models.URLField()),
                ('status', models.CharField(choices=[('UPCOMING', 'Upcoming'), ('ONGOING', 'Ongoing'), ('PAST', 'Past'), ('CANCELLED', 'Cancelled')], max_length=20)),
                ('photos', models.JSONField(blank=True, default=list)),
                ('guests', models.ManyToManyField(related_name='events', to='events.guest')),
            ],
        ),
    ]
