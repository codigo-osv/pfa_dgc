# -*- coding: UTF-8 -*-
import csv
from itertools import chain

import pandas
from psycopg2._psycopg import AsIs
import functions
import recoding


class Normalize_PFA:

    def __init__(self, csv_path):
        self.csv_path = csv_path
        self.aux_csv = AuxFCSV()

    def process_csv(self):
        dict_lst = functions.csv_to_dict_list(self.csv_path)
        dict_lst = self.normalize_accidents_ids(dict_lst)
        dict_lst = self.normalize_initial_values_lst(dict_lst)
        self.gen_accidents_table(dict_lst)
        self.gen_victims_table(dict_lst)
        self.gen_accused_table(dict_lst)

    @staticmethod
    def normalize_accidents_ids(dict_lst):
        # query = functions.db.query('select max(id) from hechos')
        # newid = int(query.all().__getitem__(0)[0])
        cur = functions.psycodb.cursor()
        cur.execute('select max(id) from hechos')
        newid = int(cur.fetchone()[0])
        rec = {}
        res = []
        for adict in dict_lst:
            original_id = adict['ID']
            if original_id in rec.keys():
                newid = rec[original_id]
            else:
                newid += 1
                rec[original_id] = newid
            adict['ID'] = str(newid)
            res.append(adict)
        return res

    def normalize_initial_values_lst(self, dict_lst):
        res = []
        for adict in dict_lst:
            dn = self.normalize_initial_values(adict)
            res.append(dn)
        return res

    @staticmethod
    def normalize_initial_values(adict):
        for key in adict.keys():
            if recoding.is_no_data(adict[key]):
                adict[key] = ''
            elif adict[key] == 'AVENIDA + AUTOPISTA':
                adict[key] = 'AUTOPISTA'
            elif adict[key] == 'AUTO (no se especifica si es particular o de alquiler)':
                adict[key] = 'AUTO'
            elif adict[key] == 'AUTO PFA / MOVIL / GENDARMERIA / METROPOLITANA / MOTO MOVIL':
                adict[key] = 'FUERZA SEGURIDAD'
            elif adict[key] == 'CONDUCTOR (A/P-A/A-MOTO-CICLOMOTOR-T/P-CAMION-UTILITARIO)':
                adict[key] = 'CONDUCTOR'
            elif adict[key] == 'PASAJERO/ACOMPAÑANTE (A/P-A/A-MOTO-CICLOMOTOR-T/P-CAMION-UTILITARIO)':
                adict[key] = 'PASAJERO'
            elif 'PASAJERO/ACOMPAÑANTE' in adict[key]:
                adict[key] = adict[key].replace('PASAJERO/ACOMPAÑANTE', 'PASAJERO')
            elif 'PASAJERO/ ACOMPAÑANTE' in adict[key]:
                adict[key] = adict[key].replace('PASAJERO/ ACOMPAÑANTE', 'PASAJERO')
            elif 'PASAJERO/ACOMPAïż½ANTE' in adict[key]:
                adict[key] = adict[key].replace('PASAJERO/ACOMPAïż½ANTE', 'PASAJERO')
            elif 'PASAJERO/ ACOMPAïż½ANTE' in adict[key]:
                adict[key] = adict[key].replace('PASAJERO/ ACOMPAïż½ANTE', 'PASAJERO')
        return adict

    def gen_accidents_table(self, rows):
        res1 = []
        res2 = []
        # create a tuple with the fields of each row to compare and check them to avoid adding duplicate entries
        for case in rows:
            comp = case['ID']
            if comp not in res1:
                res1.append(comp)
                formatted = {"orden": case['ORDEN'], "id": comp, "mes": case['PERIODO'], "comisaria": case['COMISARIA'],
                             "fecha": case['FECHA'],
                             "hora": case['HORA'], "tipo_colision": case['TIPO_COLISION'],
                             "tipo_hecho": case['TIPO_HECHO'], "lugar_hecho": case['LUGAR_DEL_HECHO'],
                             "direccion_normalizada": case['Dirección Normalizada'],
                             "tipo_calle": case['TIPO_DE_CALLE'],
                             "direccion_normalizada_arcgis": case['Dirección Normalizada (ArcGIS)'],
                             "calle1": case['Calle'], "altura": case['Altura'],
                             "calle2": case['Cruce'], "codigo_calle": case['Código de Calle'],
                             "codigo_cruce": case['Código de Cruce'],
                             "geocodificacion": case['Geocodificación']}
                res2.append(formatted)
        ordrd_cols = ["orden", "id", "mes", "comisaria", "fecha", "hora", "tipo_colision", "tipo_hecho", "lugar_hecho",
                      "direccion_normalizada", "tipo_calle",
                      "direccion_normalizada_arcgis", "calle1", "altura", "calle2", "codigo_calle", "codigo_cruce",
                      "geocodificacion"]
        self.aux_csv.dicts_to_csv_ordrd(res2, ordrd_cols, 'hechos')

    def gen_victims_table(self, rows):
        res1 = []
        res2 = []
        # query = functions.db.query('select max(id) from victimas')
        # lstid = int(query.all().__getitem__(0)[0])
        cur = functions.psycodb.cursor()
        cur.execute('select max(id) from victimas')
        lstid = int(cur.fetchone()[0])
        # create a tuple with the fields of each row to compare and check them to avoid adding duplicate entries
        for case in rows:
            cmp_dup = (case['ID'], case['CAUSA'], case['EDAD_VICTIMA'], case['SEXO_VICTIMA'], case['VICTIMA'],
                       case['TIPO_VEHICULO_VICTIMA'], case['MARCA_VEHICULO_VICTIMA'], case['MODELO_VEHICULO_VICTIMA'])
            cmp_emp = (case['CAUSA'], case['EDAD_VICTIMA'], case['SEXO_VICTIMA'], case['VICTIMA'],
                       case['TIPO_VEHICULO_VICTIMA'],
                       case['MARCA_VEHICULO_VICTIMA'], case['MODELO_VEHICULO_VICTIMA'], case['COLECTIVO_VICTIMA'],
                       case['INTERNO_VICTIMA'])
            if not ((cmp_dup in res1) or (self.aux_csv.blank_fields(cmp_emp))):
                lstid += 1
                res1.append(cmp_dup)
                formatted = {"id_hecho": case['ID'], "causa": case['CAUSA'], "rol": case['VICTIMA'],
                             "tipo": case['TIPO_VEHICULO_VICTIMA'], "marca": case['MARCA_VEHICULO_VICTIMA'],
                             "modelo": case['MODELO_VEHICULO_VICTIMA'], "colectivo": case['COLECTIVO_VICTIMA'],
                             "interno_colectivo": case['INTERNO_VICTIMA'], "sexo": case['SEXO_VICTIMA'],
                             "edad": case['EDAD_VICTIMA'], "sumario": case['SRIO_NRO'], "id": lstid}
                res2.append(formatted)
        ordrd_cols = ["id_hecho", "causa", "rol", "tipo", "marca", "modelo", "colectivo", "interno_colectivo", "sexo",
                      "edad", "sumario", "id"]
        self.aux_csv.dicts_to_csv_ordrd(res2, ordrd_cols, 'victimas')

    def gen_accused_table(self, rows):
        res1 = []
        res2 = []
        # query = functions.db.query('select max(id) from acusados')
        # lstid = int(query.all().__getitem__(0)[0])
        cur = functions.psycodb.cursor()
        cur.execute('select max(id) from acusados')
        lstid = int(cur.fetchone()[0])
        # create a tuple with the fields of each row to compare and check them to avoid adding duplicate entries
        for case in rows:
            cmp_dup = (case['ID'], case['CAUSA'], case['EDAD_ACUSADO'], case['SEXO_ACUSADO'], case['ACUSADO'],
                       case['TIPO_VEHICULO_ACUSADO'], case['MARCA_VEHICULO_ACUSADO'], case['MODELO_VEHICULO_ACUSADO'])
            cmp_emp = (case['CAUSA'], case['EDAD_ACUSADO'], case['SEXO_ACUSADO'], case['ACUSADO'],
                       case['TIPO_VEHICULO_ACUSADO'],
                       case['MARCA_VEHICULO_ACUSADO'], case['MODELO_VEHICULO_ACUSADO'],
                       case['COLECTIVO_ACUSADO'], case['INTERNO_ACUSADO'])
            if not ((cmp_dup in res1) or (self.aux_csv.blank_fields(cmp_emp))):
                lstid += 1
                res1.append(cmp_dup)
                formatted = {"id_hecho": case['ID'], "rol": case['ACUSADO'], "tipo": case['TIPO_VEHICULO_ACUSADO'],
                             "marca": case['MARCA_VEHICULO_ACUSADO'],
                             "modelo": case['MODELO_VEHICULO_ACUSADO'], "colectivo": case['COLECTIVO_ACUSADO'],
                             "interno_colectivo": case['INTERNO_ACUSADO'],
                             "sexo": case['SEXO_ACUSADO'], "edad": case['EDAD_ACUSADO'], "id": lstid}
                res2.append(formatted)
        ordrd_cols = ["id_hecho", "rol", "tipo", "marca", "modelo", "colectivo", "interno_colectivo", "sexo", "edad",
                      "id"]
        self.aux_csv.dicts_to_csv_ordrd(res2, ordrd_cols, 'acusados')

    def upd_xy(self):
        dict_lst = functions.csv_to_dict_list(self.csv_path)
        cur = functions.psycodb.cursor()
        for adict in dict_lst:
            cur.execute("update hechos set %s = %s, %s = %s where id = %s;",
                        (AsIs('x'), adict['POINT_X'], AsIs('y'), adict['POINT_Y'], adict['id']))
            functions.psycodb.commit()


