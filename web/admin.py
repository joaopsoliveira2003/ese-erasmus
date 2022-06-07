from django.contrib import admin
from web.models import *

admin.site.site_header = 'Website Administration'
admin.site.site_title = 'Website'
admin.site.index_title = 'Administration'

class listcity(admin.ModelAdmin):
    list_display = ("name", "country")

class listcoordinator(admin.ModelAdmin):
    list_display = ("name", "email", "tel")

class listschool(admin.ModelAdmin):
    list_display = ("name", "email", "tel", "address", "website", "get_city_country")

    def get_city_country(self, obj):
        return f"{obj.city}, {obj.city.country}"

    get_city_country.admin_order_field  = 'location'
    get_city_country.short_description = 'Location'

admin.site.register(country)
admin.site.register(city, listcity)
admin.site.register(category)
admin.site.register(educational_sector)
admin.site.register(coordinator, listcoordinator)
admin.site.register(school, listschool)