# -*- coding: utf-8 -*-
#!/usr/bin/env python

#Удаление временных платежей

import MySQLdb, mysql_db


import datetime
now_date = datetime.date.today()

cur = mysql_db.db.cursor()
sql = ("SELECT * FROM pythonix2app_temporarypayment")
cur.execute(sql)
temporarypayment_list = cur.fetchall()
cur.close()


from datetime import date, timedelta
for temporary_payment in temporarypayment_list:

        if temporary_payment[3] < date.today():
            #Select client
            cur = mysql_db.db.cursor()
            sql = ("SELECT * FROM pythonix2app_clients WHERE id=%s") % (temporary_payment[1])
            cur.execute(sql)
            select_client = cur.fetchone()
            cur.close()

            print select_client

            if select_client[15] - int(temporary_payment[2]) < 0:

                #Select client
                cur = mysql_db.db.cursor()
                sql = ("SELECT * FROM pythonix2app_clientsgroups WHERE id=%s") % (select_client[7])
                cur.execute(sql)
                clients_groups = cur.fetchone()
                cur.close()
                #print "\033[34m| %30s \033[0m" % (clients_groups[1])

                #Select device
                cur = mysql_db.db.cursor()
                sql = ("SELECT * FROM pythonix2app_devices WHERE id=%s") % (clients_groups[2])
                cur.execute(sql)
                client_device = cur.fetchone()
                cur.close()

                cur = mysql_db.db.cursor()
                sql = ("SELECT * FROM pythonix2app_devicetype WHERE id=%s") % (client_device[3])
                cur.execute(sql)
                type_device = cur.fetchone()
                cur.close()

                import ActionDevice

                print client_device
                devobj = ActionDevice.ActionDevice(type_device[1])
                res = devobj.dev_obj.f_off_client(client_device[5], client_device[6], client_device[4], client_device[7], select_client[4], )



                if res == "worked":
                    cur = mysql_db.db.cursor()
                    sql = "DELETE FROM pythonix2app_temporarypayment WHERE id = '%s'" % (temporary_payment[0])
                    cur.execute(sql)
                    cur.close()

                    cur = mysql_db.db.cursor()
                    sql = "UPDATE pythonix2app_clients SET balance='%s'  WHERE id='%s'" % (int(select_client[15]) - int(temporary_payment[2]), select_client[0])
                    cur.execute(sql)
                    mysql_db.db.commit()
                    cur.close()
                else:
                    print "No connect"

                print res

            else:
                cur = mysql_db.db.cursor()
                sql = "DELETE FROM pythonix2app_temporarypayment WHERE id = '%s'" % (temporary_payment[0])
                cur.execute(sql)
                cur.close()

                cur = mysql_db.db.cursor()
                sql = "UPDATE pythonix2app_clients SET balance='%s'  WHERE id='%s'" % (int(select_client[15]) - int(temporary_payment[2]), select_client[0])
                cur.execute(sql)
                mysql_db.db.commit()
                cur.close()


        else:
            print temporary_payment[3]
            print date.today()
            print "-------------------"




#print temporarypayment_list
