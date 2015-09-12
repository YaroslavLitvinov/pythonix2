# -*- coding: utf-8 -*-
#Начало нового месяца для клиентов каждый день
import MySQLdb, mysql_db
import datetime
now_date = datetime.date.today()
print now_date



def f_new_month():

    cur = mysql_db.db.cursor()
    sql = ("SELECT ip_address, end_used_date, balance, select_tarif_id, select_clients_group_id, id  FROM pythonix2app_clients ")
    cur.execute(sql)
    clients = cur.fetchall()
    cur.close()

    from datetime import date, timedelta
    for client in clients:
        if client[1] <= date.today():
            
            #Сведенья о тарифе
            cur = mysql_db.db.cursor()
            sql = ("SELECT fee FROM pythonix2app_tarifs WHERE id='%s'") % (client[3])
            cur.execute(sql)
            tarif = cur.fetchone()

            if client[2] >= 0:

                if client[2] >= tarif[0]:
                    import new_date
                    new_date_value = new_date.f_new_date(client[1])
                    #Обновление данных
                    cur = mysql_db.db.cursor()
                    sql = "UPDATE pythonix2app_clients SET balance='%s', end_used_date='%s'  WHERE id='%s'" % ((client[2] - tarif[0]), new_date_value, client[5])
                    cur.execute(sql)
                    mysql_db.db.commit()
                    cur.close()
                    print new_date_value
                else:
                    #Обновление данных
                    cur = mysql_db.db.cursor()
                    sql = "UPDATE pythonix2app_clients SET balance='%s', internet_status='%s' WHERE id='%s'" % ((client[2] - tarif[0]), 0, client[5])
                    cur.execute(sql)
                    mysql_db.db.commit()
                    cur.close()




            print "END MONTH"

        else:
            print "NO END MONTH"



f_new_month()