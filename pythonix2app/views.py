#!/usr/bin/python
# -*- coding: koi8-r -*-


#Embedded file name: views.py
from django.http import HttpResponse
from django.template import loader, Context
from django.views.generic.simple import direct_to_template
from django.http import HttpResponseRedirect
from pythonix2app.models import *
from pythonix_utils import *
import locale
from datetime import datetime
from datetime import date
import math


def hello(request):
    #return HttpResponse('Hello')
    return HttpResponseRedirect('/auth_client/')

def passgen(size = None):
    import random
    if not size:
        size = 8

    return ''.join((str(random.randint(2, 9)) for i in range(size)))

def admin_billing(request):
    try:
        request.session['login_admin']
    except:
        return HttpResponseRedirect('/auth_admin/')

    return direct_to_template(request, 'base_admin.html')


def auth_admin(request):
    if not request.POST:
        return direct_to_template(request, 'login.html')
    else:
        try:
            auth_admin = BillingAdmins.objects.get(login=request.POST['login_admin'], passwod=request.POST['password_admin'])
        except:
            return HttpResponseRedirect('/admin_billing/')

        request.session['id'] = auth_admin.id
        request.session['login_admin'] = request.POST['login_admin']
        request.session['password_admin'] = request.POST['password_admin']
        request.session['fio_admin'] = auth_admin.fio
        return HttpResponseRedirect('/admin_billing/')


def add_client_select_physical_network(request):
    try:
        request.session['login_admin']
    except:
        return HttpResponseRedirect('/auth_admin/')

    name_form = u'Выбор физической сети'
    physicalnetwork_all = PhysicalNetwork.objects.filter(select_admin=request.session['id'])
    form_field_list = [['select_physicalnetwork',
      u'Выбор физической сети',
      physicalnetwork_all,
      'select']]
    return direct_to_template(request, 'add_client.html', {'name_form': name_form,
     'form_field_list': form_field_list,
     'action': '/add_client_select_device/'})


def add_client_select_device(request):
    try:
        request.session['login_admin']
    except:
        return HttpResponseRedirect('/auth_admin/')

    name_form = u'Выбор устройства'
    try:
        device_count = Devices.objects.filter(physicalnetwork_id=request.POST['select_physicalnetwork']).count()
    except:
        return HttpResponseRedirect('/add_client_select_physical_network/')

    if device_count == 0:
        return HttpResponseRedirect('/add_client_select_physical_network/')
    device_all = Devices.objects.filter(physicalnetwork_id=request.POST['select_physicalnetwork'], master=1)
    form_field_list = [['select_device',
      u'Выбор устройства',
      device_all,
      'select']]
    return direct_to_template(request, 'add_client.html', {'name_form': name_form,
     'form_field_list': form_field_list,
     'action': '/add_client_select_group/'})


def add_client_select_group(request):
    try:
        request.session['login_admin']
    except:
        return HttpResponseRedirect('/auth_admin/')

    try:
        clients_group_count = ClientsGroups.objects.filter(select_device_id=request.POST['select_device']).count()
    except:
        return HttpResponseRedirect('/add_client_select_physical_network/')

    if clients_group_count == 0:
        return HttpResponseRedirect('/add_client_select_physical_network/')
    name_form = u'Выбор группы клиентов'
    clients_group__all = ClientsGroups.objects.filter(select_device_id=request.POST['select_device'], select_admin=request.session['id'])
    form_field_list = [['select_clients_group',
      u'Выбор группы клиентов',
      clients_group__all,
      'select']]
    return direct_to_template(request, 'add_client.html', {'name_form': name_form,
     'form_field_list': form_field_list,
     'action': '/add_client/'})


def add_client(request):
    try:
        request.session['login_admin']
    except:
        return HttpResponseRedirect('/auth_admin/')

    name_form = u'Добавление клиента'
    physicalnetwork_all = PhysicalNetwork.objects.filter()
    all_clients = Clients.objects.filter(select_clients_group_id=request.POST['select_clients_group'])
    select_client_group = ClientsGroups.objects.get(id=request.POST['select_clients_group'])
    ipnetworks = IPNetworks.objects.all()
    get_device = Devices.objects.get(id=select_client_group.select_device_id)
    ip_networks_count = select_client_group.networks_list.filter(clientsgroups=request.POST['select_clients_group']).count()
    if ip_networks_count == 0:
        return HttpResponseRedirect(u'/message_page/Добавьте_подсеть/')
    select_ip_networks = select_client_group.networks_list.filter(clientsgroups=request.POST['select_clients_group'])
    if Tarifs.objects.filter(select_physicalnetwork_id=get_device.physicalnetwork_id).count() == 0:
        return httpresponseredirect(u'/message_page/Добавьте_тариф/')
    all_tarifs = Tarifs.objects.filter(select_physicalnetwork_id=get_device.physicalnetwork_id)
    streets_count = Streets.objects.filter(select_device_id=get_device.id).count()
    if streets_count == 0:
        return HttpResponseRedirect(u'/message_page/Добавьте_улицу/')
    all_street = Streets.objects.filter(select_device_id=get_device.id)
    list_ip_networks = ''
    for ip_network in select_ip_networks:
        ip_c = str(ip_network.ipnetworks) + '/' + str(ip_network.CIDR)
        if list_ip_networks == '':
            list_ip_networks = str(ip_c)
        else:
            list_ip_networks = str(list_ip_networks) + ',' + str(ip_c)

    userd_ips = ''
    for used in all_clients:
        userd_ips = userd_ips + str(used.ip_address)

    import iplib
    free_ips = []
    networks = list_ip_networks.split(',')
    for network in networks:
        getway_ip = str(network).split('/')
        for i in iplib.CIDR(network):
            if str(i) in userd_ips:
                pass
            elif str(i) != str(getway_ip[0]):
                free_ips.append(str(i))
                break

    form_field_list = [['fio',
      u'Ф.И.О',
      u'Введите Ф.И.О клиента',
      'input'],
     ['login',
      u'Логин',
      u'Введите логин клиента',
      'input'],
     ['password',
      u'Пароль',
      u'Введите Пароль клиента',
      'input',
      passgen(9)],
     ['input_mac',
      'mac',
      u'Введите mac (format 00:11:22:33:AA:FF)',
      'input',
      ""],
     ['input_ip_local',
      'local ip',
      u'Введите local ip',
      'input',
      ""],
     ['send_sms',
      u'Отправка смс',
      u'Установить галочку для отправки',
      'checkbox'],
     ['select_free_ip',
      u'Выбор свободного адреса',
      free_ips,
      'select_ip'],
     ['input_ip',
      u'ip адрес',
      u'Введите ip адрес',
      'input'],
     ['select_tarif',
      u'Выбор тарифа',
      all_tarifs,
      'select'],
     ['end_used_date',
      u'Дата отключения',
      u'Введите Ф.И.О клиента',
      'date'],
     ['select_street',
      u'Выбор улицы',
      all_street,
      'select'],
     ['home_address',
      u'Домашний адрес',
      u'Введите домашний адрес',
      'input'],
     ['mobile_phone',
      u'Мобильный телефон',
      u'Введите Мобильный телефон',
      'input']]
    return direct_to_template(request, 'add_client.html', {'name_form': name_form,
     'form_field_list': form_field_list,
     'action': '/client_save/' + request.POST['select_clients_group'] + '/'})


