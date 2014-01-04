import sqlite3 as lite
import numpy
import Pycluster as cluster
from scipy import stats

import matplotlib.pyplot as plt 

def build_model(dbName, clusterIdtoSPND, dataPoints=None):
  """ """  
  models = {}
  
  con = lite.connect(dbName)
  
  with con:
    cur = con.cursor()

    for clusterNo in clusterIdtoSPND.keys():
      column = ", ".join(clusterIdtoSPND[clusterNo])
      cur.execute("SELECT {0} FROM sensor".format(column))
      data = cur.fetchall()
      if(dataPoints==None):
        data_c = meanc(numpy.matrix(data))  #-----------Select all data points
      else:
        data_c = meanc(numpy.matrix(data[0:dataPoints-1])) #-----------Select first dataPoints data points
      

      print("cluster No. {} : {}".format(clusterNo, column))
      
#---------------------------------------Calculate SVD--------------------------------------------------      
      #U, S, V = numpy.linalg.svd(numpy.transpose(data_c))
      #columnmean, coordinates, components, eigenvalues = cluster.pca(numpy.transpose(data_c))
      covMatrix = numpy.cov(data_c,rowvar=0)
      S, U = numpy.linalg.eigh(covMatrix)      
      #print(eigenvalues)
      #print(components)
      #print(numpy.around(components,3))
      #print(numpy.around(U, 4))
      print(S)
      print(type(S))
      #print(U)
      #print(model_order_eigh(S))
      #plot_eigen(S, clusterNo, column)
      #print(model_order(eigenvalues))
      #plot_eigen(eigenvalues, clusterNo, column)
#------------------------------------------------------------------------------------------------------
      
      #models[clusterNo] = U[:, model_order_svd(S):]           # for numpy.linalg.svd
      models[clusterNo] = U[:, :model_order_eigh(S)]       # for numpy.linalg.eigh

  return models;   
       



def meanc(data):
  return (data - numpy.mean(data, axis=0))      # Converting data to zero mean


def model_order_eigh(S):                        # Calculate model order for numpy.linalg.eigh()
  m=0
  avg_eigen = numpy.mean(S)
  for i in range(S.shape[0]):
    if S[i] > avg_eigen:
      m = i
      break
  return m;    


def model_order_svd(S):                         # Calculate model order for numpy.linalg.svd()
  m=0
  avg_eigen = numpy.mean(S)
  for eigen_val in S:
    if eigen_val > avg_eigen:
      m += 1
  return m


def plot_eigen(S, clusterNo, column):      # Plot Eigen Values
  plt.title("Cluster: {} , Column: {}".format(clusterNo, column))
  plt.plot(S, marker='o', linestyle='--', color='r', label='Square')
  plt.ylabel("Eigen Value")
  plt.show()


if __name__ == "__main__":
  pass
  #build_model("SPND_Database/Cobalt/10SPND1-42.db")  
  clusterIdtoSPND = {0: ['Co4', 'Co11', 'Co18', 'Co25', 'Co32', 'Co39'], \
                     1: ['Co3', 'Co10', 'Co17', 'Co24', 'Co31', 'Co38'], \
		     2: ['Co6', 'Co13', 'Co20', 'Co27', 'Co34', 'Co41'], \
		     3: ['Co5', 'Co12', 'Co19', 'Co26', 'Co33', 'Co40'], \
		     4: ['Co7', 'Co14', 'Co21', 'Co28', 'Co35', 'Co42'], \
		     5: ['Co2', 'Co9', 'Co16', 'Co23', 'Co30', 'Co37'],  \
		     6: ['Co1', 'Co8', 'Co15', 'Co22', 'Co29', 'Co36']}
  build_model("SPND_Database/Cobalt/10SPND1-42.db", clusterIdtoSPND)
