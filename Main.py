# -*- coding: utf-8 -*-
import re
import pyomo
import pandas as pd
import numpy as np
import seaborn as sb
from copy import deepcopy
from pyomo.environ import *
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from scipy.spatial import distance_matrix
from sklearn.preprocessing import MinMaxScaler


col_clientes = ['Cliente','x coordinate','y coordinate', 'Demanda']
col_depositos = ['Deposito','x coordinate','y coordinate','Capacity']
col_vehiculos = ['Registration Category','Registration Term','Purpose of Use','Body Shape','Year of Manufacture','Make','Model','Colour','Fuel Type','Number of Cylinders','Number of Seats','ATM Weight','GCM Weight','GTM Weight','GVM Weight','TARE Weight','VIN Prefix']
data_clientes = pd.read_csv("Customers.csv", sep=',', names=col_clientes, encoding='latin-1')
data_depositos = pd.read_csv("Deposits.csv", sep=',', names=col_depositos, encoding='latin-1')
data_vehiculos = pd.read_csv("Vehicles.csv", sep=',', names=col_vehiculos,  encoding='latin-1')

# Se crea la matrix de puntos
c_latitud  =  data_clientes['x coordinate'].values
c_longitud =  data_clientes['y coordinate'].values
d_latitud  =  data_depositos['x coordinate'].values
d_longitud =  data_depositos['y coordinate'].values
capacity_d = data_depositos['Capacity'].values
demanda =  data_clientes['Demanda'].values
capacity_v =  data_vehiculos['GVM Weight'].values

# Lista de costo fijo de los vehiculos.
cfv     =   [2428.90, 2428.90, 2428.90, 2428.90, 2428.90, 2428.90, 2428.90, 2428.90, 2428.90, 2428.90, 2428.90, 2428.90, 2428.90, 2428.90, 2428.90, 2428.90, 2428.90, 2428.90, 2428.90, 2428.90, ] # Se crea vector de costo fijo de los vehiculos. ejemplo : $ 5'400.000 pesos colombianos -> Dolar Australiano 
# Lista de costo por kilometro de los vehiculos.
ckv     =   [0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03 ] # Se crea vector de costo por kilometro de los vehiculos.
# Lista del factor de velocidad de los vehiculos.
fvv     =   [109, 109, 109, 109, 109, 109, 109, 109, 109, 109, 109, 109, 109, 109, 109, 109, 109, 109, 109, 109 ] # Se crea vector de factor de velocidad de los vehiculos 109 Km/h -> 2600 RPM.

# Lista de matrices de costo en funcion de la distancia recorrida
# para cada vehiculo V para viajar de cliente a cliente.
for i in range (len(ckv)):
    mdcc_ckv = pd.DataFrame(mdcc * ckv[i] )
# Lista de matrices de costo en funcion de la distancia recorrida
# para cada vehiculo V para viajar de deposito a cliente.
for i in range (len(ckv)):
    mddc_ckv = pd.DataFrame(mddc * ckv[i] )
# Lista de matrices de costo en funcion de la distancia recorrida
# para cada vehiculo V para viajar de cliente a deposito.
for i in range (len(ckv)):
    mdcd_ckv = pd.DataFrame(mdcd * ckv[i] )

X = np.array(list(zip(c_latitud[0:50], c_longitud[0:50])))
Y = np.array(list(zip(d_latitud,d_longitud)))
H = []
[H.append(p) for p in range(1, len(X)+1)]
#W = range(1, len(X)-1)

# Dominio del Modelo - MDVRP

# I Conjunto de depósitos
# J Conjunto de clientes
# K Conjunto de vehículos


modelo = ConcreteModel()
modelo.i = Set(initialize=['D1','D2','D3','D4','D5','D6','D7','D8','D9','D10'], doc='Deposito')
modelo.j = Set(initialize=H, doc='Cliente')
modelo.k = Set(initialize=['1','2','3','4','5','6','7','8','9','10'], doc='Vehiculo')

# Parametros:

# N Número de vehículos
# Cij Costos entre los nodos i y j
# Wi Capacidad del depósito
# di Demanda del cliente j
# Qk Capacidad del vehículo (ruta) k
# l cardinalidad de los depositos.
# m cardinalidad del conjunto de vehiculos.
# n cardinalidad del conjunto de nodos.

l = len(data_depositos)
N = len(data_vehiculos)
modelo.w = Param(modelo.i, initialize=capacity_d, doc='Capacidad del depósito (Wi)')
modelo.d = Param(modelo.j, initialize=demanda, doc='Demanda del cliente (Dj)')
modelo.q = Param(modelo.k, initialize=capacity_v, doc='Capacidad del Vehiculo (Qk)')

#V.Decision:

# Xijk : Variable binaria que indica que el nodo i precede al nodo j en la ruta k. 
# Zij : Variable binaria que define si el consumidor ubicado en el nodo j es atendido por el centro de distribución i.
# Ulk : Variable auxiliar usada en las restricciones de eliminación de sub-toures en la ruta k.

modelo.x = Var(modelo.i, modelo.j, modelo.k, within= Binary, bounds=(0.0,None), doc='Variable binaria que indica que el nodo i precede al nodo j en la ruta k')

modelo.z = Var(modelo.i, modelo.j, within= Binary, bounds=(0.0,None), doc='Variable binaria que define si el consumidor ubicado en el nodo j es atendido por el centro de distribución i.')

modelo.u = Var(modelo.i, modelo.j, within= Binary, bounds=(0.0,None), doc='Variable auxiliar usada en las restricciones de eliminación de sub-toures en la ruta k.')


#Funcion Objetivo:

def objective_rule(modelo):
 return sum(modelo.C[i,j]*modelo.x[i,j] for i in modelo.i for j in modelo.j)

modelo.objective = Objective(rule=objective_rule, sense=minimize, doc='FunciÃ³n objetivo')

