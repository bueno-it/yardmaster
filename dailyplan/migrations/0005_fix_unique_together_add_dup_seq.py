from django.db import migrations, models


def backfill_dup_seq(apps, schema_editor):
    """Give each existing duplicate row (same date+store_id_raw+hb_bd) a
    sequential dup_seq (0, 1, 2...) based on its current row_order, so the
    new unique constraint doesn't collide on the default dup_seq=0."""
    DailyPlan = apps.get_model('dailyplan', 'DailyPlan')
    from collections import defaultdict

    groups = defaultdict(list)
    for plan in DailyPlan.objects.all().order_by('row_order', 'id'):
        key = (plan.date, plan.store_id_raw, plan.hb_bd)
        groups[key].append(plan)

    for key, plans in groups.items():
        for idx, plan in enumerate(plans):
            if plan.dup_seq != idx:
                plan.dup_seq = idx
                plan.save(update_fields=['dup_seq'])


def noop(apps, schema_editor):
    pass


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

        # Step 2: drop the row_order-based constraint and add dup_seq
        # (every existing row starts at dup_seq=0).
        migrations.AlterUniqueTogether(
            name='dailyplan',
            unique_together=set(),
        ),
        migrations.AddField(
            model_name='dailyplan',
            name='dup_seq',
            field=models.IntegerField(default=0),
        ),

        # Step 3: number genuine duplicate rows (same date+store_id_raw+hb_bd)
        # sequentially so the new constraint below won't collide.
        migrations.RunPython(backfill_dup_seq, noop),

        # Step 4: now it's safe to create the dup_seq-based constraint.
        migrations.AlterUniqueTogether(
            name='dailyplan',
            unique_together={('date', 'store_id_raw', 'hb_bd', 'dup_seq')},
        ),
    ]
