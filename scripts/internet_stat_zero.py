# -*- coding: utf-8 -*-
#Новая дата для всех клиентов
import MySQLdb, mysql_db
import datetime




def f_internet_stat():

    cur = mysql_db.db.cursor()
    sql = ("SELECT ip_address, end_used_date, balance, select_tarif_id, select_clients_group_id, id  FROM pythonix2app_clients ")
    cur.execute(sql)
    clients = cur.fetchall()
    cur.close()

    import new_date
    for client in clients:
        print client
        if int(client[2]) < 0:
            #Обновление данных
            cur = mysql_db.db.cursor()
            sql = "UPDATE pythonix2app_clients SET internet_status='%s'  WHERE id='%s'" % (0, client[5])
            cur.execute(sql)
            mysql_db.db.commit()
            cur.close()
        else:
            cur = mysql_db.db.cursor()
            sql = "UPDATE pythonix2app_clients SET internet_status='%s'  WHERE id='%s'" % (1, client[5])
            cur.execute(sql)
            mysql_db.db.commit()
            cur.close()


f_internet_stat()