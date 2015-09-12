#!/usr/bin/env python
# -*- coding: utf_8 -*-
import MySQLdb
def f_mysql_connect():
    con = mysql_db_connect = MySQLdb.connect(host='localhost', user='root', passwd='1q2w3e', db='pythonix2', charset='utf8')
    return con
db = f_mysql_connect()