def client_save(request, id_group):

    try:
        request.session['login_admin']
    except:
        return HttpResponseRedirect('/auth_admin/')

    login_client = request.POST['login']
    try:
        select_client_group = ClientsGroups.objects.get(id=id_group)
        get_login = Clients.objects.get(login=request.POST['login'], select_clients_group_id=id_group)
    except:
        pass
    else:
        return HttpResponseRedirect(u'/message_page/Логин_занят/')

    password_client = request.POST['password']
    mac_client = request.POST['input_mac']
    ip_local_client = request.POST['input_ip_local']
    select_client_group = ClientsGroups.objects.get(id=id_group)
    get_device = Devices.objects.get(id=select_client_group.select_device_id)
    login_device = get_device.login
    password_device = get_device.passwod
    ip_device = get_device.network_address
    try:
        request.POST['send_sms']
    except:
        send_sms = 0
    else:
        send_sms = 1

    save_client = Clients()
    save_client.fio = request.POST['fio']
    save_client.login = request.POST['login']
    save_client.password = request.POST['password']
    save_client.mac = request.POST['input_mac']
    save_client.ip_local = request.POST['input_ip_local']
    import iplib
    if request.POST['input_ip'] == '':
        if iplib.detect(request.POST['select_free_ip']) == 1:
            save_client.ip_address = request.POST['select_free_ip']
            try:
                Clients.objects.get(ip_address=request.POST['select_free_ip'], select_clients_group_id=id_group)
            except:
                ip_user = request.POST['select_free_ip']
            else:
                return HttpResponseRedirect(u'/message_page/IP_адрес_занят/')

    elif iplib.detect(request.POST['input_ip']) == 1:
        try:
            Clients.objects.get(ip_address=request.POST['input_ip'], select_clients_group_id=id_group)
        except:
            save_client.ip_address = request.POST['input_ip']
            ip_user = request.POST['input_ip']
        else:
            return HttpResponseRedirect(u'/message_page/IP_адрес_занят/')

    save_client.send_sms = send_sms
    save_client.select_tarif_id = request.POST['select_tarif']
    get_tarif = Tarifs.objects.get(id=request.POST['select_tarif'])
    speed_up = get_tarif.speed_up
    speed_down = get_tarif.speed_down
    now_date = date.today()
    save_client.create_date = now_date
    if  save_client.mac == '':
        return HttpResponseRedirect(u'/message_page/Вы_не_указали_MAC_адрес/')
    if save_client.ip_local == '':
        return HttpResponseRedirect(u'/message_page/Вы_не_указали_local_IP_адрес/')
    if request.POST['select_date'] == '':
        return HttpResponseRedirect(u'/message_page/Вы_не_выбрали_дату/')
    txtdate = request.POST['select_date'][3:5] + '/' + request.POST['select_date'][0:2] + '/' + request.POST['select_date'][6:]
    enddate = datetime.strptime(txtdate, '%d/%m/%Y')
    """IL Prepare date in mikrotik's format to be used for disabling users by script. This approach is for backup in addition to pythonix cron service"""
    save_client.end_used_date = enddate.date()
    save_client.select_clients_group_id = id_group
    save_client.select_street_id = request.POST['select_street']
    save_client.home_address = request.POST['home_address']
    save_client.mobile_phone = request.POST['mobile_phone']
    save_client.internet_status = 1
    get_street = Streets.objects.get(id=request.POST['select_street'])
    import pytils
    if request.POST['home_address'] == '':
        comment = pytils.translit.slugify(get_street.name + request.POST['fio'])
    else:
        comment = pytils.translit.slugify(get_street.name + request.POST['home_address'])
    from scripts import ActionDevice
    get_devicetype = DeviceType.objects.get(id=get_device.devicetype_id)
    devobj = ActionDevice.ActionDevice(get_devicetype.name)
    res = devobj.dev_obj.f_add_client(login_device, password_device, ip_device, mac_client, ip_local_client, ip_user, login_client, password_client, speed_up, speed_down, 'internet', 'M', save_client.end_used_date,  get_device.api_port)
    link_servers = Devices.objects.filter(physicalnetwork_id=get_device.physicalnetwork_id).exclude(id=get_device.id)
    count_clients = Clients.objects.all().count()

    if res == 'worked':
        for link_server in link_servers:
            devobj = ActionDevice.ActionDevice(link_server.devicetype.name)
            devobj.dev_obj.f_add_client(link_server.login, link_server.passwod, link_server.network_address, mac_client, ip_local_client, ip_user, login_client, password_client, speed_up, speed_down, 'internet', 'M', save_client.end_used_date, link_server.api_port)

        save_client.save()
        return HttpResponseRedirect(u'/message_page/Клиент_добавлен/')
    else:
        return HttpResponseRedirect(u'/message_page/Нет_связи_с_сервером/')


def f_del_client(request, id_client):
    try:
        request.session['login_admin']
    except:
        return HttpResponseRedirect('/auth_admin/')

    if not request.POST:
        name_form = u'Подтвердить удаление клиента'
        return direct_to_template(request, 'del_client_form.html', {'name_form': name_form,
         'action': '/del_client/' + id_client + '/'})
    del_client = Clients.objects.get(id=id_client)
    select_client_group = ClientsGroups.objects.get(id=del_client.select_clients_group_id)
    get_device = Devices.objects.get(id=select_client_group.select_device_id)
    login_device = get_device.login
    password_device = get_device.passwod
    ip_device = get_device.network_address
    api_port = get_device.api_port
    from scripts import ActionDevice
    objdel = ActionDevice.ActionDevice(get_device.devicetype.name)
    res = objdel.dev_obj.f_remove_client(login_device, password_device, ip_device, api_port, del_client.ip_local, del_client.ip_address)
    link_servers = Devices.objects.filter(physicalnetwork_id=get_device.physicalnetwork_id).exclude(id=get_device.id)
    for link_server in link_servers:
        objdel = ActionDevice.ActionDevice(link_server.devicetype.name)
        objdel.dev_obj.f_remove_client(link_server.login, link_server.passwod, link_server.network_address, api_port, del_client.ip_local, del_client.ip_address)

    if res == 'worked':
        del_client.delete()
        return HttpResponseRedirect(u'/message_page/Клиент_удален/')
    else:
        return HttpResponseRedirect(u'/message_page/Клиент_не_удален/')


def f_recharge(request, id_client):
    try:
        request.session['login_admin']
    except:
        return HttpResponseRedirect('/auth_admin/')

    try:
        recharge_client = Clients.objects.get(id=id_client)
    except:
        return HttpResponse(u'Клиента не существует')

    if not request.POST:
        name_form = u'Пополнение счета клиента: ' + recharge_client.fio
        physicalnetwork_all = PhysicalNetwork.objects.all()
        form_field_list = [['recharge_field',
          u'Сумма',
          u'Введите сумму',
          'input'], 
          # ['temporary_payment',
          # u'Временный платеж',
          # u'Установить галочку для временного платежа',
          # 'checkbox'], ['count_days',
          # u'Количество дней',
          # [1,
          #  2,
          #  3,
          #  4,
          #  5,
          #  6,
          #  7,
          #  8,
          #  9,
          #  10,
          #  11,
          #  12,
          #  13,
          #  14,
          #  15],
          # 'select_count_days']
          ]
        return direct_to_template(request, 'recharge_form.html', {'name_form': name_form,
         'form_field_list': form_field_list,
         'action': '/recharge/' + id_client + '/'})

    try:
        payment = int(request.POST['recharge_field'])
    except:
        return HttpResponse(u'Введено неверное значение, для пополнения')

    return f_do_payment(request, recharge_client, payment, None)



