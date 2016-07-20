# -*- coding: UTF-8 -*-
import functions


class DbPfDg:


    def gen_accidents_table(self, csv_path):
        rows = functions.csv_to_dict_list(csv_path)
        res1 = []
        res2 = []
        # create a tuple with the fields of each row to compare and check them to avoid adding duplicate entries
        for case in rows:
            cmp = case['ID']
            if not cmp in res1:
                res1.append(cmp)
                idh = str(case['PERIODO']) + str(case['ID'])
                formatted = {"orden" : case['ORDEN'], "id" : idh, "mes" : case['PERIODO'], "comisaria" : case['COMISARIA'], "fecha" : case['FECHA'],
                             "hora" : case['HORA'], "tipo_colision" : case['TIPO_COLISION'], "tipo_hecho" : case['TIPO_HECHO'], "lugar_hecho" : case['LUGAR_DEL_HECHO'],
                             "direccion_normalizada" : case['Dirección Normalizada'], "tipo_calle" : case['TIPO_DE_CALLE'],
                             "direccion_normalizada_arcgis" : case['Dirección Normalizada (ArcGIS)'], "calle1" : case['Calle'], "altura" : case['Altura'],
                             "calle2" : case['Cruce'], "codigo_calle" : case['Código de Calle'], "codigo_cruce" : case['Código de Cruce'],
                             "geocodificacion" : case['Geocodificación']
                             }
                res2.append(formatted)
        functions.dicts_to_csv(res2)


    def gen_victims_table(self, csv_path):
        rows = functions.csv_to_dict_list(csv_path)
        res1 = []
        res2 = []
        id = 0
        # create a tuple with the fields of each row to compare and check them to avoid adding duplicate entries
        for case in rows:
            cmp = (case['ID'],case['CAUSA'],case['EDAD_VICTIMA'],case['SEXO_VICTIMA'],case['VICTIMA'],case['TIPO_VEHICULO_VICTIMA'],case['MARCA_VEHICULO_VICTIMA'],case['MODELO_VEHICULO_VICTIMA'])
            if not cmp in res1:
                id += 1
                idh = str(case['PERIODO']) + str(case['ID'])
                res1.append(cmp)
                formatted = {"id_hecho" : idh, "causa" : case['CAUSA'], "rol" : case['VICTIMA'], "tipo" : case['TIPO_VEHICULO_VICTIMA'], "marca" : case['MARCA_VEHICULO_VICTIMA'],
                             "modelo" : case['MODELO_VEHICULO_VICTIMA'], "colectivo" : case['COLECTIVO_VICTIMA'], "interno_colectivo" : case['INTERNO_VICTIMA'], "sexo" : case['SEXO_VICTIMA'],
                             "edad" : case['EDAD_VICTIMA'], "sumario" : case['SRIO_NRO'], "id" : id
                            }
                res2.append(formatted)
        functions.dicts_to_csv(res2)


    def gen_accuseds_table(self, csv_path):
        rows = functions.csv_to_dict_list(csv_path)
        res1 = []
        res2 = []
        id = 0
        # create a tuple with the fields of each row to compare and check them to avoid adding duplicate entries
        for case in rows:
            cmp = (case['ID'],case['EDAD_ACUSADO'],case['SEXO_ACUSADO'],case['ACUSADO'],case['TIPO_VEHICULO_ACUSADO'],case['MARCA_VEHICULO_ACUSADO'],case['MODELO_VEHICULO_ACUSADO'])
            if not cmp in res1:
                id += 1
                idh = str(case['PERIODO']) + str(case['ID'])
                res1.append(cmp)
                formatted = {"id_hecho" : idh, "rol" : case['ACUSADO'], "tipo" : case['TIPO_VEHICULO_ACUSADO'], "marca" : case['MARCA_VEHICULO_ACUSADO'],
                             "modelo" : case['MODELO_VEHICULO_ACUSADO'], "colectivo" : case['COLECTIVO_ACUSADO'], "interno_colectivo" : case['INTERNO_ACUSADO'], "sexo" : case['SEXO_ACUSADO'],
                             "edad" : case['EDAD_ACUSADO'], "id" : id
                            }
                res2.append(formatted)
        functions.dicts_to_csv(res2)