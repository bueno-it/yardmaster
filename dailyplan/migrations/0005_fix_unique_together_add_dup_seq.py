from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dailyplan', '0004_dailyplan_flag_color'),
    ]

    operations = [
        # Step 1: Django's migration history thinks the unique_together is
        # still the old 3-column version, but the database was already
        # altered directly to the 4-column (…, row_order) version by a
        # migration whose file got lost on a container rebuild before it
        # was committed to git. This step only corrects Django's internal
        # state to match reality — it does NOT touch the database.
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.AlterUniqueTogether(
                    name='dailyplan',
                    unique_together={('date', 'store_id_raw', 'hb_bd', 'row_order')},
                ),
            ],
            database_operations=[],
        ),

        # Step 2: the real change we actually want — drop the row_order-based
        # constraint, add dup_seq, and create the dup_seq-based constraint.
        migrations.AlterUniqueTogether(
            name='dailyplan',
            unique_together=set(),
        ),
        migrations.AddField(
            model_name='dailyplan',
            name='dup_seq',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterUniqueTogether(
            name='dailyplan',
            unique_together={('date', 'store_id_raw', 'hb_bd', 'dup_seq')},
        ),
    ]