###############################
def f_display_change_tarif(request, client_id, template, link_form, link_form_next, link_message):

    client = Clients.objects.get(id=client_id)
    client_group = ClientsGroups.objects.get(id=client.select_clients_group_id)
    device = Devices.objects.get(id=client_group.select_device_id)
    all_tarifs = Tarifs.objects.filter(select_physicalnetwork_id=device.physicalnetwork_id)
    old_tarif = Tarifs.objects.get(id=client.select_tarif_id)

    if not request.POST:
        name_form = u'Пользователь: ' + client.login + u'. Сменить текущий тариф: '+ old_tarif.name
        form_field_list = [['select_tarif_id',
                            u'Выбор тарифа',
                            all_tarifs,
                            'select']]
        return direct_to_template(request, template, {
                'name_form': name_form,
                'form_field_list': form_field_list,
                'select_tarif_id': client.select_tarif_id,
                'action': link_form})

    new_tarif_id = int(request.POST['select_tarif_id'])
    if client.select_tarif_id == new_tarif_id:
        return HttpResponseRedirect(link_message+u'Без_изменений/')
    else:
        """ Handle form's POST request"""
        return HttpResponseRedirect(link_form_next+ str(new_tarif_id)+'/')


def f_admin_change_tarif(request, client_id_str):
    try:
        request.session['login_admin']
    except:
        return HttpResponseRedirect('/auth_admin/')

    try:
        foo_client = Clients.objects.get(id=client_id_str)
    except:
        return HttpResponse(u'Клиента не существует')

    return f_display_change_tarif(request, int(client_id_str), \
                                      'admin_change_tarif.html',\
                                      '/achange_tarif/'+client_id_str+'/', \
                                      '/aconfirm_change_tarif/'+client_id_str+'/',\
                                      u'/message_page/' )


def f_user_change_tarif(request):
    try:
        request.session['client_id']
    except:
        return HttpResponseRedirect('/auth_client/')

    return f_display_change_tarif(request, int(request.session['client_id']), \
                                      'user_change_tarif.html',\
                                      '/change_tarif/', \
                                      '/confirm_change_tarif/',\
                                      u'/message_page_client/' )
    # client = Clients.objects.get(id=request.session['client_id'])
    # client_group = ClientsGroups.objects.get(id=client.select_clients_group_id)
    # device = Devices.objects.get(id=client_group.select_device_id)
    # all_tarifs = Tarifs.objects.filter(select_physicalnetwork_id=device.physicalnetwork_id)
    # old_tarif = Tarifs.objects.get(id=client.select_tarif_id)

    # if not request.POST:
    #     name_form = u'Изменение текущего тарифа: '+ old_tarif.name
    #     form_field_list = [['select_tarif_id',
    #                         u'Выбор тарифа',
    #                         all_tarifs,
    #                         'select']]
    #     return direct_to_template(request, 'user_change_tarif.html', {
    #             'name_form': name_form,
    #             'form_field_list': form_field_list,
    #             'select_tarif_id': client.select_tarif_id,
    #             'action': '/change_tarif/'})

    # new_tarif_id = int(request.POST['select_tarif_id'])
    # if client.select_tarif_id == new_tarif_id:
    #     return HttpResponseRedirect(u'/message_page_client/Без_изменений/')
    # else:
    #     """ Handle form's POST request"""
    #     return HttpResponseRedirect('/confirm_change_tarif/'+ \
    #                                     str(new_tarif_id)+'/')


def f_display_change_tarif_confirm(request, client_id, new_tarif_id, 
                                   template, link_form, link_message):

    client = Clients.objects.get(id=client_id)
    client_group = ClientsGroups.objects.get(id=client.select_clients_group_id)
    device = Devices.objects.get(id=client_group.select_device_id)
    old_tarif = Tarifs.objects.get(id=client.select_tarif_id)
    new_tarif = Tarifs.objects.get(id=new_tarif_id)

    money_amount_by_end_used_date = f_money_left_for_payed_period( \
        date.today(), client.end_used_date, old_tarif.fee)
    new_end_date_for_selected_tarif = \
        f_recalculate_date_counter(date.today(), \
                                       money_amount_by_end_used_date, \
                                       new_tarif.fee)

    is_active_subscription = u"Включен"
    if client.end_used_date < date.today():
        is_active_subscription = u"Отключен"
        new_end_date_for_selected_tarif = client.end_used_date
    
    if not request.POST:
        name_form = u'Пользователь: ' + client.login + u'. Подтвердить смену тарифа: '+ old_tarif.name
        form_field_list = [
          ['tarif_field',
              u'Тариф',
              u'Ваш текущий тариф',
              'input',
              old_tarif.name],
          ['new_tarif_field',
              u'Тариф',
              u'Новый тариф',
              'input',
              new_tarif.name],
          ['old_tarif_fee_field',
              u'Абонплата',
              u'Старая абонплата',
              'input',
              old_tarif.fee],
          ['new_tarif_fee_field',
              u'Абонплата',
              u'Новая абонплата',
              'input',
              new_tarif.fee],
          ['recalculated_money_field',
              u'Деньги',
              u'Пересчитанный остаток на счету',
              'input',
              money_amount_by_end_used_date],
          ['old_end_date_field',
              u'Дата',
              u'Текущая дата отключения',
              'input',
              client.end_used_date],
          ['new_end_date_field',
              u'Дата',
              u'Новая дата отключения',
              'input',
              new_end_date_for_selected_tarif],
          ['is_active_field',
              u'Статус',
              u'Текущий статус клиента',
              'input',
              is_active_subscription]
          ]
        return direct_to_template(request, template, {
         'name_form': name_form,
         'form_field_list': form_field_list,
         'action': link_form+str(new_tarif_id)+'/'})

    """for POST form data, get confirmation from user about new tarif"""
    if client.select_tarif_id == new_tarif_id:
        return HttpResponseRedirect(link_message+'Без_изменений/')
    elif client.end_used_date < date.today():
        """ as service is disabled, do not recalculate end_used_date,\
        just update queue """
        from scripts import ActionDevice
        devobj = ActionDevice.ActionDevice(device.devicetype.name)
        res = devobj.dev_obj.f_update_client(device.login, device.passwod, device.network_address, device.api_port, 'update_queue', client.login, new_tarif.speed_down)
        if res == 'worked':
            client.select_tarif_id = new_tarif_id
            client.save()
            return HttpResponseRedirect(link_message+u'Тариф_изменен_услуга_не_активна/')
        else:
            return HttpResponseRedirect(link_message+u'Не_могу_сменить_тариф_Сервер_не_доступен/')
    elif new_end_date_for_selected_tarif >= date.today():
        """ change tarif """
        from scripts import ActionDevice
        devobj = ActionDevice.ActionDevice(device.devicetype.name)
        change_tarif_res = devobj.dev_obj.f_update_client(device.login, device.passwod, device.network_address, device.api_port, 'update_queue', client.login, new_tarif.speed_down)
        if change_tarif_res == 'worked':
            end_date_res = devobj.dev_obj.f_on_client(device.login, device.passwod, device.network_address, device.api_port, client.ip_address, client.ip_local, new_end_date_for_selected_tarif)
            if end_date_res == 'worked':
                client.select_tarif_id = new_tarif_id
                client.end_used_date = new_end_date_for_selected_tarif
                client.save()
                return HttpResponseRedirect(link_message+u'Тариф_изменен/')
            else:
                return HttpResponseRedirect(link_message+u'При_изменении_тарифа_произошла_ошибка_Обратитесь_в_техподдержку/')
        else:
            return HttpResponseRedirect(link_message+u'Не_могу_сменить_тариф_Сервер_не_доступен/')
    else:
        return HttpResponseRedirect(link_message+u'Недостаточный_баланс_для_смены_тарифа/')


