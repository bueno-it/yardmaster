from django.db import models

DAY_CHOICES = [
    ('Sun', 'Sunday'), ('Mon', 'Monday'), ('Tue', 'Tuesday'),
    ('Wed', 'Wednesday'), ('Thu', 'Thursday'), ('Fri', 'Friday'), ('Sat', 'Saturday'),
]
SPLIT_CHOICES = [('Full', 'Full'), ('Split', 'Split')]
DEL_CHOICES   = [('', '—'), ('HB', 'HB'), ('BD', 'BD'), ('MID', 'MID'), ('HD', 'HD')]
CONSOLIDATED_CHOICES = [
    ('', '—'), ('Loaded', 'Loaded'), ('On the Load', 'On the Load'),
    ('Pending', 'Pending'), ('Cancelled', 'Cancelled'), ('Consolidated', 'Consolidated'),
    ('Wrapped and Ready to Load', 'Wrapped and Ready to Load'),
    ('Waiting on Load', 'Waiting on Load'),
]


class Store(models.Model):
    name       = models.CharField(max_length=200, unique=True)
    store_code = models.CharField(max_length=20, blank=True)
    active     = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.store_code})" if self.store_code else self.name


class Driver(models.Model):
    name   = models.CharField(max_length=200, unique=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Company(models.Model):
    name   = models.CharField(max_length=200, unique=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Companies'

    def __str__(self):
        return self.name


class Load(models.Model):
    day            = models.CharField(max_length=3, choices=DAY_CHOICES, blank=True)
    date           = models.DateField(null=True, blank=True)
    del_type       = models.CharField(max_length=10, choices=DEL_CHOICES, blank=True)
    split_full     = models.CharField(max_length=10, choices=SPLIT_CHOICES, default='Full')

    # FK to Store — keeps raw text fallback for imported data
    store          = models.ForeignKey(Store, null=True, blank=True, on_delete=models.SET_NULL, related_name='loads')
    store_name     = models.CharField(max_length=200, blank=True)   # fallback / legacy
    store_code     = models.CharField(max_length=20, blank=True)    # fallback / legacy

    final_plt      = models.IntegerField(null=True, blank=True)
    bay            = models.CharField(max_length=20, blank=True)
    time_arrive    = models.TimeField(null=True, blank=True)
    departure_time = models.TimeField(null=True, blank=True)

    # FK to Driver
    driver         = models.ForeignKey(Driver, null=True, blank=True, on_delete=models.SET_NULL, related_name='loads')
    driver_name    = models.CharField(max_length=200, blank=True)   # fallback / legacy

    # FK to Company
    company        = models.ForeignKey(Company, null=True, blank=True, on_delete=models.SET_NULL, related_name='loads')
    company_name   = models.CharField(max_length=200, blank=True)   # fallback / legacy

    schedule_eta   = models.CharField(max_length=50, blank=True)
    date_departed  = models.DateField(null=True, blank=True)
    time_departed  = models.TimeField(null=True, blank=True)
    trailer_no     = models.CharField(max_length=50, blank=True)
    consolidated   = models.CharField(max_length=100, choices=CONSOLIDATED_CHOICES, blank=True)
    revised_eta    = models.CharField(max_length=50, blank=True)
    status         = models.CharField(max_length=50, blank=True)  # kept for DB compat, hidden from UI
    comment        = models.TextField(blank=True)

    ROW_COLOR_CHOICES = [
        ('', 'None'), ('red', 'Red'), ('green', 'Green'), ('blue', 'Blue'),
        ('yellow', 'Yellow'), ('lightblue', 'Light Blue'), ('lightgreen', 'Light Green'),
    ]
    row_color             = models.CharField(max_length=20, choices=ROW_COLOR_CHOICES, blank=True, default='')
    pre_checked_load      = models.CharField(max_length=200, blank=True)
    supervisor_checked    = models.CharField(max_length=200, blank=True)
    total_picked          = models.IntegerField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['date', 'departure_time']

    def get_store_display(self):
        return self.store.name if self.store else self.store_name

    def get_store_code(self):
        return self.store.store_code if self.store else self.store_code

    def get_driver_display(self):
        return self.driver.name if self.driver else self.driver_name

    def get_company_display(self):
        return self.company.name if self.company else self.company_name

    def __str__(self):
        return f"{self.date} | {self.get_store_display()} | {self.get_driver_display()}"
