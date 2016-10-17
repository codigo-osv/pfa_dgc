# -*- coding: UTF-8 -*-
import analysis
import functions
import pandas
import recoding
import  lfunctions
import psycopg2.extras
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

dtf1 = pandas.read_sql_query('select * from hechos;', functions.psycodb)
dtf2 = pandas.read_sql_query('select * from victimas order by id_hecho;', functions.psycodb)
dtf3 = pandas.read_sql_query('select * from acusados order by id_hecho;', functions.psycodb)
with pandas.ExcelWriter('base_pfa_2006-15.xlsx') as writer:
    dtf1.to_excel(writer, sheet_name='Siniestros', index=False)
    dtf2.to_excel(writer, sheet_name='Víctimas', index=False)
    dtf3.to_excel(writer, sheet_name='Acusados', index=False)

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
# labels = ['Homicidio Femeninio','Homicidio Masculino','Homicidio Sin Datos','Lesiones Femenino',
#           'Lesiones Masculino', 'Lesiones Sin Datos']
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

# template 2x3 categorical horizontal bars
# d2014_15 = pandas.read_sql_query('select anio, sexo, count(*) as Cantidad from victimas join hechos on '
#                                 'victimas.id_hecho = hechos.id where anio = 2014 or anio = 2015 '
#                                 'group by anio, sexo order by anio, sexo;',
#                                 functions.psycodb, index_col='anio')
#
# labels = ['2014 Femenino','2014 Masculino','2014 Sin datos','2015 Femenino','2015 Masculino', '2015 Sin datos']
# plt.rcParams["figure.facecolor"]='white'
# plt.rcParams["axes.facecolor"]='lightgray'
# plt.rcParams["savefig.facecolor"]='white'
# plt.rcParams['figure.figsize'] = 15, 10
# dtg = d2014_15.plot.barh(title='Número de víctimas según sexo. Años 2014 y 2015.', color=['bgm'])
# plt.yticks(range(len(d2014_15)), rotation='horizontal')
# dtg.grid(True, color='gray', linestyle='solid')
# dtg.legend(loc='upper right')
# blue_patch = mpatches.Patch(color='b', label='Femenino')
# green_patch = mpatches.Patch(color='g', label='Masculino')
# pur_patch = mpatches.Patch(color='m', label='Sin datos')
# plt.legend(handles=[blue_patch, green_patch, pur_patch])
# plt.ylabel('Año')
# plt.xlabel('Cantidad')
# dtg.set_axisbelow(True)
# # plt.show(dtg)
# plt.savefig('horizontal_bars.png', dpi=199, frameon=True)

# template pie bar with categorical variable
# plt.rcParams["figure.facecolor"]='white'
# plt.rcParams["axes.facecolor"]='white'
# plt.rcParams["savefig.facecolor"]='white'
# data2 = pandas.read_sql_query('select sexo, count(*) as Cantidad from victimas group by sexo;',
#                               functions.psycodb, index_col='sexo')
# dtg2 = data2.plot.pie(title='Porcentaje de víctimas según sexo', labels=['Sin datos', 'Masculino', 'Femenino'],
#                       y='cantidad', colors='rcg', autopct='%.0f%%', fontsize=15, pctdistance=0.85)
# plt.ylabel('Porcentaje', fontsize=10)
# dtg2.set_aspect('equal')
# # plt.show(dtg2)
# # plt.savefig('pie.png')