def f_admin_change_tarif_confirm(request, client_id_str, new_tarif_id_str):
    try:
        request.session['login_admin']
    except:
        return HttpResponseRedirect('/auth_admin/')

    try:
        foo_client = Clients.objects.get(id=client_id_str)
    except:
        return HttpResponse(u'Клиента не существует')

    return f_display_change_tarif_confirm(\
        request, \
            int(client_id_str),\
            int(new_tarif_id_str), \
            'admin_change_tarif.html', \
            '/aconfirm_change_tarif/' + client_id_str + '/', \
            u'/message_page/')


def f_user_change_tarif_confirm(request, new_tarif_id_str):
    try:
        request.session['client_id']
    except:
        return HttpResponseRedirect('/auth_client/')

    return f_display_change_tarif_confirm(\
        request, \
            int(request.session['client_id']),\
            int(new_tarif_id_str), \
            'user_change_tarif.html', \
            '/confirm_change_tarif/', \
            u'/message_page_client/')
    # new_tarif_id = int(new_tarif_id_str)
    # client = Clients.objects.get(id=request.session['client_id'])
    # client_group = ClientsGroups.objects.get(id=client.select_clients_group_id)
    # device = Devices.objects.get(id=client_group.select_device_id)
    # old_tarif = Tarifs.objects.get(id=client.select_tarif_id)
    # new_tarif = Tarifs.objects.get(id=new_tarif_id)

    # money_amount_by_end_used_date = f_money_left_for_payed_period( \
    #     date.today(), client.end_used_date, old_tarif.fee)
    # new_end_date_for_selected_tarif = \
    #     f_recalculate_date_counter(date.today(), \
    #                                    money_amount_by_end_used_date, \
    #                                    new_tarif.fee)

    # is_active_subscription = u"Включен"
    # if client.end_used_date < date.today():
    #     is_active_subscription = u"Отключен"
    #     new_end_date_for_selected_tarif = client.end_used_date
    
    # if not request.POST:
    #     name_form = u'Подтверждение изменения тарифа: '
    #     form_field_list = [
    #       ['tarif_field',
    #           u'Тариф',
    #           u'Ваш текущий тариф',
    #           'input',
    #           old_tarif.name],
    #       ['new_tarif_field',
    #           u'Тариф',
    #           u'Новый тариф',
    #           'input',
    #           new_tarif.name],
    #       ['old_tarif_fee_field',
    #           u'Абонплата',
    #           u'Старая абонплата',
    #           'input',
    #           old_tarif.fee],
    #       ['new_tarif_fee_field',
    #           u'Абонплата',
    #           u'Новая абонплата',
    #           'input',
    #           new_tarif.fee],
    #       ['recalculated_money_field',
    #           u'Деньги',
    #           u'Пересчитанный остаток на счету',
    #           'input',
    #           money_amount_by_end_used_date],
    #       ['old_end_date_field',
    #           u'Дата',
    #           u'Текущая дата отключения',
    #           'input',
    #           client.end_used_date],
    #       ['new_end_date_field',
    #           u'Дата',
    #           u'Новая дата отключения',
    #           'input',
    #           new_end_date_for_selected_tarif],
    #       ['is_active_field',
    #           u'Статус',
    #           u'Текущий статус клиента',
    #           'input',
    #           is_active_subscription]
    #       ]
    #     return direct_to_template(request, 'user_change_tarif.html', {
    #      'name_form': name_form,
    #      'form_field_list': form_field_list,
    #      'action': '/confirm_change_tarif/'+new_tarif_id_str+'/'})

    # """for POST form data, get confirmation from user about new tarif"""
    # if client.select_tarif_id == new_tarif_id:
    #     return HttpResponseRedirect(u'/message_page_client/Без_изменений/')
    # elif client.end_used_date < date.today():
    #     """ as service is disabled, do not recalculate end_used_date,\
    #     just update queue """
    #     from scripts import ActionDevice
    #     devobj = ActionDevice.ActionDevice(device.devicetype.name)
    #     res = devobj.dev_obj.f_update_client(device.login, device.passwod, device.network_address, device.api_port, 'update_queue', client.login, new_tarif.speed_down)
    #     if res == 'worked':
    #         client.select_tarif_id = new_tarif_id
    #         client.save()
    #         return HttpResponseRedirect(u'/message_page_client/Тариф_изменен_услуга_не_активна/')
    #     else:
    #         return HttpResponseRedirect(u'/message_page/Не_могу_сменить_тариф_Сервер_не_доступен/')
    # elif new_end_date_for_selected_tarif >= date.today():
    #     """ change tarif """
    #     from scripts import ActionDevice
    #     devobj = ActionDevice.ActionDevice(device.devicetype.name)
    #     change_tarif_res = devobj.dev_obj.f_update_client(device.login, device.passwod, device.network_address, device.api_port, 'update_queue', client.login, new_tarif.speed_down)

    #     if change_tarif_res == 'worked':
    #         end_date_res = devobj.dev_obj.f_on_client(device.login, device.passwod, device.network_address, device.api_port, client.ip_address, new_end_date_for_selected_tarif)
    #         if end_date_res == 'worked':
    #             client.select_tarif_id = new_tarif_id
    #             client.end_used_date = new_end_date_for_selected_tarif
    #             client.save()
    #             return HttpResponseRedirect(u'/message_page_client/Тариф_изменен/')
    #         else:
    #             return HttpResponseRedirect(u'/message_page/При_изменении_тарифа_произошла_ошибка_Обратитесь_в_техподдержку/')
    #     else:
    #         return HttpResponseRedirect(u'/message_page/Не_могу_сменить_тариф_Сервер_не_доступен/')
    # else:
    #     return HttpResponseRedirect(u'/message_page_client/Недостаточный_баланс_для_смены_тарифа/')

###############################


