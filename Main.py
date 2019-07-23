# -*- coding: utf-8 -*-
import re
import pyomo
from pyomo.environ import *
from Utils import *

# Parametros:

# N Número de vehículos
# Cij Costos entre los nodos i y j
# Wi Capacidad del depósito
# Di Demanda del cliente j
# Qk Capacidad del vehículo (ruta) k
# l cardinalidad de los depositos.
# m cardinalidad del conjunto de vehiculos.
# n cardinalidad del conjunto de nodos.

d = []
[d.append(p) for p in range(1, len(data_depositos)+1)]
c = []
[c.append(p) for p in range(1, len(data_clientes)+1)]
v = []
[v.append(p) for p in range(1, len(data_vehiculos)+1)]

# Capacidad del depósito (Wi)
W = []
[W.append(p) for p in data_depositos]
# Demanda del cliente (Dj)
D = []
[D.append(p) for p in data_clientes]
# Capacidad del Vehiculo (Qk)
Q = []
[Q.append(p) for p in data_vehiculos]

l = len(d)
n = len(c) 
m = len(v)



# Dominio del Modelo - MDVRP

# I Conjunto de depósitos
# J Conjunto de clientes
# K Conjunto de vehículos

modelo = ConcreteModel()

modelo.i = Set(initialize=d, doc='Deposito')
modelo.j = Set(initialize=c, doc='Cliente')
modelo.k = Set(initialize=v, doc='Vehiculo')


#V.Decision:

# Xijk : Variable binaria que indica que el nodo i precede al nodo j en la ruta k. 
# Zij : Variable binaria que define si el consumidor ubicado en el nodo j es atendido por el centro de distribución i.
# Ulk : Variable auxiliar usada en las restricciones de eliminación de sub-toures en la ruta k.

modelo.x = Var(modelo.i, modelo.j, modelo.k, within= Binary, bounds=(0.0,None), doc='Variable binaria que indica que el nodo i precede al nodo j en la ruta k')

modelo.z = Var(modelo.i, modelo.j, within= Binary, bounds=(0.0,None), doc='Variable binaria que define si el consumidor ubicado en el nodo j es atendido por el centro de distribución i.')

modelo.u = Var(modelo.j, modelo.k, within= NonNegativeReals, bounds=(0.0,None), doc='Variable auxiliar usada en las restricciones de eliminación de sub-toures en la ruta k.')



# s.a: - Restricciones:

def X_ijk_rule(modelo, i):
 return sum(modelo.x[i,j,k] for j in modelo.j for k in modelo.k) == 1
modelo.X_ijk = Constraint(modelo.i, rule=X_ijk_rule, doc='Cada cliente j debe ser asignado a un vehiculo K')


#def Q_k_rule(modelo, i, D ):
# return sum(D[j]*modelo.x[i,j,k] for j in modelo.j for k in modelo.k) <= (modelo.u[k] for k in modelo.k)
#modelo.Q_k = Constraint(modelo.i, D, rule=Q_k_rule, doc='Capacidad del conjunto de vehiculos K')


def X_ijk_X_jik_rule(modelo, i):
 return sum(modelo.x[i,j,k] for j in modelo.j for k in modelo.k ) - sum(modelo.xx[j,i,k] for j in modelo.j for k in modelo.k ) == 0
modelo.X_ijk_X_jik_rule = Constraint(modelo.i,  rule=X_ijk_X_jik_rule , doc='Conservacion de Flujos')

def X_ijk__rule(modelo, i):
 return sum(modelo.x[i,j,k] for j in modelo.j for k in modelo.k) <= 1
modelo.X_ijk__ = Constraint(modelo.i, rule=X_ijk__rule, doc='Garantiza que cada vehiculo atienda almenos una unica ruta')



#Funcion Objetivo:

def objective_rule(modelo):
 return sum(cfv*modelo.x[i,j,k] for i in modelo.i for j in modelo.j for k in modelo.k)

modelo.objective = Objective(rule=objective_rule, sense=minimize, doc='FunciÃ³n objetivo')







#for a in modelo.x:
#  print(a)
 # print("\n")



