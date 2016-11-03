from itertools import chain
import dbconnections
import functions
import operator
import psycopg2
import psycopg2.extras
import recoding


def freqabs_by_values_of_4cols(str_table_name, str_col1_name, str_col2_name, str_col3_name, str_col4_name):
    # Requires the table name where the first column is, atm works with joined 'hechos' and 'victimas' tables.
    val1 = functions.unique_values_of(str_table_name, str_col1_name)
    rec1 = []
    for vala in val1:
        sq = '(select * from victimas join hechos on victimas.id_hecho = hechos.id where ' +\
               functions.formatted_query(str_col1_name, vala) + ') as sq'
        freqsa = freqs_by_values_of_3cols(sq, str_col2_name, str_col3_name, str_col4_name)
        freqsb = [(vala, x[0], x[1], x[2], x[3]) for x in freqsa]
        rec1.append(freqsb)
    res = list(chain.from_iterable(rec1))
    return sorted(res, key=operator.itemgetter(0, 1, 2, 3))


def freqs_by_values_of_3cols(str_table_name, str_col1_name, str_col2_name, str_col3_name):
    # Precondition: all columns are in the same table. Can also be used with a subquery
    # in place of the table name argument, as long as it returns all the columns.
    val1 = functions.unique_values_of(str_table_name, str_col1_name)
    val2 = functions.unique_values_of(str_table_name, str_col2_name)
    val3 = functions.unique_values_of(str_table_name, str_col3_name)
    rec1 = []
    res = []
    total = functions.number_of_rows_in(str_table_name)
    for vala in val1:
        freq = freqs_per_unique_value_aux3(str_table_name, str_col1_name, vala,
                                           str_col2_name, val2, str_col3_name, val3)
        rec1.append(freq)
    flattened = list(chain.from_iterable(rec1))
    for tupl in flattened:
        percentage = round((tupl[3]/total)*100, 2)
        res.append(tupl + (str(percentage) + '%',))
    return sorted(res, key=operator.itemgetter(0, 1, 2))


def freqs_by_values_of_2cols(str_table_name, str_col1_name, str_col2_name):
    # Precondition: all columns are in the same table.
    val1 = functions.unique_values_of(str_table_name, str_col1_name)
    val2 = functions.unique_values_of(str_table_name, str_col2_name)
    rec = []
    res = []
    total = functions.number_of_rows_in(str_table_name)
    for vala in val1:
        freq = freqs_per_unique_value_aux1(str_table_name, str_col1_name, vala, str_col2_name, val2)
        rec.append(freq)
    flattened = [val for sublist in rec for val in sublist]
    for tupl in flattened:
        percentage = round((tupl[2]/total)*100, 2)
        res.append(tupl + (str(percentage) + '%',))
    return sorted(res, key=operator.itemgetter(0, 1))


def freqabs_by_values_of_1col(str_table_name, str_col_name):
    vals = functions.unique_values_of(str_table_name, str_col_name)
    res = []
    for val in vals:
        frec = num_of_rows_with_values_in_columns(str_table_name, [(str_col_name, val)])
        res.append((val, frec))
    return res


def freqs_per_unique_value_aux3(str_table_name, name_col_a, val_col_a, name_col_b,
                                lst_vals_col_b, name_col_c, list_vals_col_c):
    res = []
    for val_col_b in lst_vals_col_b:
        freq = freqs_per_unique_value_aux2(str_table_name, name_col_a, val_col_a, name_col_b,
                                           val_col_b, name_col_c, list_vals_col_c)
        res.append(freq)
    return list(chain.from_iterable(res))


def freqs_per_unique_value_aux2(str_table_name, name_col_a, val_col_a, name_col_b,
                                val_col_b, name_col_c, list_vals_col_c):
    res = []
    for val_col_c in list_vals_col_c:
        frec = num_of_rows_with_values_in_columns(str_table_name,
                                                  [(name_col_a, val_col_a),
                                                   (name_col_b, val_col_b), (name_col_c, val_col_c)])
        res.append((val_col_a, val_col_b, val_col_c, frec))
    return res


def freqs_per_unique_value_aux1(str_table_name, name_col_a, val_col_a, name_col_b, lst_vals_col_b):
    res = []
    for val_col_b in lst_vals_col_b:
        frec = num_of_rows_with_values_in_columns(str_table_name, [(name_col_a, val_col_a), (name_col_b, val_col_b)])
        res.append((val_col_a, val_col_b, frec))
    return res


