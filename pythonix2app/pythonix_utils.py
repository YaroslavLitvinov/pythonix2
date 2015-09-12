#!/usr/bin/python
# -*- coding: koi8-r -*-

from datetime import datetime
from datetime import date
from datetime import timedelta
import math
from dateutil.relativedelta import *

def f_add_months_to_date(old_date, m):
    """ return new date based and initial date and payed months count"""
    return old_date + relativedelta(months=m)


def f_recalculate_date_counter(initial_end_used_date, payment, tarif_fee):
    return_date = initial_end_used_date
    payed_for_month = math.modf(float(payment) / tarif_fee)
    if payed_for_month[1] > 0:
        """ If payed at least for one month. integer part is second tuple"""
        return_date = return_date + \
            relativedelta(months=int(payed_for_month[1]))

    if payed_for_month[0] > 0:
        """ If payed for incomplite month. fractional part is first tuple.
        During days count calculation fractional day's part is ignored"""
        days_payed = int(payed_for_month[0] * 30)
        return_date = return_date + relativedelta(days=days_payed)
    return return_date

def f_money_left_for_payed_period(from_date, end_used_date, tarif_fee):
    diff = relativedelta(end_used_date, from_date)
    amount=0.0
    tf=1.0
    if abs(diff.years) > 0 :
        amount = amount + tf*tarif_fee*12*diff.years
    if abs(diff.months) > 0:
        amount = amount + tf*tarif_fee*diff.months
    if abs(diff.days) > 0:
        amount = amount + tf*tarif_fee*diff.days/30
    return amount


def check_fail(name, res):
    if res != True:
        print "failed", name
    else:
        print "passed", name


def test_recalculate_date_counter():
    initial_date = date(2015, 03, 30)
    return_date = f_recalculate_date_counter(initial_date, 130, 130)
    check_fail( 'recalc_date_test1', \
                    date(2015, 04, 30) == return_date )
    initial_date = date(2015, 03, 30)
    return_date = f_recalculate_date_counter(initial_date, 10, 130)
    check_fail( 'recalc_date_test2', \
                    date(2015, 04, 1) == return_date )
    initial_date = date(2015, 03, 30)
    return_date = f_recalculate_date_counter(initial_date, 1, 130)
    check_fail( 'recalc_date_test3', \
                    date(2015, 03, 30) == return_date )

    check_fail( 'recalc_date_test4', initial_date < date(2015, 04, 30) )

    initial_date = date(2015, 03, 30)
    return_date = f_recalculate_date_counter(initial_date, 0, 130)
    check_fail( 'recalc_date_test5', \
                    date(2015, 03, 30) == return_date )

    initial_date = date(2015, 04, 6)
    return_date = f_recalculate_date_counter(initial_date, 150, 80)
    check_fail( 'recalc_date_test6', \
                    date(2015, 06, 1) == return_date )

    
def test_money_left_for_payed_period():
    check_fail( 'money_left_test1_days', \
                    f_money_left_for_payed_period( \
            date(2015, 03, 30), date(2015, 03, 30), 130) == 0)
    check_fail( 'money_left_test2_days', \
                    math.modf(f_money_left_for_payed_period( \
            date(2015, 03, 25), date(2015, 03, 30), 130))[1] == 21)
    check_fail( 'money_left_test3_days', \
                    math.modf(f_money_left_for_payed_period( \
            date(2015, 04, 4), date(2015, 03, 30), 130))[1] == -21)
    check_fail( 'money_left_test4_months', \
                    f_money_left_for_payed_period( \
            date(2015, 01, 30), date(2015, 03, 30), 130) == 260)
    check_fail( 'money_left_test5_years_months', \
                    f_money_left_for_payed_period( \
            date(2015, 01, 30), date(2016, 03, 30), 130) == 1560+260)
    

if __name__ == "__main__":
    test_recalculate_date_counter()
    test_money_left_for_payed_period()
