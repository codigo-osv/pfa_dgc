# -*- coding: UTF-8 -*-
import functions
import recoding


def genVictimsTable(strPathToCsv):
    rows = functions.csvToDictList(strPathToCsv)
    res1 = []
    res2 = []
    query = functions.db.query('select max(id) from victimas;')
    id = int(query.all().__getitem__(0)[0])
    # create a tuple with the fields of each row to compare and check them to avoid adding duplicate entries
    for case in rows:
        cmp = (case['ID'],case['CAUSA'],case['EDAD_VICTIMA'],case['SEXO_VICTIMA'],case['VICTIMA'],case['TIPO_VEHICULO_VICTIMA'],case['MARCA_VEHICULO_VICTIMA'],case['MODELO_VEHICULO_VICTIMA'])
        if not cmp in res1:
            id += 1
            res1.append(cmp)
            formatted = {"id_hecho" : case['ID'], "causa" : case['CAUSA'], "rol" : case['VICTIMA'], "tipo" : case['TIPO_VEHICULO_VICTIMA'], "marca" : case['MARCA_VEHICULO_VICTIMA'],
                         "modelo" : case['MODELO_VEHICULO_VICTIMA'], "colectivo" : case['COLECTIVO_VICTIMA'], "interno_colectivo" : case['INTERNO_VICTIMA'], "sexo" : case['SEXO_VICTIMA'],
                         "edad" : case['EDAD_VICTIMA'], "sumario" : case['SRIO_NRO'], "id" : id
                         # "tipo_recod" : recoding.vehicleTypeRecoded(case['TIPO_VEHICULO_VICTIMA']),"franja_edad" : recoding.ageRange(int(case['EDAD_VICTIMA']))
                         }
            res2.append(formatted)
    functions.dictsToCsv(res2)


def genAccusedsTable(strPathToCsv):
    rows = functions.csvToDictList(strPathToCsv)
    res1 = []
    res2 = []
    query = functions.db.query('select max(id) from acusados;')
    id = int(query.all().__getitem__(0)[0])
    # create a tuple with the fields of each row to compare and check them to avoid adding duplicate entries
    for case in rows:
        cmp = (case['ID'],case['EDAD_ACUSADO'],case['SEXO_ACUSADO'],case['ACUSADO'],case['TIPO_VEHICULO_ACUSADO'],case['MARCA_VEHICULO_ACUSADO'],case['MODELO_VEHICULO_ACUSADO'])
        if not cmp in res1:
            id += 1
            res1.append(cmp)
            formatted = {"id_hecho" : case['ID'], "rol" : case['ACUSADO'], "tipo" : case['TIPO_VEHICULO_ACUSADO'], "marca" : case['MARCA_VEHICULO_ACUSADO'],
                         "modelo" : case['MODELO_VEHICULO_ACUSADO'], "colectivo" : case['COLECTIVO_ACUSADO'], "interno_colectivo" : case['INTERNO_ACUSADO'], "sexo" : case['SEXO_ACUSADO'],
                         "edad" : case['EDAD_ACUSADO'], "id" : id
                         # "tipo_recod" : recoding.vehicleTypeRecoded(case['TIPO_VEHICULO_ACUSADO']),"franja_edad" : recoding.ageRange(int(case['EDAD_ACUSADO']))
                         }
            res2.append(formatted)
    functions.dictsToCsv(res2)