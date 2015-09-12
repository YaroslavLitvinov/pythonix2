# -*- coding: utf-8 -*-
#Начало нового месяца для клиентов
import MySQLdb, mysql_db
import datetime
now_date = datetime.date.today()




def f_new_month():

    cur = mysql_db.db.cursor()
    sql = ("SELECT ip_address, end_used_date, balance, select_tarif_id, select_clients_group_id, id FROM pythonix2app_clients ")
    cur.execute(sql)
    clients = cur.fetchall()
    cur.close()

    from datetime import date, timedelta
    for client in clients:

        #Сведенья о тарифе
        cur = mysql_db.db.cursor()
        sql = ("SELECT fee FROM pythonix2app_tarifs WHERE id='%s'") % (client[3])
        cur.execute(sql)
        tarif = cur.fetchone()

        #Обновление данных
        cur = mysql_db.db.cursor()
        if int(client[2] - tarif[0]) < 0:
            sql = "UPDATE pythonix2app_clients SET balance='%s', internet_status='%s'  WHERE id='%s'" % ((client[2] - tarif[0]), 0, client[5])
        else:
            sql = "UPDATE pythonix2app_clients SET balance='%s' WHERE id='%s'" % ((client[2] - tarif[0]), client[5])
        cur.execute(sql)
        mysql_db.db.commit()
        cur.close()





f_new_month()