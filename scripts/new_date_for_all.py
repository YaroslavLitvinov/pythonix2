# -*- coding: utf-8 -*-
#Новая дата для всех клиентов
import MySQLdb, mysql_db
import datetime




def f_new_date_clients():

    cur = mysql_db.db.cursor()
    sql = ("SELECT ip_address, end_used_date, balance, select_tarif_id, select_clients_group_id, id  FROM pythonix2app_clients WHERE internet_status=1")
    cur.execute(sql)
    clients = cur.fetchall()
    cur.close()

    import new_date
    for client in clients:

        new_date_value = new_date.f_new_date("2013-11-01")
        print client
        #Обновление данных
        cur = mysql_db.db.cursor()
        sql = "UPDATE pythonix2app_clients SET end_used_date='%s'  WHERE id='%s'" % (new_date_value, client[5])
        cur.execute(sql)
        mysql_db.db.commit()
        cur.close()

f_new_date_clients()