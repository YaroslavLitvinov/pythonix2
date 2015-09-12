# -*- coding: utf-8 -*-


class LinuxDev():
    def add_client(self, dev_login, dev_passwd, dev_dev_ip, dev_api_port, client_login, client_passwd, client_ip, speed_up, speed_down, unit):
        pass


    def del_client(self, dev_login, dev_passwd, dev_dev_ip, dev_api_port, client_ip):
        pass


    def on_client(self, dev_login, dev_passwd, dev_dev_ip, dev_api_port, client_ip):
        pass

    def off_client(self, dev_login, dev_passwd, dev_dev_ip, dev_api_port, client_ip):
        pass

    #Обновление данных клиента
    def f_update_client(self, login_device, password_device, ip_device, api_port, name_field, old_value_field, new_value_field):
        pass