def f_info_client(request, id_client):
    try:
        request.session['login_admin']
    except:
        return HttpResponseRedirect('/auth_admin/')

    info_client = Clients.objects.get(id=id_client)
    name_form = info_client.end_used_date.isoformat()
    select_client_group = ClientsGroups.objects.get(id=info_client.select_clients_group_id)
    select_client_device = Devices.objects.get(id=select_client_group.select_device_id)
    select_physicalnetwork = PhysicalNetwork.objects.get(id=select_client_device.physicalnetwork_id)
    tarif_list = Tarifs.objects.filter(select_physicalnetwork_id=select_physicalnetwork.id)
    street_list = Streets.objects.filter(select_device=select_client_device.id)
    form_field_list = [['client_fio_field',
      u'Ф.И.О',
      u'Введите Ф.И.О',
      'input',
      info_client.fio],
     ['client_login_field',
      u'Логин',
      u'Введите Логин',
      'input',
      info_client.login],
     ['client_password_field',
      u'Пароль',
      u'Введите пароль',
      'input',
      info_client.password],
     ['client_mac_field',
      'mac',
      u'Введите mac (format 00:11:22:33:AA:FF)',
      'input',
      info_client.mac],
     ['client_ip_local_field',
      'ip_local',
      u'Введите local ip',
      'input',
      info_client.ip_local],
     ['client_ip_field',
      'ip',
      u'Введите ip',
      'input',
      info_client.ip_address],
     ['curent_tarif',
      u'Тариф',
      u'Текущий тариф',
      'input',
      info_client.select_tarif.name],
     ['end_date_field',
      u'Дата',
      u'Дата отключения, не изменяется здесь',
      'input',
      info_client.end_used_date],
     ['send_sms',
      u'Отправка смс',
      u'Установить галочку для отправки',
      'checkbox'],
     ['select_street',
      u'Выбор улицы',
      street_list,
      'select'],
     ['number_house_field',
      u'номер дома',
      u'Введите номер дома',
      'input',
      info_client.home_address],
     #['select_tarif',
     # u'Выбор тарифа',
     # tarif_list,
     # 'select'],
     ['client_phone_field',
      u'Телефон',
      u'Введите Телефон',
      'input',
      info_client.mobile_phone]]
    return direct_to_template(request, 'info_user.html', {'name_form': name_form,
     'form_field_list': form_field_list,
     'action': '/update_client_info/' + id_client + '/',
     'info_client_street_id': info_client.select_street_id,
     #'select_tarif_id': info_client.select_tarif_id,
     'action_on_off': '/on_off_client/' + id_client + '/'})


def f_on_off_client(request, id_client):

    if not request.POST:
        return HttpResponseRedirect(u'/message_page/Даные_не_получены/')
    date_client = Clients.objects.get(id=id_client)
    select_client_group = ClientsGroups.objects.get(id=date_client.select_clients_group_id)
    get_device = Devices.objects.get(id=select_client_group.select_device_id)
    select_type_device = DeviceType.objects.get(id=get_device.devicetype_id)
    if request.POST['on_off_date'] == 'on':
        select_client_group = ClientsGroups.objects.get(id=date_client.select_clients_group_id)
        get_device = Devices.objects.get(id=select_client_group.select_device_id)
        from scripts import ActionDevice
        devobj = ActionDevice.ActionDevice(get_device.devicetype.name)
        res = devobj.dev_obj.f_on_client(get_device.login, get_device.passwod, get_device.network_address, get_device.api_port, date_client.ip_address, date_client.ip_local, date_client.end_used_date)
        if res == 'worked':
            link_servers = Devices.objects.filter(physicalnetwork_id=get_device.physicalnetwork_id).exclude(id=get_device.id)
            for link_server in link_servers:
                devobj = ActionDevice.ActionDevice(link_server.devicetype.name)
                """ propogate client enableing on another servers"""
                devobj.dev_obj.f_on_client(link_server.login, link_server.passwod, link_server.network_address, link_server.api_port, date_client.ip_address, date_client.ip_local, date_client.end_used_date)

            date_client.internet_status = 1
            date_client.save()
            return HttpResponseRedirect(u'/message_page/Включить_клиента/')
        else:
            return HttpResponseRedirect(u'/message_page/Сервер_не_доступен/')
    if request.POST['on_off_date'] == 'off':
        select_client_group = ClientsGroups.objects.get(id=date_client.select_clients_group_id)
        get_device = Devices.objects.get(id=select_client_group.select_device_id)
        from scripts import ActionDevice
        devobj = ActionDevice.ActionDevice(get_device.devicetype.name)
        res = devobj.dev_obj.f_off_client(get_device.login, get_device.passwod, get_device.network_address, get_device.api_port, date_client.ip_address, date_client.ip_local)
        if res == 'worked':
            link_servers = Devices.objects.filter(physicalnetwork_id=get_device.physicalnetwork_id).exclude(id=get_device.id)
            for link_server in link_servers:
                devobj = ActionDevice.ActionDevice(link_server.devicetype.name)
                devobj.dev_obj.f_off_client(link_server.login, link_server.passwod, link_server.network_address, link_server.api_port, date_client.ip_address, date_client.ip_local)

            date_client.internet_status = 1
            date_client.save()
            return HttpResponseRedirect(u'/message_page/Отключить_клиента/')
        else:
            return HttpResponseRedirect(u'/message_page/Сервер_не_доступен/')


def f_report(request):
    try:
        request.session['login_admin']
    except:
        return HttpResponseRedirect('/auth_admin/')

    curent_admin = BillingAdmins.objects.get(id=request.session['id'])
    if curent_admin.see_report == False:
        return HttpResponseRedirect(u'/message_page/Нет_возможности_просматривать_отчет/')
    all_reports = Report.objects.all()
    data_list = []
    data_list.append(all_reports)
    monts = ['January',
     'February',
     'March',
     'April',
     'May',
     'June',
     'July',
     'August',
     'September',
     'October',
     'November',
     'December']
    name_form = u'Отчет сортировка'
    now_date = date.today()
    year = now_date.year
    previous_year = year - 1
    years = [previous_year, year]
    admin_all = BillingAdmins.objects.all()
    form_field_list = [['end_used_date',
      u'Выбор даты',
      u'Выбор даты',
      'date'],
     ['select_admin',
      u'Выбор администратора',
      admin_all,
      'select'],
     ['select_monts',
      u'Выбор Месяца',
      monts,
      'select_list_data'],
     ['select_years',
      u'Выбор года',
      years,
      'select_list_data']]
    return direct_to_template(request, 'report_list.html', {'data_list': data_list,
     'name_form': name_form,
     'form_field_list': form_field_list,
     'action': '/sort_report/'})


def f_sort_report(request):
    try:
        request.session['login_admin']
    except:
        return HttpResponseRedirect('/auth_admin/')

    curent_admin = BillingAdmins.objects.get(id=request.session['id'])
    if curent_admin.see_report == False:
        return HttpResponseRedirect(u'/message_page/Нет_возможности_просматривать_отчет/')
    elif not request.POST:
        return HttpResponseRedirect('/admin_billing/')
    elif request.POST['select_date'] == '':
        monts = {'January': '01',
         'February': '02',
         'March': '03',
         'April': '04',
         'May': '05',
         'June': '06',
         'July': '07',
         'August': '08',
         'September': '09',
         'October': '10',
         'November': '11',
         'December': '12'}
        select_date = request.POST['select_years'] + '-' + monts[request.POST['select_monts']]
        records = Report.objects.filter(id_admin_select=request.POST['select_admin'])
        money = 0
        sort_records = []
        for rec in records:
            if str(rec.date_of_refill)[0:7] == select_date:
                money = money + int(rec.sum)
                sort_records.append(rec)

        data_list = []
        data_list.append(sort_records)
        return direct_to_template(request, 'report_list_selected.html', {'data_list': data_list,
         'money': money,
         'action': '/sort_report/'})
    else:
        data_list = []
        sel_date = request.POST['select_date'][6:] + '-' + request.POST['select_date'][0:2] + '-' + request.POST['select_date'][3:5]
        records = Report.objects.filter(id_admin_select=request.POST['select_admin'], date_of_refill=sel_date)
        data_list.append(records)
        money = 0
        for rec in records:
            money = money + rec.sum

        return direct_to_template(request, 'report_list_selected.html', {'data_list': data_list,
         'money': money,
         'action': '/sort_report/'})


