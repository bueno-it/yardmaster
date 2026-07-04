from django.db import models
from transport.models import Store


class DailyPlan(models.Model):
    date           = models.DateField()
    hb_bd          = models.CharField(max_length=10, blank=True)
    store          = models.ForeignKey(Store, null=True, blank=True, on_delete=models.SET_NULL, related_name='daily_plans')
    store_id_raw   = models.CharField(max_length=20, blank=True)
    store_name_raw = models.CharField(max_length=200, blank=True)
    ordered        = models.IntegerField(default=0)
    remaining      = models.IntegerField(default=0)
    doors          = models.CharField(max_length=50, blank=True)
    open_status    = models.CharField(max_length=20, blank=True)
    closed_status  = models.CharField(max_length=20, blank=True)
    company        = models.CharField(max_length=200, blank=True)
    window         = models.CharField(max_length=50, blank=True)
    comments       = models.TextField(blank=True)
    mergers        = models.CharField(max_length=100, blank=True)
    loaders        = models.CharField(max_length=100, blank=True)
    check_field    = models.CharField(max_length=100, blank=True)
    row_order      = models.IntegerField(default=0)
    flag_color     = models.CharField(max_length=20, blank=True, default='')  # manual alert flag

    created_at     = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['date', 'row_order', 'store_name_raw']
        unique_together = [['date', 'store_id_raw', 'hb_bd']]

    def __str__(self):
        name = self.store.name if self.store else self.store_name_raw
        return f"{self.date} | {name} | {self.remaining}/{self.ordered}"

    @property
    def store_display(self):
        return self.store.name if self.store else self.store_name_raw

    @property
    def picked(self):
        return max(0, self.ordered - self.remaining)

    @property
    def progress_pct(self):
        """0% if nothing picked yet, 100% only when remaining=0 and ordered>0"""
        if not self.ordered:
            return 0
        if self.remaining == 0:
            return 100
        return min(99, int((self.picked / self.ordered) * 100))

    @property
    def is_rigid(self):
        return 'rigid' in (self.company or '').lower()

    @property
    def is_complete(self):
        return self.remaining == 0 and self.ordered > 0

