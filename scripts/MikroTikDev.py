# -*- coding: utf-8 -*-
from RosAPI import Core
import locale

def ret_data(data):
    return_data = []
    for x in data:
        return_data.append(x)
    return return_data

def send_email(user, tarif, payment, last_date, text ):
    import os
    mes_format='echo "Tarif {1}, payment={2}, last_date={3}, {4}" | mail -s "payment {0} {2} {3}" -a "From: support@turbonet.go" xxx@xxx.com'
    os.system(mes_format.format(user, tarif, payment, last_date, text ) )

class MikroTikDev():

    def f_get_item_by_mac_in_dhcplease_list(self, core, mac_user):
        """ Check existing item in leases-list """
        res = ret_data(core.response_handler(core.talk(["/ip/dhcp-server/lease/print", "=.proplist="+".id,mac-address", "?mac-address=" + mac_user, ])))
        for i in res:
            if i["mac-address"] == mac_user:
                return i
        return None


    def f_get_item_by_ip_in_dhcplease_list(self, core, ip_user):
        """ Check existing item in arp-list """
        res = ret_data(core.response_handler(core.talk(["/ip/dhcp-server/lease/print", "=.proplist="+".id,address", "?address=" + ip_user, ])))
        for i in res:
            if i["address"] == ip_user:
                return i
        return None


    def f_get_item_by_mac_in_arp_list(self, core, mac_user):
        """ Check existing item in arp-list """
        res = ret_data(core.response_handler(core.talk(["/ip/arp/print", "=.proplist="+".id,mac-address", "?mac-address=" + mac_user, ])))
        for i in res:
            if i["mac-address"] == mac_user:
                return i
        return None


    def f_get_item_by_ip_in_arp_list(self, core, ip_user):
        """ Check existing item in arp-list """
        res = ret_data(core.response_handler(core.talk(["/ip/arp/print", "=.proplist="+".id,address", "?address=" + ip_user, ])))
        for i in res:
            if i["address"] == ip_user:
                return i
        return None


    def f_get_item_by_ip_in_address_list(self, core, ip_user):
        """ Check existing item in address-list """
        res = ret_data(core.response_handler(core.talk(["/ip/firewall/address-list/print", "=.proplist="+".id,address", "?address=" + ip_user, ])))
        for i in res:
            if i["address"] == ip_user:
                return i
        return None


    def f_get_item_by_ip_in_queues(self, core, ip_user):
        """ Check existing item in queue list """
        res = ret_data(core.response_handler(core.talk(["/queue/simple/print", "=.proplist="+".id,target-addresses", "?target-addresses=" + ip_user+"/32" ])))
        for i in res:
            if i["target-addresses"] == ip_user+"/32":
                return i
        return None

    def f_get_item_by_name_in_queues(self, core, name):
        """ Check existing item in queue list """
        res = ret_data(core.response_handler(core.talk(["/queue/simple/print", "=.proplist="+".id,name", "?name=" + name ])))
        for i in res:
            if i["name"] == name:
                return i
        return None


    def f_get_item_by_ip_in_secrets(self, core, ip_user):
        """ Check existing item in ppp secrets list """
        res = ret_data(core.response_handler(core.talk(["/ppp/secret/print", "=.proplist="+".id,remote-address", "?remote-address=" + ip_user])))
        for i in res:
            if i["remote-address"] == ip_user:
                return i
        return None


    def f_get_item_by_name_in_secrets(self, core, name):
        """ Check existing item in ppp secrets list """
        res = ret_data(core.response_handler(core.talk(["/ppp/secret/print", "=.proplist="+".id,name", "?name=" + name])))
        for i in res:
            if i["name"] == name:
                return i
        return None


    def f_add_client(self, login_device, password_device, ip_device, mac_user, ip_local_user, ip_user, login_client, password_client, speed_up, speed_down, address_list_name, unit, off_backup_date, api_port):
        try:
            current_loc = locale.getlocale()
            locale.setlocale(locale.LC_ALL, 'C')
            off_backup_txt_date = off_backup_date.strftime('%b/%d/%Y').lower()
            locale.setlocale(locale.LC_ALL, current_loc)

            a = Core(ip_device, api_port)
            a.login(login_device, password_device)
            if int(speed_down)== 3 or int(speed_down)== 2 or int(speed_down)== 0 or int(speed_down)== 1:
                """turbonet style queue"""
                queue = "Upload Tarif"+str(speed_up)+"/Download Tarif"+str(speed_down)
                a.response_handler(a.talk(["/queue/simple/add", "=name=" + login_client, "=target-addresses=" + ip_local_user, "=queue=" + queue,]))
            else:
                """pythonix style queue"""
                speed = str(speed_up)+"M/"+str(speed_down)+"M"
                a.response_handler(a.talk(["/queue/simple/add", "=name=" + login_client, "=target-addresses=" + ip_local_user, "=max-limit=" + speed,]))

            a.response_handler(a.talk(["/ppp/secret/add", "=name=" + login_client, "=password=" + password_client, "=local-address=" + ip_device, "=remote-address=" + ip_user,]))

            a.response_handler(a.talk(["/ip/arp/add", "=address=" + ip_local_user, "=mac-address=" + mac_user, "=interface=ether2-master-local", "=comment="+login_client, ]))

            a.response_handler(a.talk(["/ip/dhcp-server/lease/add", "=address=" + ip_local_user, "=mac-address=" + mac_user, "=comment="+login_client, ]))

            """Check if address already added"""
            if self.f_get_item_by_ip_in_address_list(a, ip_user) is None:
                """add local addr """
                a.response_handler(a.talk(["/ip/firewall/address-list/add", "=address=" + ip_local_user, "=list=" + "internet", "=comment=" + off_backup_txt_date,]))
                """add vpn addr """
                a.response_handler(a.talk(["/ip/firewall/address-list/add", "=address=" + ip_user, "=list=" + "internet", "=comment=" + off_backup_txt_date,]))

            #send_email(login_client, speed_down, "?", off_backup_date, "add user" )
            return "worked"
        except:
            return "no"


    #Удаление клиента
    def f_remove_client(self, login_device, password_device, ip_device,  api_port, ip_local, ip_user):
        try:
            a = Core(ip_device, api_port)
            a.login(login_device, password_device)

            item = self.f_get_item_by_ip_in_arp_list(a, ip_local)
            if not item is None:
                a.response_handler(a.talk(["/ip/arp/remove", "=.id=" + item[".id"],]))

            item = self.f_get_item_by_ip_in_dhcplease_list(a, ip_local)
            if not item is None:
                a.response_handler(a.talk(["/ip/dhcp-server/lease/remove", "=.id=" + item[".id"],]))

            """remove local addr from firewall addresses"""
            item = self.f_get_item_by_ip_in_address_list(a, ip_local)
            if not item is None:
                a.response_handler(a.talk(["/ip/firewall/address-list/remove", "=.id=" + item[".id"],]))
            """remove vpn addr from firewall addres"""
            item = self.f_get_item_by_ip_in_address_list(a, ip_user)
            if not item is None:
                a.response_handler(a.talk(["/ip/firewall/address-list/remove", "=.id=" + item[".id"],]))


            item = self.f_get_item_by_ip_in_secrets(a, ip_user)
            if not item is None:
                a.response_handler(a.talk(["/ppp/secret/remove", "=.id=" + item[".id"],]))

            item = self.f_get_item_by_ip_in_queues(a, ip_local)
            if not item is None:
                a.response_handler(a.talk(["/queue/simple/remove", "=.id=" + item[".id"],]))

        except:
            return "no"
        return "worked"


    def f_check_client(self, login_device, password_device, ip_device, api_port, ip_user):
        try:
            a = Core(ip_device, api_port)
            a.login(login_device, password_device)

            item = self.f_get_item_by_ip_in_address_list(a, ip_user)
            if not item is None:
                return "worked"
            else:
                return "no"
        except:
            return "no"


    #Включение клиента
    def f_on_client(self, login_device, password_device, ip_device, api_port, ip_user, ip_local, off_backup_date):
        try:
            current_loc = locale.getlocale()
            locale.setlocale(locale.LC_ALL, 'C')
            off_backup_txt_date = off_backup_date.strftime('%b/%d/%Y').lower()
            locale.setlocale(locale.LC_ALL, current_loc)

            a = Core(ip_device, api_port)
            a.login(login_device, password_device)

            #Do not touch arp as it's stay unmodified if disabling user
            #item = self.f_get_item_by_ip_in_arp_list(a, ip_user)
            #if not item is None:
            #    a.response_handler(a.talk(["/ip/arp/enable", "=.id=" + item[".id"],]))
            #    a.response_handler(a.talk(["/ip/arp/comment", "=comment=" + off_backup_txt_date, "=.id=" + item[".id"], ]))

            """ip local"""
            item = self.f_get_item_by_ip_in_address_list(a, ip_local)
            if not item is None:
                a.response_handler(a.talk(["/ip/firewall/address-list/enable", "=.id=" + item[".id"],]))
                a.response_handler(a.talk(["/ip/firewall/address-list/comment", "=comment=" + off_backup_txt_date, "=.id=" + item[".id"], ]))

            """ip vpn"""
            item = self.f_get_item_by_ip_in_address_list(a, ip_user)
            if not item is None:
                a.response_handler(a.talk(["/ip/firewall/address-list/enable", "=.id=" + item[".id"],]))
                a.response_handler(a.talk(["/ip/firewall/address-list/comment", "=comment=" + off_backup_txt_date, "=.id=" + item[".id"], ]))

            #send_email(ip_user"/"ip_local, "&", "?", off_backup_date, "on user" )
            return "worked"
        except:
            return "no"


    #Отключение клиента
    def f_off_client(self, login_device, password_device, ip_device, api_port, ip_user, ip_local):
        try:
            a = Core(ip_device, api_port)
            a.login(login_device, password_device)

            #While disabling user it still stay exist enabled in arp
            #item = self.f_get_item_by_ip_in_arp_list(a, ip_user)
            #if not item is None:
            #    a.response_handler(a.talk(["/ip/arp/disable", "=.id=" + item[".id"],]))

            """ip local"""
            item = self.f_get_item_by_ip_in_address_list(a, ip_local)
            if not item is None:
                a.response_handler(a.talk(["/ip/firewall/address-list/disable", "=.id=" + item[".id"],]))

            """ip vpn"""
            item = self.f_get_item_by_ip_in_address_list(a, ip_user)
            if not item is None:
                a.response_handler(a.talk(["/ip/firewall/address-list/disable", "=.id=" + item[".id"],]))

            #send_email(login_client, speed_down, "?", off_backup_date, "add user" )
            return "worked"
        except:
            return "no"



    #Обновление данных клиента
    def f_update_client(self, login_device, password_device, ip_device, api_port, name_field, old_value_field, new_value_field):
        try:
            a = Core(ip_device)
            a.login(login_device, password_device)

            if name_field == "update_ip":
                item =self.f_get_item_by_ip_in_address_list(a,old_value_field)
                if not item is None:
                    a.response_handler(a.talk(["/ip/firewall/address-list/set", "=address=" + new_value_field, "=.id=" + item[".id"],]))

                item2 = self.f_get_item_by_ip_in_secrets(a, old_value_field)
                if not item2 is None:
                    a.response_handler(a.talk(["/ppp/secret/set", "=remote-address=" + new_value_field, "=.id=" + item2[".id"],]))

            if name_field == "update_mac":
                item = self.f_get_item_by_mac_in_arp_list(a, old_value_field)
                if not item is None:
                    a.response_handler(a.talk(["/ip/arp/set", "=mac-address=" + new_value_field, "=.id=" + item[".id"],]))

                item = self.f_get_item_by_mac_in_dhcplease_list(a, old_value_field)
                if not item is None:
                    a.response_handler(a.talk(["/ip/dhcp-server/lease/set", "=mac-address=" + new_value_field, "=.id=" + item[".id"],]))

            if name_field == "update_ip_local":
                item =self.f_get_item_by_ip_in_address_list(a,old_value_field)
                if not item is None:
                    a.response_handler(a.talk(["/ip/firewall/address-list/set", "=address=" + new_value_field, "=.id=" + item[".id"],]))

                item = self.f_get_item_by_ip_in_arp_list(a, old_value_field)
                if not item is None:
                    a.response_handler(a.talk(["/ip/arp/set", "=address=" + new_value_field, "=.id=" + item[".id"],]))

                item = self.f_get_item_by_ip_in_queues(a, old_value_field)
                if not item is None:
                    a.response_handler(a.talk(["/queue/simple/set", "=target-addresses=" + new_value_field, "=.id=" + item[".id"],]))

                item = self.f_get_item_by_ip_in_dhcplease_list(a, old_value_field)
                if not item is None:
                    a.response_handler(a.talk(["/ip/dhcp-server/lease/set", "=address=" + new_value_field, "=.id=" + item[".id"],]))

            if name_field == "update_login":
                item = self.f_get_item_by_name_in_secrets(a, old_value_field)
                if not item is None:
                    a.response_handler(a.talk(["/ppp/secret/set", "=name=" + new_value_field, "=.id=" + item[".id"],]))

                item2 = self.f_get_item_by_name_in_queues(a, old_value_field)
                if not item2 is None:
                    a.response_handler(a.talk(["/queue/simple/set", "=name=" + new_value_field, "=.id=" + item2[".id"],]))

            if name_field == "update_password":
                item = self.f_get_item_by_name_in_secrets(a, old_value_field)
                if not item is None:
                    a.response_handler(a.talk(["/ppp/secret/set", "=password=" + new_value_field, "=.id=" + item[".id"],]))

            if name_field == "update_queue":
                item = self.f_get_item_by_name_in_queues(a, old_value_field)
                if not item is None:
                    if int(new_value_field)== 3 or int(new_value_field)== 2 or int(new_value_field)== 0 or int(new_value_field)== 1:
                        """turbonet style queue"""
                        queue = "Upload Tarif"+str(new_value_field)+"/Download Tarif"+str(new_value_field)
                        a.response_handler(a.talk(["/queue/simple/set", "=queue=" + queue, "=.id=" + item[".id"],]))
                    else:
                        """pythonix style queue"""
                        a.response_handler(a.talk(["/queue/simple/set", "=max-limit=" + new_value_field, "=.id=" + item[".id"],]))
                        
            info_mes = "New tarif=" + str(new_value_field) + " for user: "+old_value_field
            a.response_handler(a.talk(["/log/info", "=message=" + info_mes, ]))

            return "worked"

        except:
            return "no"


