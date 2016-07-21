# -*- coding: UTF-8 -*-
import functions
import recoding
import analysis

class DbPfDg:


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