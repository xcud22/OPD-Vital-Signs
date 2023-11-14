from django.contrib import admin
from patient.models import Person
from vital_signs.models import VitalSigns

class VitalSignsInline(admin.TabularInline):
    model = VitalSigns
    extra = 0

class PersonAdmin(admin.ModelAdmin):
    inlines = [VitalSignsInline]

admin.site.register(Person, PersonAdmin)