def check_fail(name, res):
    if res!="worked":
        print name, "failed"
    else:
        print name, "passed"

def test():
    import datetime
    tik = MikroTikDev()
    user="admin" 
    passw=""
    serv="77.77.77.77"
    user_ip="10.10.111.11"
    new_user_ip="10.10.111.12"
    user_ip_local="192.168.9.1"
    new_user_ip_local="192.168.9.4"
    user_mac="00:22:44:66:88:AA"
    new_user_mac="00:22:44:66:88:BB"
    name = "chamerboy"
    new_name = "chamerboyzzz"
    user_passw = "chamerboy"
    new_user_passw = "chamerboyzzz"
    date1 = datetime.datetime.strptime('16/03/2015', '%d/%m/%Y').date()
    date2 = datetime.datetime.strptime('17/03/2015', '%d/%m/%Y').date()
    check_fail("remove", 
               tik.f_remove_client(user, passw, serv, 8728, user_ip_local, user_ip))
    check_fail("add",
               tik.f_add_client(user, passw, serv, user_mac, user_ip_local, user_ip, name, "chamerboy", "3", "3", "foo-address-list-name", "foo-unit", date1, 8728 ))
    check_fail("on", 
               tik.f_on_client(user, passw, serv, 8728, user_ip, user_ip_local, date2))
    check_fail("update_mac", 
               tik.f_update_client(user, passw, serv, 8728, "update_mac", user_mac, new_user_mac))
    check_fail("update_ip_local", 
               tik.f_update_client(user, passw, serv, 8728, "update_ip_local", user_ip_local, new_user_ip_local))
    check_fail("update_ip", 
               tik.f_update_client(user, passw, serv, 8728, "update_ip", user_ip, new_user_ip))
    check_fail("update_login", 
               tik.f_update_client(user, passw, serv, 8728, "update_login", name, new_name))
    check_fail("update_password", 
               tik.f_update_client(user, passw, serv, 8728, "update_password", new_name, new_user_passw))
    #tarif
    check_fail("update_queue",
               tik.f_update_client(user, passw, serv, 8728, "update_queue", new_name, 0))
    check_fail("off", 
               tik.f_off_client(user, passw, serv, 8728, new_user_ip, new_user_ip_local))
    check_fail("remove", 
               tik.f_remove_client(user, passw, serv, 8728, new_user_ip_local, new_user_ip))
        
if __name__ == "__main__":
	test()
