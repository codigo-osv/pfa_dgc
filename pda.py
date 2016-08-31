# -*- coding: UTF-8 -*-
import six
import analysis
import functions
import pandas
import recoding
import  lfunctions
import psycopg2.extras
import matplotlib.pyplot as plt
import matplotlib.patches


# dtf = pandas.read_sql_query('select id, anio from hechos limit 10;', functions.psycodb)
# print(dtf)

# data1 = analysis.freqs_by_values_of_2cols('victimas', 'causa', 'tipo_recod')
# data2 = analysis.freqs_by_values_of_2cols('victimas', 'causa', 'sexo')
# dtf = pandas.DataFrame(data1, columns=['causa', 'sexo', 'f. abs.', 'f.perc.'])
# dtfb = pandas.DataFrame(data2, columns=['causa', 'sexo', 'f. abs.', 'f.perc.'])

# f = [dtf, dtfb]
# dtfc = pandas.concat(f)

# dtfc.to_excel('test.xlsx', sheet_name='vic c s')
# dtf.to_csv('test.csv', encoding='utf-8')
# print(dtf)


# dtg = dtf.plot.bar(title='Víctimas por gravedad y sexo', color='g')
# labels = ['Homicidio Femeninio','Homicidio Masculino','Homicidio Sin Datos','Lesiones Femenino','Lesiones Masculino', 'Lesiones Sin Datos']
# matplotlib.pyplot.xticks(range(len(dtf)), labels, rotation='horizontal')
# matplotlib.pyplot.ylabel('Cantidad')
# matplotlib.pyplot.xlabel('Grupo')
# green_patch = matplotlib.patches.Patch(color='green', label='Nro. de víctimas')
# matplotlib.pyplot.legend(handles=[green_patch])
# matplotlib.pyplot.show(dtg)


# color=['bgrymkwc'] list of different colors that can be used together
# template vertical bar with categorical variable in the x axis
# data = analysis.freqabs_by_values_of_1col('hechos', 'anio')
# data1 = functions.sort_by_num_lst(data, 0)
# dtf = pandas.DataFrame([x[1] for x in data1], columns=['Cantidad de Siniestros'], index=[x[0] for x in data1])
# dtg = dtf.plot.bar(title='Cantidad de siniestros viales por año', color='r')
# dtg.legend().set_visible(True)
# # dtg.legend(loc='upper left', numpoints = 1)
# dtg.grid(True, color='gray', linestyle='solid')
# dtg.set_axisbelow(True)
# # labels = ['2006','2007','2008','2009','2010', '2011', '2012', '2013', '2014', '2015']
# # plt.xticks(range(len(dtf)), labels, rotation='horizontal')
# plt.ylabel('Cantidad')
# plt.xlabel('Año')
# plt.show(dtg)


# template pie bar with categorical variable
plt.rcParams["figure.facecolor"]='white'
plt.rcParams["axes.facecolor"]='white'
plt.rcParams["savefig.facecolor"]='white'
data2 = pandas.read_sql_query('select sexo, count(*) as Cantidad from victimas group by sexo;',
                              functions.psycodb, index_col='sexo')
dtg2 = data2.plot.pie(title='Porcentaje de víctimas según sexo', labels=['Sin datos', 'Masculino', 'Femenino'],
                      y='cantidad', colors='rcg', autopct='%.0f%%', fontsize=15, pctdistance=0.85)
plt.ylabel('Porcentaje', fontsize=10)
dtg2.set_aspect('equal')
# plt.show(dtg2)
# plt.savefig('pie.png')