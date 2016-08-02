# -*- coding: UTF-8 -*-
import csv
from itertools import chain
import functions
import recoding


class DbPfDg:


    def process_csv(self, csv_path):
        self.normalize_accidents_ids(csv_path)
        self.normalize_initial_values_lst(csv_path)
        self.gen_accidents_table(csv_path)
        self.gen_victims_table(csv_path)
        self.gen_accuseds_table(csv_path)


    def normalize_accidents_ids(self, csv_path):
        dict_lst = functions.csv_to_dict_list(csv_path)
        query = functions.db.query('select max(id) from hechos')
        newid = int(query.all().__getitem__(0)[0])
        rec = {}
        res = []
        for dict in dict_lst:
            original_id = dict['ID']
            if original_id in rec.keys():
                newid = rec[original_id]
            else:
                newid += 1
                rec[original_id] = newid
            dict['ID'] = newid
            res.append(dict)
        functions.dicts_to_csv(res)


    def normalize_initial_values_lst(self, csv_path):
        dict_lst = functions.csv_to_dict_list(csv_path)
        res = []
        for dict in dict_lst:
            dn = self.normalize_initial_values(dict)
            res.append(dn)
        functions.dicts_to_csv(res)


    def normalize_initial_values(self, dict):
        for key in dict.keys():
            if recoding.is_no_data(dict[key]):
                dict[key] = ''
            elif dict[key] == 'AVENIDA + AUTOPISTA':
                dict[key] = 'AUTOPISTA'
            elif dict[key] == 'AUTO (no se especifica si es particular o de alquiler)':
                dict[key] = 'AUTO'
            elif dict[key] == 'AUTO PFA / MOVIL / GENDARMERIA / METROPOLITANA / MOTO MOVIL':
                dict[key] = 'FUERZA SEGURIDAD'
            elif dict[key] == 'CONDUCTOR (A/P-A/A-MOTO-CICLOMOTOR-T/P-CAMION-UTILITARIO)':
                dict[key] = 'CONDUCTOR'
            elif dict[key] == 'PASAJERO/ACOMPAÑANTE (A/P-A/A-MOTO-CICLOMOTOR-T/P-CAMION-UTILITARIO)':
                dict[key] = 'PASAJERO'
            elif 'PASAJERO/ACOMPAÑANTE' in dict[key]:
                dict[key] = dict[key].replace('PASAJERO/ACOMPAÑANTE', 'PASAJERO')
            elif 'PASAJERO/ ACOMPAÑANTE' in dict[key]:
                dict[key] = dict[key].replace('PASAJERO/ ACOMPAÑANTE', 'PASAJERO')
            elif 'PASAJERO/ACOMPAïż½ANTE' in dict[key]:
                dict[key] = dict[key].replace('PASAJERO/ACOMPAïż½ANTE', 'PASAJERO')
            elif 'PASAJERO/ ACOMPAïż½ANTE' in dict[key]:
                dict[key] = dict[key].replace('PASAJERO/ ACOMPAïż½ANTE', 'PASAJERO')
        return dict


    def gen_accidents_table(self, csv_path):
        rows = functions.csv_to_dict_list(csv_path)
        res1 = []
        res2 = []
        # create a tuple with the fields of each row to compare and check them to avoid adding duplicate entries
        for case in rows:
            cmp = case['ID']
            if not cmp in res1:
                res1.append(cmp)
                formatted = {"orden" : case['ORDEN'], "id" : cmp, "mes" : case['PERIODO'], "comisaria" : case['COMISARIA'], "fecha" : case['FECHA'],
                             "hora" : case['HORA'], "tipo_colision" : case['TIPO_COLISION'], "tipo_hecho" : case['TIPO_HECHO'], "lugar_hecho" : case['LUGAR_DEL_HECHO'],
                             "direccion_normalizada" : case['Dirección Normalizada'], "tipo_calle" : case['TIPO_DE_CALLE'],
                             "direccion_normalizada_arcgis" : case['Dirección Normalizada (ArcGIS)'], "calle1" : case['Calle'], "altura" : case['Altura'],
                             "calle2" : case['Cruce'], "codigo_calle" : case['Código de Calle'], "codigo_cruce" : case['Código de Cruce'],
                             "geocodificacion" : case['Geocodificación']
                             }
                res2.append(formatted)
        ordrd_cols = ["orden", "id", "mes", "comisaria", "fecha", "hora", "tipo_colision", "tipo_hecho", "lugar_hecho", "direccion_normalizada", "tipo_calle",
                      "direccion_normalizada_arcgis", "calle1", "altura", "calle2", "codigo_calle", "codigo_cruce", "geocodificacion"
                     ]
        self.dicts_to_csv_ordrd(res2, ordrd_cols, 'hechos')


    def gen_victims_table(self, csv_path):
        rows = functions.csv_to_dict_list(csv_path)
        res1 = []
        res2 = []
        query = functions.db.query('select max(id) from victimas')
        id = int(query.all().__getitem__(0)[0])
        # create a tuple with the fields of each row to compare and check them to avoid adding duplicate entries
        for case in rows:
            cmp_dup = (case['ID'], case['CAUSA'], case['EDAD_VICTIMA'], case['SEXO_VICTIMA'], case['VICTIMA'], case['TIPO_VEHICULO_VICTIMA'], case['MARCA_VEHICULO_VICTIMA'], case['MODELO_VEHICULO_VICTIMA'])
            cmp_emp = (case['CAUSA'], case['EDAD_VICTIMA'], case['SEXO_VICTIMA'], case['VICTIMA'], case['TIPO_VEHICULO_VICTIMA'],
                       case['MARCA_VEHICULO_VICTIMA'], case['MODELO_VEHICULO_VICTIMA'], case['COLECTIVO_VICTIMA'], case['INTERNO_VICTIMA']
                       )
            if not ((cmp_dup in res1) or (self.blank_fields(cmp_emp))):
                id += 1
                res1.append(cmp_dup)
                formatted = {"id_hecho" : case['ID'], "causa" : case['CAUSA'], "rol" : case['VICTIMA'], "tipo" : case['TIPO_VEHICULO_VICTIMA'], "marca" : case['MARCA_VEHICULO_VICTIMA'],
                             "modelo" : case['MODELO_VEHICULO_VICTIMA'], "colectivo" : case['COLECTIVO_VICTIMA'], "interno_colectivo" : case['INTERNO_VICTIMA'], "sexo" : case['SEXO_VICTIMA'],
                             "edad" : case['EDAD_VICTIMA'], "sumario" : case['SRIO_NRO'], "id" : id
                            }
                res2.append(formatted)
        ordrd_cols = ["id_hecho", "causa", "rol", "tipo", "marca", "modelo", "colectivo", "interno_colectivo", "sexo", "edad", "sumario", "id"]
        self.dicts_to_csv_ordrd(res2, ordrd_cols, 'victimas')


    def gen_accuseds_table(self, csv_path):
        rows = functions.csv_to_dict_list(csv_path)
        res1 = []
        res2 = []
        query = functions.db.query('select max(id) from acusados')
        id = int(query.all().__getitem__(0)[0])
        # create a tuple with the fields of each row to compare and check them to avoid adding duplicate entries
        for case in rows:
            cmp_dup = (case['ID'], case['EDAD_ACUSADO'], case['SEXO_ACUSADO'], case['ACUSADO'], case['TIPO_VEHICULO_ACUSADO'], case['MARCA_VEHICULO_ACUSADO'], case['MODELO_VEHICULO_ACUSADO'])
            cmp_emp = (case['EDAD_ACUSADO'], case['SEXO_ACUSADO'], case['ACUSADO'], case['TIPO_VEHICULO_ACUSADO'], case['MARCA_VEHICULO_ACUSADO'], case['MODELO_VEHICULO_ACUSADO'],
                       case['COLECTIVO_ACUSADO'], case['INTERNO_ACUSADO']
                      )
            if not ((cmp_dup in res1) or (self.blank_fields(cmp_emp))):
                id += 1
                res1.append(cmp_dup)
                formatted = {"id_hecho" : case['ID'], "rol" : case['ACUSADO'], "tipo" : case['TIPO_VEHICULO_ACUSADO'], "marca" : case['MARCA_VEHICULO_ACUSADO'],
                             "modelo" : case['MODELO_VEHICULO_ACUSADO'], "colectivo" : case['COLECTIVO_ACUSADO'], "interno_colectivo" : case['INTERNO_ACUSADO'],
                             "sexo" : case['SEXO_ACUSADO'], "edad" : case['EDAD_ACUSADO'], "id" : id
                            }
                res2.append(formatted)
        ordrd_cols = ["id_hecho", "rol", "tipo", "marca", "modelo", "colectivo", "interno_colectivo", "sexo", "edad", "id"]
        self.dicts_to_csv_ordrd(res2, ordrd_cols, 'acusados')


    def blank_fields(self, str_fields):
        res = ''
        for field in str_fields:
            res += field
        return res.__len__() == 0


    def dicts_to_csv_ordrd(self, row_dict_list, column_lst, destnm):
        #precondition: all rows have the same columns
        destf = destnm + '.csv'
        with open(destf, 'w') as fh:
            wr = csv.DictWriter(fh, fieldnames=column_lst, delimiter=',', extrasaction='ignore', lineterminator='\n')
            wr.writeheader()
            for row in row_dict_list:
                wr.writerow(row)


    def merge_csvs_ordrd(self, column_lst, destnm, *csv_path):
        #precondition: all csvs and all rows have the same columns
        rec = []
        for csv in csv_path:
            rec.append(functions.csv_to_dict_list(csv))
        flattened = list(chain.from_iterable(rec))
        self.dicts_to_csv_ordrd(flattened, column_lst, destnm)