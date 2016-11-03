# -*- coding: UTF-8 -*-
import csv
import operator
import tablib
from dbconnections import psycodb


def formatted_query(str_col, str_val):
    if str_val == "NULL":
        query = '{} is NULL'.format(str_col)
    elif not str_val.isdigit():
        query = "lower(" + str_col + ") = lower(" + "'" + str_val + "')"
    else:
        query = '{} = {}'.format(str_col, str_val)
    return query


def csv_to_dict_list(str_csv_file_nm):
    # returns a list of dictionaries with column names as keys, one for each row in the file
    with open(str_csv_file_nm) as fh:
        dr = csv.DictReader(fh, delimiter=',')
        case_list = [x for x in dr]
        return case_list


def dicts_to_csv(row_dict_list):
    # precondition: all rows have the same columns
    fieldnames = row_dict_list[0].keys()
    with open('resultado.csv', 'w') as fh:
        wr = csv.DictWriter(fh, fieldnames=fieldnames, delimiter=',', extrasaction='ignore', lineterminator='\n')
        wr.writeheader()
        for row in row_dict_list:
            wr.writerow(row)


def unique_values_of(str_table_nm, str_column_nm):
    # query = db.query("select distinct " + str_column_nm + " from " + str_table_nm + ";")
    # rows = [x.as_dict() for x in query]
    # unique_values_list = []
    # for row in rows:
    #     if row.get(str_column_nm) is None:
    #         unique_values_list.append("NULL")
    #     else:
    #         unique_values_list.append(str(row.get(str_column_nm)))
    # return unique_values_list
    cur = psycodb.cursor()
    cur.execute("select distinct " + str_column_nm + " from " + str_table_nm + ";")
    rows = [x[0] for x in cur.fetchall()]
    unique_values_list = []
    for row in rows:
        if row is None:
            unique_values_list.append("NULL")
        else:
            unique_values_list.append(str(row))
    return unique_values_list


def number_of_rows_in(str_table_name):
    # precondition: there are no duplicate rows in the table
    # query = db.query('select count(*) from ' + str_table_name + ';')
    # return float(query.all().__getitem__(0)[0])
    cur = psycodb.cursor()
    cur.execute('select count(*) from ' + str_table_name + ';')
    return float(cur.fetchone()[0])


def gen_dataset(header_lst, data_lst):
    data = tablib.Dataset()
    data.headers = header_lst
    for datum in data_lst:
        data.append(datum, tags=gen_tags(datum, header_lst))
    return data


def gen_tags(valstupl, cols):
    res = []
    ind = 0
    for val in valstupl:
        if isinstance(val, str):
            res.append(cols[ind].lower() + ':' + val.lower())
        else:
            res.append(cols[ind].lower() + ':' + str(val))
        ind += 1
    return res


def sort_by_num_lst(tupl_lst, *pos_of_cols):
    res = []
    for tupl in tupl_lst:
        res.append(str_to_num(tupl, *pos_of_cols))
    res = sorted(res, key=operator.itemgetter(*pos_of_cols))
    return res


def str_to_num(tupl, *pos_of_cols):
    res = list(tupl)
    for pos_of_col in pos_of_cols:
        if res[pos_of_col].isdigit():
            res[pos_of_col] = int(res[pos_of_col])
    return(tuple(res))