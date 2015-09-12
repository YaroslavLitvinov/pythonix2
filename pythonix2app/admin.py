# -*- coding: utf-8 -*-
from django.contrib import admin
from pythonix2app.models import *


class PhysicalNetworkAdmin(admin.ModelAdmin):

    list_display = ('name', )

class DeviceTypeAdmin(admin.ModelAdmin):

    list_display = ('name', )

class Type_of_authorizationAdmin(admin.ModelAdmin):

    list_display = ('name', )

class DevicesAdmin(admin.ModelAdmin):

    list_display = ('name', )


class BillingAdminsAdmin(admin.ModelAdmin):

    list_display = ('fio', )


class ClientsGroupsAdmin(admin.ModelAdmin):

    list_display = ('name', )
    list_filter = ('select_device',)


class IPNetworksAdmin(admin.ModelAdmin):

    list_display = ('ipnetworks', )


class TarifsAdmin(admin.ModelAdmin):

    list_display = ('name', )
    list_filter = ('select_physicalnetwork', )

class StreetsAdmin(admin.ModelAdmin):

    list_display = ('name', 'select_device',)
    search_fields = ('name', )
    list_filter = ('select_device',)

class ClientsAdmin(admin.ModelAdmin):
    #inlines = [IPAddress_client_Line, Personal_data_clients_Line,]

    list_display = ('fio', 'select_clients_group', 'ip_address',)
    list_filter = ('select_clients_group', 'select_street',)

admin.site.register(PhysicalNetwork, PhysicalNetworkAdmin)
admin.site.register(DeviceType, DeviceTypeAdmin)
admin.site.register(Devices, DevicesAdmin)
admin.site.register(BillingAdmins, BillingAdminsAdmin)
admin.site.register(ClientsGroups, ClientsGroupsAdmin)
admin.site.register(IPNetworks, IPNetworksAdmin)
admin.site.register(Tarifs, TarifsAdmin)
admin.site.register(Streets, StreetsAdmin)
admin.site.register(Clients, ClientsAdmin)
