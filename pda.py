# -*- coding: UTF-8 -*-
import analysis
import functions
import pandas
import recoding
import  lfunctions
import psycopg2.extras
import matplotlib.pyplot
import matplotlib.patches

# dtf = pd.read_sql_query('select * from hechos limit 1;', functions.psycodb)
data1 = analysis.freqs_by_values_of_2cols('victimas', 'causa', 'tipo_recod')
data2 = analysis.freqs_by_values_of_2cols('victimas', 'causa', 'sexo')
dtf = pandas.DataFrame(data1, columns=['causa', 'sexo', 'f. abs.', 'f.perc.'])
dtfb = pandas.DataFrame(data2, columns=['causa', 'sexo', 'f. abs.', 'f.perc.'])

f = [dtf, dtfb]
dtfc = pandas.concat(f)

# dtfc.to_excel('test.xlsx', sheet_name='vic c s')
# dtf.to_csv('test.csv', encoding='utf-8')
# print(dtfc)

dtg = dtf.plot.bar(title='Víctimas por gravedad y sexo', color='g')
labels = ['Homicidio Femeninio','Homicidio Masculino','Homicidio Sin Datos','Lesiones Femenino','Lesiones Masculino', 'Lesiones Sin Datos']
matplotlib.pyplot.xticks(range(len(dtf)), labels, rotation='horizontal')
matplotlib.pyplot.ylabel('Cantidad')
matplotlib.pyplot.xlabel('Grupo')
green_patch = matplotlib.patches.Patch(color='green', label='Nro. de víctimas')
matplotlib.pyplot.legend(handles=[green_patch])
matplotlib.pyplot.show(dtg)
