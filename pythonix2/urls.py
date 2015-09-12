# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from pythonix2app.views import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'pythonix2.views.home', name='home'),
    # url(r'^pythonix2/', include('pythonix2.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    ('^$', hello),

    #URLs для админ понели
    url(r'^admin_billing/$', admin_billing), #Главная страница админки
    url(r'^auth_admin/$', auth_admin), #Ссылка авторизации администраторов
    url(r'^add_client_select_physical_network/$', add_client_select_physical_network), #Добавление клиента вывод списка физических сетей
    url(r'^add_client_select_device/$', add_client_select_device), #Добавление клиента вывод списка устройств
    url(r'^add_client_select_group/$', add_client_select_group), #Добавление клиента вывод групп клиентов
    url(r'^add_client/$', add_client), #Форма добавление клиента
    url(r'^client_save/(\d{1,9})/$', client_save), #Сохранение данных о клиенте
    url(r'^achange_tarif/(\d{1,9})/$', f_admin_change_tarif),
    url(r'^aconfirm_change_tarif/(\d{1,9})/(\d{1,9})/$', f_admin_change_tarif_confirm),

    #Списки клиентов
    url(r'^client_list_all/$', f_client_list_all),
    url(r'^client_list_sel_group/(\d{1,9})/$', f_client_list_sel_group),
    #Удаление клиентов
    url(r'^del_client/(\d{1,9})/$', f_del_client),
    #Пополнение счета
    url(r'^recharge/(\d{1,9})/$', f_recharge),
    #Информация о клиенте
    url(r'^info_client/(\d{1,9})/$', f_info_client),
    #Включение отключение клиентов
    url(r'^on_off_client/(\d{1,9})/$', f_on_off_client),
    #Обновление данных клиента
    url(r'^update_client_info/(\d{1,9})/$', f_update_client_info),
    #Отчет о пополнениях клиентов
    url(r'^client_report/$', f_report),
    #Сортировка отчета администратора пополнений клиентов
    url(r'^sort_report/$', f_sort_report),
    #Генерация карточек
    url(r'^gen_card/$', f_gen_card),
    #Передача средств
    url(r'^transfer_of_money/$', f_transfer_of_money),
    #Отчет по карточкам
    url(r'^report_card/$', f_report_card),
    #Снятие оплат по карточкам
    url(r'^withdrawal/$', f_withdrawal),


    #Клиенты
    url(r'^auth_client/$', auth_client),
    url(r'^exit_client/$', exit_client),
    url(r'^client_info/$', f_client_info),
    url(r'^recharge_card/$', f_recharge_card),
    url(r'^recharge_card_kievstar/$', f_recharge_card_kievstar),
    url(r'^change_tarif/$', f_user_change_tarif),
    url(r'^confirm_change_tarif/(\d{1,9})/$', f_user_change_tarif_confirm),

    url(r'^message_page/(\w+)/$', f_message_page),
    url(r'^message_page_client/(\w+)/$', f_message_page_client),


    #Показать карточки
    url(r'^see_card/$', f_see_card),

)
