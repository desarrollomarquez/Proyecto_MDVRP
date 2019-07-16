
import pandas as pd

data_matrix = pd.read_csv("data_distance.csv", sep=';', encoding='latin-1')


print(data_matrix[0:10].values)
