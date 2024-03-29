# -*- coding: utf-8 -*-
import re
import pyomo as pyo
#from pyomo.environ as pyo
from pyomo.environ import *
from Utils import *
from time import time #importamos la función time para capturar tiempos


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

print("- Parametros:","\n")
modelo.i = Set(initialize=d, doc='Deposito')
modelo.j = Set(initialize=c, doc='Cliente')
modelo.k = Set(initialize=v, doc='Vehiculo')
modelo.u = Set(initialize=c, doc='Ruta Clientes')

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
print("-------------Vehiculos-----------------","\n")
for y in modelo.q:
  print(modelo.q[y]) 



#V.Decision:
print("- V.Decision:","\n")

# Xijk : Variable binaria que indica que el nodo i precede al nodo j en la ruta k. 
# Zij : Variable binaria que define si el consumidor ubicado en el nodo j es atendido por el centro de distribución i.
# Ulk : Variable auxiliar usada en las restricciones de eliminación de sub-toures en la ruta k.

modelo.x = Var(modelo.i, modelo.j, modelo.k, initialize=1, within= Binary, bounds=(0.0,1), doc='Variable binaria que indica que el nodo i precede al nodo j en la ruta k')

modelo.xx = Var(modelo.j, modelo.i, modelo.k, initialize=1, within= Binary, bounds=(0.0,None), doc='Variable binaria que indica que el nodo j precede al nodo i en la ruta k')

modelo.ux = Var(modelo.j, modelo.u, modelo.k, initialize=1, within= Binary, bounds=(0.0,None), doc='Variable binaria que indica que el nodo j precede al nodo u en la ruta k')

modelo.xu = Var(modelo.u, modelo.j, modelo.k, initialize=1, within= Binary, bounds=(0.0,None), doc='Variable binaria que indica que el nodo u precede al nodo j en la ruta k')

modelo.z = Var(modelo.i, modelo.j, initialize=1, within= Binary, bounds=(0.0,None), doc='Variable binaria que define si el consumidor ubicado en el nodo j es atendido por el centro de distribución i.')

modelo.ui = Var(modelo.i, modelo.k, within= NonNegativeReals, bounds=(0.0,None), doc='Variable auxiliar usada en las restricciones de eliminación de sub-toures en la ruta k para i.')

modelo.uj = Var(modelo.j, modelo.k, within= NonNegativeReals, bounds=(0.0,None), doc='Variable auxiliar usada en las restricciones de eliminación de sub-toures en la ruta k para j.')



# s.a: - Restricciones:
print("- Restricciones:","\n")

t_inicial = time()
def X_ijk_rule(modelo, i):
 return sum(modelo.x[i,j,k] for j in modelo.j for k in modelo.k) == 1
modelo.X_ijk = Constraint(modelo.i, rule=X_ijk_rule, doc='Cada cliente j debe ser asignado a un vehiculo K')

print("·R1 X_ijk_rule·"," T. Ejecucion sg: ",(time()-t_inicial))

t_inicial = time()
def Q_k_rule(modelo, i, k):
 return sum( modelo.d[j] for j in modelo.j)*sum(modelo.x[i,j,k] for j in modelo.j for k in modelo.k) <= modelo.q[k]
modelo.Q_k = Constraint(modelo.i, modelo.k,  rule=Q_k_rule, doc='Capacidad del conjunto de vehiculos K')

print("·R2 Q_k_rule·"," T. Ejecucion sg: ",(time()-t_inicial))

t_inicial = time()
def X_ijk_X_jik_rule(modelo, i):
 return sum(modelo.x[i,j,k] for j in modelo.j for k in modelo.k ) - sum(modelo.xx[j,i,k] for j in modelo.j for k in modelo.k ) == 0
modelo.X_ijk_X_jik_rule = Constraint(modelo.i,  rule=X_ijk_X_jik_rule , doc='Conservacion de Flujos')

print("·R3 X_ijk_X_jik_rule·"," T. Ejecucion sg: ",(time()-t_inicial))

t_inicial = time()
def X_ijk__rule(modelo, i):
 return sum(modelo.x[i,j,k] for j in modelo.j for k in modelo.k) <= 1
modelo.X_ijk__ = Constraint(modelo.i, rule=X_ijk__rule, doc='Garantiza que cada vehiculo atienda almenos una unica ruta')

print("·R4 X_ijk__rule·"," T. Ejecucion sg: ",(time()-t_inicial))

t_inicial = time()
def W_i_rule(modelo, i):
 return sum(modelo.d[i]*modelo.z[i,j] for j in modelo.j)  <= modelo.w[i]
modelo.W_i = Constraint(modelo.i, rule=W_i_rule, doc='Capacidad del conjunto de depositos i')

print("·R5 W_i_rule·"," T. Ejecucion sg: ",(time()-t_inicial))

t_inicial = time() # Revisar esta restriccion de secuencia.... esto bajo subtours
def U_ij_rule(modelo, i, j, k):
 return modelo.ui[i,k] - modelo.uj[j,k] + N*modelo.x[i,j,k] <= N-1
modelo.U_ij = Constraint(modelo.i, modelo.j, modelo.k, rule=U_ij_rule, doc='Garantiza la eliminacion de SubTours')

print("·R6 U_ij_rule·"," T. Ejecucion sg: ",(time()-t_inicial))

# Un cliente puede ser asignado al deposito, unicamente si hay una ruta que parte desde el mismo deposito y transita atravez del cliente.
t_inicial = time()
def X_uk_rule(modelo, i, j):
 return  sum(modelo.ux[i,u,k] + modelo.xu[u,j,k] for j in modelo.j for k in modelo.k for u in modelo.u)  - modelo.z[i,j] <= 1 
modelo.X_uk = Constraint(modelo.i, modelo.j, rule=X_uk_rule, doc='Garantiza asignacion de cliente j si transita por depositos i')

print("·R7 X_uk_rule·"," T. Ejecucion sg: ",(time()-t_inicial))


#Funcion Objetivo: 

t_inicial = time()
def objective_rule(modelo):
 return sum(cfv*modelo.x[i,j,k] for i in modelo.i for j in modelo.j for k in modelo.k)
modelo.objective = Objective(rule=objective_rule, sense=minimize, doc='FunciÃ³n objetivo')

print("·F.O objective_rule·"," T. Ejecucion sg: ",(time()-t_inicial),"\n")

print("·················Finalizo el modelo··························","\n")


#%%
#def pyomo_postprocess(options=None, instance=None, results=None):
 # modelo.ui.display()

#print(pyomo_postprocess("threads=1", modelo, 2))
# Revisar el valor de la variable binaria....
#%%


# Funcion para llamar al solucionador de problema (NEOS)

print("·················llamada al solucionador de problema (NEOS)··························","\n")

instance = modelo
opt = SolverFactory("cplex") # cbc - cplex - glpk
solver_manager = SolverManagerFactory('neos')
results = solver_manager.solve(instance, opt=opt) ##options="threads=8")
results.write()
modelo.x.display()
modelo.objective.display()
#['bonmin', 'cbc', 'conopt', 'couenne', 'cplex', 'filmint', 'filter', 'ipopt', 'knitro', 'l-bfgs-b', 'loqo', 'minlp', 'minos', 'minto', 'mosek', 'ooqp', 'path', 'snopt']
print("················· Final de llamada al solucionador de problema (NEOS)··························","\n")

