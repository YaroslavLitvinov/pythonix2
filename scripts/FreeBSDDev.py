# -*- coding: utf-8 -*-


class FreeBSDDev():
    def f_add_client(self, login_device, password_device, ip_device, ip_user, login_client, password_client, speed_up, speed_down, address_list_name, unit, api_port):
        from paramiko import SSHClient
        from paramiko import AutoAddPolicy
        import time
        ssh_port = int(api_port)
        ssh = SSHClient()
        ssh.set_missing_host_key_policy(AutoAddPolicy())
        try:
            ssh.connect(ip_device, port=ssh_port, username=login_device, password=password_device)
        except :
            return u"Нет связи с сервером"

        else:
            #Добавление ip в таблицу
            #cmd = "sudo ipfw table 3 add %s" % (ip_user)
            #ssh.exec_command(cmd)
            #ssh.close()

            #time.sleep(0.3)
            #ssh.connect(ip_device, port=ssh_port, username=login_device, password=password_device)
            #cmd = 'sudo  echo %s \"%s\" %s >> /usr/local/etc/mpd5/mpd.secret' % (login_client, password_client, ip_user,)
            cmd = 'echo %s %s %s >> /usr/home/tram/mpd.secret' % (login_client, password_client, ip_user,)
            ssh.exec_command(cmd)
            ssh.close()

            #time.sleep(0.3)
            #ssh.connect(ip_device, port=ssh_port, username=login_device, password=password_device)
            #cmd = "sudo ipfw pipe %s config bw %s%sbit/s" % (pipe_number, speed_down, unit,)
            #ssh.exec_command(cmd)
            #ssh.close()

            #time.sleep(0.3)
            #ssh.connect(ip_device, port=ssh_port, username=login_device, password=password_device)
            #cmd = "sudo ipfw add 20 pipe %s ip from any to %s in" % (id_tarif, ip_user,)
            #ssh.exec_command(cmd)
            #ssh.close()

            #time.sleep(0.3)
            #ssh.connect(ip_device, port=ssh_port, username=login_device, password=password_device)
            #cmd = "sudo ipfw add 20 pipe %s ip from %s to any out" % (id_tarif, ip_user,)
            #ssh.exec_command(cmd)
            #ssh.close()


            return "worked"


    def f_remove_client(self, login_device, password_device, ip_device, api_port, ip_user):
        pass


    def f_on_client(self, dev_login, dev_passwd, dev_dev_ip, dev_api_port, client_ip):
        pass

    def f_off_client(self, dev_login, dev_passwd, dev_dev_ip, dev_api_port, client_ip):
        pass

    #Обновление данных клиента
    def f_update_client(login_device, password_device, ip_device, api_port, name_field, old_value_field, new_value_field):
        pass