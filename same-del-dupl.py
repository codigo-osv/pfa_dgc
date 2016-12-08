import operator
import pandas as pd
import dbconnections
import functions
import lfunctions

# def del_dupl_victims():
#     cur = dbconnections.psycodb.cursor()
#     cur.execute('select id_v from svictimas order by id_v;')
#     ids = [x[0] for x in cur.fetchall()]
#     res = set()
#     for id in ids:
#         q = cur.execute('select same_id, hospital_realiza, hospital_deriva,'
#                         ' hora_llamada, hora_despacho, hora_llegada, sexo,'
#                         ' edad, diagnostico from svictimas where id_v = {}'.format(id))
#         row = cur.fetchone()
#         res.add(row)
#     res1 = sorted(res, key=operator.itemgetter(0))
#     return res1
#
# cur = dbconnections.psycodb.cursor()
# cur.execute('create temp table svictimas as select row_number() over() as id_v, same_id,'
#             ' hospital_realiza, hospital_deriva, hora_llamada, hora_despacho, hora_llegada, sexo,'
#             ' edad, diagnostico from same.victimas_same;')
#
# res = del_dupl_victims()
# pdd = pd.DataFrame.from_records(res, columns=['same_id', 'hospital_realiza', 'hospital_deriva', 'hora_llamada',
#                                               'hora_despacho', 'hora_llegada', 'sexo', 'edad', 'diagnostico'])
# pdd.to_csv('svctimas.csv', index_label='id_v', encoding='utf-8')
# print(pdd)
# for r in res: print(r)


def mark_non_duplicate_rows(file_name, *filter_column_names):

    rows = functions.csv_to_dict_list(file_name)
    cols = list(rows[0].keys())
    ct = []
    ct2 = []
    targets = []
    for row in rows:
        targets = [row[column] for column in filter_column_names]
        ct.append(targets)
    for row in rows:
        targets = [row[column] for column in filter_column_names]
        if not targets in ct2:
            row['original'] = 1
            ct2.append(targets)
        row['cantidad'] = ct.count(targets)
    lfunctions.AuxFCSV.dicts_to_csv_ordrd(rows, cols + ['original', 'cantidad'], 'test')
