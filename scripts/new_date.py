def f_new_date(old_date):
        from datetime import datetime
        old_date_string = old_date

        split_date = str(old_date_string).split('-')

        if (int(split_date[1])+1) > 12:
            split_date = (str(int(split_date[0])+1) + "-" + "01" + "-" + split_date[2]).split('-')
        else:
            split_date = (str(split_date[0]) + "-" + str(int(split_date[1])+1) + "-" + split_date[2]).split('-')

        #dt_obj = datetime(2013, 02, 28, )
        try:
            dt_obj = datetime(int(split_date[0]), int(split_date[1]), int(split_date[2]), )
            date_str = dt_obj.strftime("%Y-%m-%d")
            return date_str
        except:
            #print
            dt_obj = datetime(int(split_date[0]), int(split_date[1]) + 1, 1, )
            date_str = dt_obj.strftime("%Y-%m-%d")
            return date_str