def f_client_list_all(request):
    try:
        request.session['login_admin']
    except:
        return HttpResponseRedirect('/auth_admin/')

    clients_group_all = ClientsGroups.objects.filter(select_admin=request.session['id'])
    data_list = []
    for clients_group in clients_group_all:
        all_clients = Clients.objects.filter(select_clients_group_id=clients_group.id)
        clients_count = Clients.objects.filter(select_clients_group_id=clients_group.id).count()
        data_list.append([all_clients,
         clients_group.name,
         clients_count,
         clients_group.id])

    return direct_to_template(request, 'client_list.html', {'data_list': data_list})


def f_message_page(request, message):
    str = message.split('_')
    message = ''
    for i in str:
        message = message + i + ' '

    return direct_to_template(request, 'message_page.html', {'message': message})


def f_update_client_info(request, id_client):

    try:
        request.session['login_admin']
    except:
        return HttpResponseRedirect('/auth_admin/')

    if not request.POST:
        return HttpResponseRedirect(u'/message_page/Нет_данных_для_обновления/')
    else:
        update_client = Clients.objects.get(id=id_client)
        select_client_group = ClientsGroups.objects.get(id=update_client.select_clients_group_id)
        select_client_device = Devices.objects.get(id=select_client_group.select_device_id)
        select_type_device = DeviceType.objects.get(id=select_client_device.devicetype_id)
        update_client.mobile_phone = request.POST['client_phone_field']
        update_client.fio = request.POST['client_fio_field']
        if update_client.password != request.POST['client_password_field']:
            from scripts import ActionDevice
            devobj = ActionDevice.ActionDevice(select_client_device.devicetype.name)
            res = devobj.dev_obj.f_update_client(select_client_device.login, select_client_device.passwod, select_client_device.network_address, select_client_device.api_port, 'update_password', update_client.password, request.POST['client_password_field'])
            if res == 'worked':
                update_client.password = request.POST['client_password_field']
            else:
                return HttpResponseRedirect(u'/message_page/Обновление_пароля_Сервер_не_доступен/')
        if update_client.login != request.POST['client_login_field']:
            from scripts import ActionDevice
            devobj = ActionDevice.ActionDevice(select_client_device.devicetype.name)
            res = devobj.dev_obj.f_update_client(select_client_device.login, select_client_device.passwod, select_client_device.network_address, select_client_device.api_port, 'update_login', update_client.login, request.POST['client_login_field'])
            if res == 'worked':
                update_client.login = request.POST['client_login_field']
            else:
                return HttpResponseRedirect(u'/message_page/Обновление_логина_Сервер_не_доступен/')
        if update_client.ip_address != request.POST['client_ip_field']:
            try:
                Clients.objects.get(ip_address=request.POST['client_ip_field'], select_clients_group_id=update_client.select_clients_group)
            except:
                from scripts import ActionDevice
                devobj = ActionDevice.ActionDevice(select_client_device.devicetype.name)
                res = devobj.dev_obj.f_update_client(select_client_device.login, select_client_device.passwod, select_client_device.network_address, select_client_device.api_port, 'update_ip', update_client.ip_address, request.POST['client_ip_field'])
                if res == 'worked':
                    update_client.ip_address = request.POST['client_ip_field']
                else:
                    return HttpResponseRedirect(u'/message_page/Обновление_ip_Сервер_не_доступен/')

        if update_client.mac != request.POST['client_mac_field']:
            try:
                Clients.objects.get(mac=request.POST['client_mac_field'], select_clients_group_id=update_client.select_clients_group)
            except:
                from scripts import ActionDevice
                devobj = ActionDevice.ActionDevice(select_client_device.devicetype.name)
                res = devobj.dev_obj.f_update_client(select_client_device.login, select_client_device.passwod, select_client_device.network_address, select_client_device.api_port, 'update_mac', update_client.mac, request.POST['client_mac_field'])
                if res == 'worked':
                    update_client.mac = request.POST['client_mac_field']
                else:
                    return HttpResponseRedirect('/message_page/mac_address_update_error/')

        if update_client.ip_local != request.POST['client_ip_local_field']:
            try:
                Clients.objects.get(ip_local=request.POST['client_ip_local_field'], select_clients_group_id=update_client.select_clients_group)
            except:
                from scripts import ActionDevice
                devobj = ActionDevice.ActionDevice(select_client_device.devicetype.name)
                res = devobj.dev_obj.f_update_client(select_client_device.login, select_client_device.passwod, select_client_device.network_address, select_client_device.api_port, 'update_ip_local', update_client.ip_local, request.POST['client_ip_local_field'])
                if res == 'worked':
                    update_client.ip_local = request.POST['client_ip_local_field']
                else:
                    return HttpResponseRedirect('/message_page/ip_local_address_update_error/')

        # if str(update_client.select_tarif_id) != str(request.POST['select_tarif']):
        #     select_client_group = ClientsGroups.objects.get(id=update_client.select_clients_group_id)
        #     select_client_device = Devices.objects.get(id=select_client_group.select_device_id)
        #     select_tarif = Tarifs.objects.get(id=request.POST['select_tarif'])
        #     if int(select_tarif.speed_down)== 3 or int(select_tarif.speed_down)== 2 or int(select_tarif.speed_down)== 0 or int(select_tarif.speed_down)== 1:
        #         """turbonet style queue"""
        #         speed = select_tarif.speed_down
        #     else:
        #         """pythonix style queue"""
        #         speed = str(select_tarif.speed_up) + 'M' + '/' + str(select_tarif.speed_down) + 'M'
        #     from scripts import ActionDevice
        #     devobj = ActionDevice.ActionDevice(select_client_device.devicetype.name)
        #     res = devobj.dev_obj.f_update_client(select_client_device.login, select_client_device.passwod, select_client_device.network_address, select_client_device.api_port, 'update_queue', update_client.login, speed)
        #     if res == 'worked':
        #         update_client.select_tarif_id = request.POST['select_tarif']
        #     else:
        #         return HttpResponseRedirect('/message_page/can_not_update_queue/')
        try:
            request.POST['send_sms']
        except:
            update_client.send_sms = 0
        else:
            update_client.send_sms = 1

        if update_client.home_address != request.POST['number_house_field']:
            update_client.home_address = request.POST['number_house_field']
        if update_client.select_street_id != request.POST['select_street']:
            update_client.select_street_id = request.POST['select_street']
        update_client.save()
        return HttpResponseRedirect(u'/message_page/Обновляем_данные/')


