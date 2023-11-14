from django.contrib import admin
from .models import Transaction
from vital_signs.models import VitalSigns

class VitalSignsInline(admin.TabularInline):
    model = VitalSigns
    extra = 0
    fields = ('temperature','respiratory_rate','heart_rate','blood_pressure','oxygen_saturation','pain_scale','random_blood_sugar', 'remarks','transaction')

class TransactionAdmin(admin.ModelAdmin):
    search_fields = ['created_at', 'physician__first_name', 'physician__last_name', 'patient__first_name', 'patient__last_name']
    inlines = [VitalSignsInline]
    ordering = ('-created_at',)

admin.site.register(Transaction, TransactionAdmin)