def frqs_per_collision_type():
    rec = []
    res = set()
    accs_and_collisions = collision_type_for_accidents()
    for acc in accs_and_collisions:
        rec.append(acc[1])
    total = rec.__len__() * 1.0
    for r in rec:
        freq = rec.count(r)
        percentage = str(round((freq/total)*100, 2)) + '%'
        res.add((r, freq, percentage))
    return res


def collision_type_for_accidents():
    res = []
    accs_and_vehicles = vehic_type_of_victims_and_accuseds_for_accidents()
    for acc in accs_and_vehicles.items():
        res.append(recoding.collision_type(acc))
    return res


def num_of_rows_with_values_in_columns(str_table_name, tupl_nom_column_nom_val_lst):
    # precondition: there are no duplicate rows in the table
    cur = dbconnections.psycodb.cursor()
    subconditions = []
    for tupl in tupl_nom_column_nom_val_lst:
        if tupl == tupl_nom_column_nom_val_lst[-1]:
            subconditions.append(functions.formatted_query(tupl[0], tupl[1]) + ';')
        else:
            subconditions.append(functions.formatted_query(tupl[0], tupl[1]) + ' and')
    # query = db.query('select count(*) from ' + str_table_name + ' where ' + join(subconditions))
    # return query.all().__getitem__(0)[0]
    cur.execute('select count(*) from ' + str_table_name + ' where ' + str.join(' ', subconditions))
    return cur.fetchone()[0]


def num_of_unq_victims_for_accidents():
    # query = db.query("select id_hecho, causa, edad, sexo, rol, tipo, marca, modelo "
    #                  "from victimas;")
    # rows = [x.as_dict() for x in query]
    dict_cur = dbconnections.psycodb.cursor(cursor_factory=psycopg2.extras.DictCursor)
    dict_cur.execute("select id_hecho, causa, edad, sexo, rol, tipo, marca, modelo "
                     "from victimas;")
    rows = dict_cur.fetchall()
    set_cases = set()
    res1 = []
    res2 = set()
    # create tuples with id, cause, age, sex, vehicle type, brand, model for each row
    # and add them to a set to eliminate duplicates
    for case in rows:
        set_cases.add((case['id_hecho'], case['causa'], case['edad'], case['sexo'],
                       case['rol'], case['tipo'], case['marca'], case['modelo']))
    # create a list with the first element (accident id) of each unique tuple
    for case in set_cases:
        res1.append(int(case[0]))
    # create a tuple with accident id and the number of times it is present in the list of unique victims
    for case in res1:
        res2.add((case, res1.count(case)))
    # or key= lambda tuplaIDSiniestroYFrecuencia: tuplaIDSiniestroYFrecuencia[0])
    return sorted(res2, key=operator.itemgetter(0))


def vehic_type_of_victims_and_accuseds_for_accidents():
    # query = db.query("select victimas.id_hecho, victimas.tipo, "
    #                  "victimas.marca, victimas.modelo "
    #                  "from victimas"
    #                  "union all "
    #                  "select acusados.id_hecho, acusados.tipo, "
    #                  "acusados.marca, acusados.modelo "
    #                  "from acusados;"
    #                  )
    # # save in a list of dictionaries (one for each row) the result of the db query
    # rows = [x.as_dict() for x in query]
    dict_cur = dbconnections.psycodb.cursor(cursor_factory=psycopg2.extras.DictCursor)
    dict_cur.execute("select victimas.id_hecho, victimas.tipo, "
                     "victimas.marca, victimas.modelo "
                     "from victimas "
                     "union all "
                     "select acusados.id_hecho, acusados.tipo, "
                     "acusados.marca, acusados.modelo "
                     "from acusados;"
                     )
    rows = dict_cur.fetchall()
    # for each dictionary of the list generate a tuple with id_hecho, tipo, modelo y marca, and add it to a set
    # to eliminate duplicates
    res1 = set()
    for row in rows:
        res1.add((row['id_hecho'], row['tipo'], row['modelo'], row['marca']))
    # oder the resulting tuples by id_hecho
    res1 = sorted(res1, key=operator.itemgetter(0))
    # save in a dictionary each id_hecho as key and a list with the type of vehicles involved
    # as value
    res2 = dict()
    for x in res1:
        if x[1] is not None:
            res2.setdefault(x[0], []).append(x[1])
        else:
            res2.setdefault(x[0], []).append('NULL')
    return res2
