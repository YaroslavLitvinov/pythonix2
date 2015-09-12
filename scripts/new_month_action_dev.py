# -*- coding: utf-8 -*-
#Начало нового месяца для клиентов
import MySQLdb, mysql_db
import datetime
now_date = datetime.date.today()
print now_date



def f_new_month():

    cur = mysql_db.db.cursor()
    sql = ("SELECT ip_address, end_used_date, balance, select_tarif_id, select_clients_group_id, id, internet_status FROM pythonix2app_clients ")
    cur.execute(sql)
    clients = cur.fetchall()
    cur.close()

    from datetime import date, timedelta
    for client in clients:
        print client[0]

        cur = mysql_db.db.cursor()
        sql = ("SELECT select_device_id FROM pythonix2app_clientsgroups WHERE id='%s'") % (client[4])
        cur.execute(sql)
        client_group = cur.fetchone()
        cur.close()

        cur = mysql_db.db.cursor()
        sql = ("SELECT login, passwod, network_address, api_port, physicalnetwork_id FROM pythonix2app_devices WHERE id='%s'") % (client_group[0])
        cur.execute(sql)
        device = cur.fetchone()
        cur.close()

        cur = mysql_db.db.cursor()
        sql = ("SELECT devicetype_id, network_address, login, passwod, api_port FROM pythonix2app_devices WHERE physicalnetwork_id='%s'") % (device[4])
        cur.execute(sql)
        all_devices = cur.fetchall()
        cur.close()

        #print all_devices
        if client[6] == 0:

            import ActionDevice

            for device in all_devices:
                login = device[2]
                password = device[3]
                network_address = device[1]
                api_port = device[4]
                cur = mysql_db.db.cursor()
                sql = ("SELECT name FROM pythonix2app_devicetype WHERE id='%s'") % (device[0])
                cur.execute(sql)
                type_device = cur.fetchone()
                cur.close()
                #print type_device[0]
                #print "#####################################"
                devobj = ActionDevice.ActionDevice(type_device[0])
                devobj.dev_obj.f_off_client(login, password, network_address, api_port, client[0])






f_new_month()