class AuxFCSV:

    @staticmethod
    def blank_fields(str_fields):
        res = ''
        for field in str_fields:
            res += field
        return (res.__len__() == 0) | res.isspace()

    @staticmethod
    def dicts_to_csv_ordrd(row_dict_list, column_lst, destnm):
        # precondition: all rows have the same columns
        destf = destnm + '.csv'
        with open(destf, 'w') as fh:
            wr = csv.DictWriter(fh, fieldnames=column_lst, delimiter=',', extrasaction='ignore', lineterminator='\n')
            wr.writeheader()
            for row in row_dict_list:
                wr.writerow(row)

    def merge_csvs_ordrd(self, column_lst, destnm, *csv_path):
        # precondition: all csvs and all rows have the same columns
        rec = []
        for fcsv in csv_path:
            rec.append(functions.csv_to_dict_list(fcsv))
        flattened = list(chain.from_iterable(rec))
        self.dicts_to_csv_ordrd(flattened, column_lst, destnm)


class PdaUtils:

    @staticmethod
    def dframes_to_excel_sheets(data_frames, sheet_names, file_name):
        # precondition: [data_frames].size() = [sheet_names].size()
        ct = 0
        with pandas.ExcelWriter(file_name + '.xlsx') as writer:
            for df in data_frames:
                df.to_excel(writer, sheet_name=sheet_names[ct], index=False)
                ct += 1
