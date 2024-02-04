from django.contrib import admin

from . import models
from import_export.admin import ImportExportModelAdmin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from inline_actions.admin import InlineActionsMixin
from inline_actions.admin import InlineActionsModelAdminMixin
from django.utils.html import format_html

class LocationAdmin(ImportExportModelAdmin):

    def image_tag(self, obj):
        try:
            return format_html('<img src="https://chart.apis.google.com/chart?cht=qr&chs=200x200&chl={}"  width="250px" />'.format(obj.serial_number))
        except:
            return format_html('<img src="{}"  width="50px" />'.format("/media/not-available.jpg"))
        
    image_tag.short_description = 'Serial Number'
    readonly_fields = ['image_tag']
    list_display = ('name','serial_number','address')
    list_filter = ('name','address')
    search_fields = ['address']



class RemoteAdmin(ImportExportModelAdmin):
    list_display = ('name','location','serial_number','manufacturer')
    list_filter = ('name','serial_number')
    search_fields = ['name']


class LocationFilter(admin.SimpleListFilter):
    title = 'Location'
    parameter_name = 'location'

    def lookups(self, request, model_admin):
        locations = set([incident.remote.location for incident in models.Incident.objects.all() if incident.remote.location])
        return [(location.id, location.name) for location in locations]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(remote__location__id=self.value())
        else:
            return queryset



class IncidentAdmin(InlineActionsModelAdminMixin,ImportExportModelAdmin):
    list_display = ('remote','event_type','call','acknowledge','reset')
    list_filter = (LocationFilter,'timestamp','event_type','remote')
    search_fields = ['remote']


    def acknowledge_action(self, request, obj, parent_obj=None):
        if(obj.acknowledge!= None):
            messages.warning(request, _("Incedent Aleready Acknowledged"))
            return
        if(obj.reset!= None):
            messages.warning(request, _("Incedent Aleready Reseted"))
            return
        obj.acknowledge = timezone.now()
        obj.save()
        messages.info(request, _("Incedent Acknowledged"))

    acknowledge_action.short_description = "Acknowledge"

    def reset_action(self, request, obj, parent_obj=None):
        if(obj.reset!= None):
            messages.warning(request, _("Incedent Aleready Reseted"))
            return
        obj.reset = timezone.now()
        obj.save()
        messages.info(request, _("Incedent Reseted"))

    reset_action.short_description = "Reset"

    inline_actions = ['acknowledge_action', 'reset_action']



class SubscriptionAdmin(ImportExportModelAdmin):
    
    list_display = ('location','subscriber','timestamp')
    list_filter = ('location','subscriber','timestamp')
    search_fields = ['subscriber']

# Register your models here.
admin.site.register(models.Location,LocationAdmin)
admin.site.register(models.Remote,RemoteAdmin)
admin.site.register(models.Incident,IncidentAdmin)
admin.site.register(models.Subscription,SubscriptionAdmin)