def f_gen_card(request):
    try:
        request.session['login_admin']
    except:
        return HttpResponseRedirect('/auth_admin/')

    curent_admin = BillingAdmins.objects.get(id=request.session['id'])
    if curent_admin.see_report == False:
        return HttpResponseRedirect(u'/message_page/Нет_возможности_генерировать_карточки/')
    elif not request.POST:
        name_form = u'Генерация карточек'
        physicalnetwork_all = PhysicalNetwork.objects.all()
        form_field_list = [['cound_card',
          u'Количество',
          u'Введите количество',
          'input'], ['par_card',
          u'Номинал',
          u'Введите номинал',
          'input']]
        return direct_to_template(request, 'gen_card_form.html', {'name_form': name_form,
         'form_field_list': form_field_list,
         'action': '/gen_card/'})
    else:
        gobj = GenCardModel()
        count_gen_card = gobj.f_gen_card(request.POST['cound_card'], request.POST['par_card'])
        return HttpResponse(count_gen_card)


def f_transfer_of_money(request):
    try:
        request.session['login_admin']
    except:
        return HttpResponseRedirect('/auth_admin/')

    curent_admin = BillingAdmins.objects.get(id=request.session['id'])
    if curent_admin.see_report == False:
        return HttpResponseRedirect(u'/message_page/Нет_возможности_просматривать_отчет/')
    elif not request.POST:
        name_form = u'Передача средств'
        admin_all = BillingAdmins.objects.all()
        form_field_list = [['money',
          u'Сумма для передачи',
          u'Введите сумму для передачи',
          'input'], ['select_admin',
          u'Выбор администратора',
          admin_all,
          'select']]
        return direct_to_template(request, 'transfer_money.html', {'name_form': name_form,
         'form_field_list': form_field_list,
         'admin_all': admin_all,
         'action': '/transfer_of_money/'})
    else:
        sel_admin = BillingAdmins.objects.get(id=request.POST['select_admin'])
        if int(request.POST['money']) < 0:
            return HttpResponseRedirect(u'/message_page/Отрицательное_значение_не_допустимо/')
        elif int(sel_admin.balance) < int(request.POST['money']):
            return HttpResponseRedirect(u'/message_page/Передаваемая_сумма_привышает_баланс_администратора/')
        sel_admin.balance = sel_admin.balance - int(request.POST['money'])
        sel_admin.save()
        return HttpResponseRedirect(u'/message_page/Средства_переданы/')


def f_report_card(request):
    report_data = PhysicalNetworkCardReport.objects.all()
    return direct_to_template(request, 'report_card.html', {'name_form': u'Отчет о карточках',
     'report_data': report_data})


def auth_client(request):
    if not request.POST:
        return direct_to_template(request, 'login_client.html')
    else:
        try:
            auth_client = Clients.objects.get(login=request.POST['login_client'], password=request.POST['password_client'])
        except:
            return HttpResponseRedirect('/client_info/')

        request.session['client_id'] = auth_client.id
        return HttpResponseRedirect('/client_info/')


def exit_client(request):
    try:
        del request.session['client_id']
    except:
        pass

    return HttpResponseRedirect('/client_info/')


def f_client_info(request):
    try:
        request.session['client_id']
    except:
        return HttpResponseRedirect('/auth_client/')

    info_client = Clients.objects.get(id=request.session['client_id'])
    name_form = info_client.fio
    select_tarif = Tarifs.objects.get(id=info_client.select_tarif_id)
    select_street = Streets.objects.get(id=info_client.select_street_id)
    used_cards = CardReport.objects.filter(client_used_card=request.session['client_id'])
    pay_report = Report.objects.filter(id_client_select=request.session['client_id'])
    form_field_list = [['client_fio_field',
      u'Ф.И.О',
      u'Ваше Ф.И.О',
      'input',
      info_client.fio],
     ['client_login_field',
      u'Логин',
      u'Ваш Логин',
      'input',
      info_client.login],
     ['client_password_field',
      u'Пароль',
      u'Ваш пароль',
      'input',
      info_client.password],
     ['client_mac_field',
      'mac',
      u'Ваш mac',
      'input',
      info_client.mac],
     ['client_ip_local_field',
      'ip_local',
      u'Ваш local ip',
      'input',
      info_client.ip_local],
     ['client_ip_field',
      'ip',
      u'Ваш ip',
      'input',
      info_client.ip_address],
     ['street_field',
      u'Улица',
      u'Ваша улица',
      'input',
      select_street.name],
     ['number_house_field',
      u'Номер дома',
      u'Ваш номер дома',
      'input',
      info_client.home_address],
     ['tarif_field',
      u'Тариф',
      u'Ваш тариф',
      'input',
      select_tarif.name],
     #['balance',
     # u'Баланс',
     # u'Ваш баланс',
     # 'input',
     # info_client.balance],
     ['client_end_date',
      u'Дата',
      u'Дата отключения',
      'input',
      info_client.end_used_date]]
    return direct_to_template(request, 'info_for_client.html', {'name_form': name_form,
     'form_field_list': form_field_list,
     'action': '',
     'used_cards': used_cards,
     'pay_report': pay_report})


def f_add_reprt_card(id_client, id_card):
    select_card = Card.objects.get(id=id_card)
    curent_client = Clients.objects.get(id=id_client)
    select_client_group = ClientsGroups.objects.get(id=curent_client.select_clients_group_id)
    get_device = Devices.objects.get(id=select_client_group.select_device_id)
    report_card = CardReport()
    report_card.client_used_card = id_client
    report_card.used_date = date.today()
    report_card.par_card = select_card.par_card
    report_card.physicalnetwork_id = get_device.physicalnetwork.id
    report_card.secret_code = select_card.secret_code
    report_card.series_card = select_card.series
    report_card.save()
    select_card.used = 1
    select_card.save()
    try:
        get_physicalnetwork_card_report = PhysicalNetworkCardReport.objects.get(physicalnetwork_id=get_device.physicalnetwork_id)
    except:
        new_physicalnetwork_card_report = PhysicalNetworkCardReport()
        new_physicalnetwork_card_report.physicalnetwork_id = get_device.physicalnetwork_id
        new_physicalnetwork_card_report.money = select_card.par_card
        new_physicalnetwork_card_report.save()
    else:
        get_physicalnetwork_card_report.money = str(int(get_physicalnetwork_card_report.money) + int(select_card.par_card))
        get_physicalnetwork_card_report.save()


