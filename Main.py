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
from cvxopt import matrix, solvers, spdiag
from sklearn.preprocessing import MinMaxScaler

col_clientes = ['Cliente','x coordinate','y coordinate', 'Demanda']
col_depositos = ['Deposito','x coordinate','y coordinate','Capacity']
col_vehiculos = ['Registration Category','Registration Term','Purpose of Use','Body Shape','Year of Manufacture','Make','Model','Colour','Fuel Type','Number of Cylinders','Number of Seats','ATM Weight','GCM Weight','GTM Weight','GVM Weight','TARE Weight','VIN Prefix']

data_cl  = pd.read_csv("Customers.csv", sep=',', names=col_clientes, encoding='latin-1')
data_de  = pd.read_csv("Deposits.csv", sep=',', names=col_depositos, encoding='latin-1')
data_ve  = pd.read_csv("Vehicles.csv", sep=',', names=col_vehiculos,  encoding='latin-1')

data_clientes  = data_cl[0:300]
data_depositos = data_de
data_vehiculos = data_ve


# Matrix de Distancias entre clientes
dfcc = pd.DataFrame(data_clientes[['x coordinate', 'y coordinate']].values, columns=['x coordinate', 'y coordinate'])
mdcc = pd.DataFrame(distance_matrix(dfcc.values, dfcc.values), index=data_clientes['Cliente'], columns=data_clientes['Cliente'])
# Matrix de Distancias de Depositos a Clientes.
dfd  = pd.DataFrame(data_depositos[['x coordinate', 'y coordinate']].values, columns=['x coordinate', 'y coordinate'])
dfc  = pd.DataFrame(data_clientes[['x coordinate', 'y coordinate']].values, columns=['x coordinate', 'y coordinate'])
mddc = pd.DataFrame(distance_matrix(dfd.values, dfc.values), index=data_depositos['Deposito'], columns=data_clientes['Cliente'])
# Matrix de Distancia de Clientes a Depositos.
dfc  = pd.DataFrame(data_clientes[['x coordinate', 'y coordinate']].values, columns=['x coordinate', 'y coordinate'])
dfd  = pd.DataFrame(data_depositos[['x coordinate', 'y coordinate']].values, columns=['x coordinate', 'y coordinate'])
mdcd = pd.DataFrame(distance_matrix(dfc.values, dfd.values), index=data_clientes['Cliente'], columns=data_depositos['Deposito'])

# PARAMETROS GENERALES DEL P.L.
# Costo fijo de los vehiculos.
cfv =  2428.90 # Costo fijo de los vehiculos. ejemplo : $ 5'400.000 pesos colombianos -> Dolar Australiano como es flota homogenea corresponde al mismo

# Lista de costo por kilometro de los vehiculos.
ckv =   0.03 # Costo por kilometro de los vehiculos como es flota homogenea corresponde al mismo.

# Lista del factor de velocidad de los vehiculos.
fvv = 109 # Factor de velocidad de los vehiculos 109 Km/h -> 2600 RPM.como es flota homogenea corresponde al mismo.

# Lista de matrices de costo en funcion de la distancia recorrida
# para cada vehiculo V para viajar de cliente a cliente.
mdcc_ckv = pd.DataFrame(mdcc * ckv )
# Lista de matrices de costo en funcion de la distancia recorrida para cada vehiculo V para viajar de deposito a cliente.
mddc_ckv = pd.DataFrame(mddc * ckv )
# Lista de matrices de costo en funcion de la distancia recorrida  para cada vehiculo V para viajar de cliente a deposito.
mdcd_ckv = pd.DataFrame(mdcd * ckv )
# Capacidad del Deposito para almacenar en metros cuadrados
capacity_d = data_depositos['Capacity'].values
# Demanda de cada cliente
demanda =  data_clientes['Demanda'].values
# Capacidad Carga de cada vehiculo
capacity_v =  data_vehiculos['GVM Weight'].values

H = []
[H.append(p) for p in range(1, len(data_clientes)+1)]

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
# Di Demanda del cliente j
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



# s.a: - Restricciones:

def supply_rule(modelo, i):
 return sum(modelo.x[i,j] for j in modelo.j) <= modelo.d[i]

modelo.supply = Constraint(modelo.i, rule=supply_rule, doc='No exceder la capacidad de cada fabricante i')



#Funcion Objetivo:

def objective_rule(modelo):
 return sum(cfv*modelo.x[i,j,k] for i in modelo.i for j in modelo.j for k in modelo.k)

modelo.objective = Objective(rule=objective_rule, sense=minimize, doc='FunciÃ³n objetivo')



# Funcion para llamar al solucionador de problema (NEOS)

instance = modelo
opt = SolverFactory("cbc") #cbc -cplex
solver_manager = SolverManagerFactory('neos')
results = solver_manager.solve(instance, opt=opt)
results.write()
modelo.x.display()
modelo.objective.display()





