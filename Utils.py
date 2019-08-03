import pandas as pd
import numpy as np
import seaborn as sb
from copy import deepcopy
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from scipy.spatial import distance_matrix
from sklearn.preprocessing import MinMaxScaler


col_clientes = ['Cliente','x coordinate','y coordinate', 'Demanda']
col_depositos = ['Deposito','x coordinate','y coordinate','Capacity']
col_vehiculos = ['Registration Category','Registration Term','Purpose of Use','Body Shape','Year of Manufacture','Make','Model','Colour','Fuel Type','Number of Cylinders','Number of Seats','ATM Weight','GCM Weight','GTM Weight','GVM Weight','TARE Weight','VIN Prefix']

data_cl  = pd.read_csv("/home/diego/Documentos/Proyecto_MDVRP/Data_Source/Customers_50.csv", sep=',', names=col_clientes, encoding='latin-1')
data_de  = pd.read_csv("/home/diego/Documentos/Proyecto_MDVRP/Data_Source/Deposits.csv", sep=',', names=col_depositos, encoding='latin-1')
data_ve  = pd.read_csv("/home/diego/Documentos/Proyecto_MDVRP/Data_Source/Vehicles.csv", sep=',', names=col_vehiculos,  encoding='latin-1')

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



d = []
[d.append(p) for p in range(1, len(data_depositos)+1)]
c = []
[c.append(p) for p in range(1, len(data_clientes)+1)]
v = []
[v.append(p) for p in range(1, len(data_vehiculos)+1)]

# Capacidad del depósito (Wi)
W = []
[W.append(p) for p in capacity_d]
# Demanda del cliente (Dj)
D = []
[D.append(p) for p in demanda]
# Capacidad del Vehiculo (Qk)
Q = []
[Q.append(p) for p in capacity_v]

L = len(d)
C = len(c) 
N = len(v)

print("------ tamaño vectores ----------")
print(L,"-> Depositos")
print(C,"-> Clientes")
print(N,"-> Vehiculos")
print("\n")