def f_do_payment(request, curent_client, amount, card_id):
    """ Turbonet implementation dosn't support a balance, so end date must be setted immediately during account balance refill"""

    """ get tarif, device auth data"""
    tarif = Tarifs.objects.get(id=curent_client.select_tarif_id)
    select_client_group = ClientsGroups.objects.get(id=curent_client.select_clients_group_id)
    get_device = Devices.objects.get(id=select_client_group.select_device_id)
    from scripts import ActionDevice
    devobj = ActionDevice.ActionDevice(get_device.devicetype.name)

    """ choose max date to add payment from"""
    initial_end_used_date = date.today()
    if curent_client.end_used_date > initial_end_used_date:
        initial_end_used_date = curent_client.end_used_date
    """ Update end period of subscription"""
    curent_client.end_used_date = \
        f_recalculate_date_counter(initial_end_used_date, \
                                       amount, tarif.fee)
    if curent_client.end_used_date > initial_end_used_date:
        """ If user payed at least for two days """
        res = devobj.dev_obj.f_on_client(get_device.login, get_device.passwod, get_device.network_address, get_device.api_port, curent_client.ip_address, curent_client.end_used_date)
        if res == 'worked':
            curent_client.save()
            if card_id != None:
                f_add_reprt_card(request.session['client_id'], card_id)
            else:
                """ If refill doing by admin, request is needed to get extra fieds"""
                data_report = Report()
                data_report.id_admin_select_id = request.session['id']
                data_report.id_client_select_id = request.session['client_id']
                data_report.sum = request.POST['recharge_field']
                data_report.date_of_refill = date.today()
                data_report.save()
                sel_admin = BillingAdmins.objects.get(id=request.session['id'])
                sel_admin.balance = sel_admin.balance + int(request.POST['recharge_field'])
                sel_admin.save()

            if card_id != None:
                return HttpResponseRedirect(u'/message_page_client/Счет_пополнен_услуга_активна/')
            else:
                return HttpResponseRedirect(u'/message_page/Счет_пополнен_услуга_активна/')
        else:
            if card_id != None:
                return HttpResponseRedirect(u'/message_page_client/Сервер_не_доступен_попробуйте_еще_раз_позже/')
            else:
                return HttpResponseRedirect(u'/message_page/Сервер_не_доступен_попробуйте_еще_раз_позже/')
    else:
        if card_id != None:
            return HttpResponseRedirect(u'/message_page_client/Недостаточно_средств_для_оплаты_и_включения_услуги/')
        else:
            return HttpResponseRedirect(u'/message_page/Недостаточно_средств_для_оплаты_и_включения_услуги/')


def f_recharge_card(request):
    try:
        request.session['client_id']
    except:
        return HttpResponseRedirect('/auth_client/')

    if not request.POST:
        name_form = u'Пополнение счета, карточкой'
        form_field_list = [['code_card',
          u'Код карточки',
          u'Введите код карточки',
          'input']]
        return direct_to_template(request, 'recharge_form_card.html', {'name_form': name_form,
         'form_field_list': form_field_list,
         'action': '/recharge_card/'})
    try:
        select_card = Card.objects.get(secret_code=request.POST['code_card'], used=0)
    except:
        curent_client = Clients.objects.get(id=request.session['client_id'])
        curent_client.error_card = int(curent_client.error_card) + 1
        curent_client.save()
        return HttpResponseRedirect(u'/message_page_client/Введены_неверные_данные_для_пополнения_5_неверных_пополнений_приведет_к_блокировке/')

    curent_client = Clients.objects.get(id=request.session['client_id'])
    return f_do_payment(request, curent_client, select_card.par_card, select_card.id)


def f_recharge_card_kievstar(request):
    try:
        request.session['client_id']
    except:
        return HttpResponseRedirect('/auth_client/')

    if not request.POST:
        name_form = u'Пополнение счета, карточкой киевстар'
        form_field_list = [['code_card',
          u'Код карточки',
          u'Введите код карточки',
          'input']]
        return direct_to_template(request, 'recharge_form_card.html', {'name_form': name_form,
         'form_field_list': form_field_list,
         'action': '/recharge_card_kievstar/'})
    else:
        try:
            int(request.POST['code_card'])
        except:
            return HttpResponseRedirect(u'/message_page_client/Не_верное_значение/')

        if request.POST['code_card'] == '':
            return HttpResponseRedirect(u'/message_page_client/Значение_не_может_быть_пустым/')
        info_client = Clients.objects.get(id=request.session['client_id'])
        client_street = Streets.objects.get(id=info_client.select_street_id)
        select_client_group = ClientsGroups.objects.get(id=info_client.select_clients_group_id)
        get_device = Devices.objects.get(id=select_client_group.select_device_id)
        phisic_network = PhysicalNetwork.objects.get(id=get_device.physicalnetwork_id)
        from smsc_api import SMSC
        import sms_info
        import pytils
        send_text = pytils.translit.slugify(phisic_network.name + ' ' + client_street.name + ' ' + info_client.home_address) + ' CODE ' + request.POST['code_card']
        smsc = SMSC()
        try:
            smsc.send_sms(sms_info.phones, send_text, sender=sms_info.sender)
        except:
            pass

        return HttpResponseRedirect(u'/message_page_client/Данные_отправлены_оператору/')


def f_message_page_client(request, message):
    str = message.split('_')
    message = ''
    for i in str:
        message = message + i + ' '

    return direct_to_template(request, 'message_page_client.html', {'message': message})


def f_withdrawal(request):
    try:
        request.session['login_admin']
    except:
        return HttpResponseRedirect('/auth_admin/')

    curent_admin = BillingAdmins.objects.get(id=request.session['id'])
    if curent_admin.see_report == False:
        return HttpResponseRedirect(u'/message_page/Нет_возможности_просматривать_отчет/')
    elif not request.POST:
        return HttpResponseRedirect('/report_card/')
    else:
        sel_phisical_network = PhysicalNetworkCardReport.objects.get(physicalnetwork_id=request.POST['phisical_network'])
        try:
            int(request.POST['money'])
        except:
            return HttpResponseRedirect(u'/message_page/Введенное_значение_не_допустимо/')

        if int(request.POST['money']) < 0:
            return HttpResponseRedirect(u'/message_page/Отрицательное_значение_не_допустимо/')
        elif int(sel_phisical_network.money) < int(request.POST['money']):
            return HttpResponseRedirect(u'/message_page/Передаваемая_сумма_привышает_баланс_/')
        sel_phisical_network.money = int(sel_phisical_network.money) - int(request.POST['money'])
        sel_phisical_network.save()
        return HttpResponseRedirect(u'/message_page/Средства_переданы/')


def f_client_list_sel_group(request, id):
    try:
        request.session['login_admin']
    except:
        return HttpResponseRedirect('/auth_admin/')

    inspection = InspectionRightsAdmin()
    try:
        if int(inspection.f_inspection(request.session['id'], id)) == 0:
            return HttpResponseRedirect(u'/message_page/Нет_доступа_к_данной_группе/')
    except:
        return HttpResponseRedirect(u'/message_page/Группа_не_выбрана/')

    sel_clients_group = ClientsGroups.objects.get(id=id)
    if not request.POST:
        all_clients = Clients.objects.filter(select_clients_group_id=id)
        clients_count = Clients.objects.filter(select_clients_group_id=id).count()
    else:
        all_clients = Clients.objects.filter(select_clients_group_id=id, select_street_id=request.POST['sel_street'])
        clients_count = Clients.objects.filter(select_clients_group_id=id, select_street_id=request.POST['sel_street']).count()
    select_device = Devices.objects.get(id=sel_clients_group.select_device_id)
    streets_list = Streets.objects.filter(select_device=select_device.id)
    data_list = []
    data_list.append([all_clients,
     sel_clients_group.name,
     clients_count,
     sel_clients_group.id])
    return direct_to_template(request, 'client_list_select_group.html', {'data_list': data_list,
     'clients_count': clients_count,
     'streets_list': streets_list,
     'sel_clients_group': id})


def f_see_card(request):
    try:
        request.session['login_admin']
    except:
        return HttpResponseRedirect('/auth_admin/')

    card_list = Card.objects.filter(used=0)[0:150]
    return direct_to_template(request, 'see_card.html', {'card_list': card_list})


