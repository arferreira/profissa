from django.contrib import admin

from core.models import (Newsletter, Category, Configuration)


admin.site.register(Newsletter)
admin.site.register(Category)
admin.site.register(Configuration)
