# -*- coding: utf-8 -*-
from utils import *


# Dominio del Modelo - Vestidos

modelo = ConcreteModel()
modelo.i = Set(initialize=['Q','R','S','T'], doc='Fabricante')
modelo.j = Set(initialize=['A','B','C','D','E'], doc='Modelo')


#Vectores

modelo.Disp = Param(modelo.i, initialize={'Q':325,'R':300,'S':275,'T':275},doc='Fabricantes cuyas disponibilidades Disp(j)')

modelo.Cant = Param(modelo.j, initialize={'A':150,'B':100,'C':75,'D':250,'E':200}, doc='Demandas mÃ­nimas de vestidos de mujer Cant(i)')

#Matriz

tablac = {
('Q', 'A'): 28,
('Q', 'B'): 35,
('Q', 'C'): 43,
('Q', 'D'): 22,
('Q', 'E'): 15,

('R', 'A'): 30,
('R', 'B'): 32,
('R', 'C'): 45,
('R', 'D'): 18,
('R', 'E'): 10,

('S', 'A'): 25,
('S', 'B'): 35,
('S', 'C'): 48,
('S', 'D'): 20,
('S', 'E'): 13,

('T', 'A'): 33,
('T', 'B'): 27,
('T', 'C'): 40,
('T', 'D'): 25,
('T', 'E'): 27,
 }

modelo.C = Param(modelo.i, modelo.j, initialize=tablac, doc='Utilidades (Uij) por modelo varÃ­an de acuerdo con cada fabricante')


#V.Decision:

modelo.x = Var(modelo.i, modelo.j, bounds=(0.0,None), doc='Cantidad de modelos modelo i comprados a tienda j')




# s.a: - Restricciones:

def supply_rule(modelo, i):
 return sum(modelo.x[i,j] for j in modelo.j) <= modelo.Disp[i]

modelo.supply = Constraint(modelo.i, rule=supply_rule, doc='No exceder la capacidad de cada fabricante i')

def demand_rule(modelo, j):
 return sum(modelo.x[i,j] for i in modelo.i) >= modelo.Cant[j]

modelo.demand = Constraint(modelo.j, rule=demand_rule, doc='Satisfacer la demanda de cada modelo j')


#Funcion Objetivo:

def objective_rule(modelo):
 return sum(modelo.C[i,j]*modelo.x[i,j] for i in modelo.i for j in modelo.j)

modelo.objective = Objective(rule=objective_rule, sense=maximize, doc='FunciÃ³n objetivo')


# Funcion para llamar al solucionador de problema (NEOS)

instance = modelo
opt = SolverFactory("cplex") #cbc
solver_manager = SolverManagerFactory('neos')
results = solver_manager.solve(instance, opt=opt)
results.write()
modelo.x.display()
modelo.objective.display()
