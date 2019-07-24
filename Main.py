# -*- coding: utf-8 -*-
import re
import pyomo
from pyomo.environ import *
from Utils import *



# Dominio del Modelo - MDVRP

modelo = ConcreteModel()



# Parametros:

# I Conjunto de depósitos
# J Conjunto de clientes
# K Conjunto de vehículos

# N Número de vehículos
# Cij Costos entre los nodos i y j
# l cardinalidad de los depositos.
# m cardinalidad del conjunto de vehiculos.
# n cardinalidad del conjunto de nodos.


modelo.i = Set(initialize=d, doc='Deposito')
modelo.j = Set(initialize=c, doc='Cliente')
modelo.k = Set(initialize=v, doc='Vehiculo')

# Wi Capacidad del depósito
# Di Demanda del cliente j
# Qk Capacidad del vehículo (ruta) k

modelo.w = Param(modelo.i, initialize=lambda modelo, i: W[i-1])
modelo.d = Param(modelo.j, initialize=lambda modelo, j: D[j-1])
modelo.q = Param(modelo.k, initialize=lambda modelo, k: Q[k-1])


print("-------------Depositos-----------------")
for y in modelo.w:
  print(modelo.w[y]) 
print("-------------Clientes------------------")
for y in modelo.d:
  print(modelo.d[y]) 
print("-------------Vehiculos-----------------")
for y in modelo.q:
  print(modelo.q[y]) 



#V.Decision:

# Xijk : Variable binaria que indica que el nodo i precede al nodo j en la ruta k. 
# Zij : Variable binaria que define si el consumidor ubicado en el nodo j es atendido por el centro de distribución i.
# Ulk : Variable auxiliar usada en las restricciones de eliminación de sub-toures en la ruta k.

modelo.x = Var(modelo.i, modelo.j, modelo.k, within= Binary, bounds=(0.0,None), doc='Variable binaria que indica que el nodo i precede al nodo j en la ruta k')

modelo.xx = Var(modelo.j, modelo.i, modelo.k, within= Binary, bounds=(0.0,None), doc='Variable binaria que indica que el nodo j precede al nodo i en la ruta k')

modelo.z = Var(modelo.i, modelo.j, within= Binary, bounds=(0.0,None), doc='Variable binaria que define si el consumidor ubicado en el nodo j es atendido por el centro de distribución i.')

modelo.u = Var(modelo.j, modelo.k, within= NonNegativeReals, bounds=(0.0,None), doc='Variable auxiliar usada en las restricciones de eliminación de sub-toures en la ruta k.')



# s.a: - Restricciones:

def X_ijk_rule(modelo, i):
 return sum(modelo.x[i,j,k] for j in modelo.j for k in modelo.k) == 1
modelo.X_ijk = Constraint(modelo.i, rule=X_ijk_rule, doc='Cada cliente j debe ser asignado a un vehiculo K')


def Q_k_rule(modelo, i, k):
 return sum(modelo.x[i,j,k] for j in modelo.j for k in modelo.k) <= modelo.q[k]
modelo.Q_k = Constraint(modelo.i, modelo.k,  rule=Q_k_rule, doc='Capacidad del conjunto de vehiculos K')


def X_ijk_X_jik_rule(modelo, i):
 return sum(modelo.x[i,j,k] for j in modelo.j for k in modelo.k ) - sum(modelo.xx[j,i,k] for j in modelo.j for k in modelo.k ) == 0
modelo.X_ijk_X_jik_rule = Constraint(modelo.i,  rule=X_ijk_X_jik_rule , doc='Conservacion de Flujos')

def X_ijk__rule(modelo, i):
 return sum(modelo.x[i,j,k] for j in modelo.j for k in modelo.k) <= 1
modelo.X_ijk__ = Constraint(modelo.i, rule=X_ijk__rule, doc='Garantiza que cada vehiculo atienda almenos una unica ruta')

#def W_i_rule(modelo, i , W):
# return sum(modelo.z[i,j] for j in modelo.j)  <= sum(W[i])
#modelo.W_i = Constraint(modelo.i, W,  rule=W_i_rule, doc='Capacidad de los depositos i')

#(D[j] for j in modelo.j)*  W[i] 


#Funcion Objetivo:

def objective_rule(modelo):
 return sum(cfv*modelo.x[i,j,k] for i in modelo.i for j in modelo.j for k in modelo.k)

modelo.objective = Objective(rule=objective_rule, sense=minimize, doc='FunciÃ³n objetivo')






#for a in modelo.x:
#  print(a)
 # print("\n")





