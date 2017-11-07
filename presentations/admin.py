from django.contrib import admin
from .models import Lead


admin.site.site_header = 'Profissa.de | Administração'

class LeadAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'subscribe',)
    list_filter = ('subscribe', 'city_state',)


admin.site.register(Lead, LeadAdmin)
