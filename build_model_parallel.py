import sqlite3 as lite
import numpy
import Pycluster as cluster
from scipy import stats

import matplotlib.pyplot as plt 
import multiprocessing

class build_model_process(multiprocessing.Process):
  def __init__(self, spnd_names, dbName, dataPoints):
    multiprocessing.Process.__init__(self)
    self.spnd_names = spnd_names.get()  
    self.dbName     = dbName
    self.dataPoints = dataPoints
    
  def run(self):
    con = lite.connect(self.dbName)
    with con:
      cur = con.cursor()
      column = ", ".join(self.spnd_names)
      cur.execute("SELECT {0} FROM sensor".format(column))
      data = cur.fetchall()
      if(self.dataPoints==None):
        data_c = self.meanc(numpy.matrix(data))  #-----------Select all data points
      else:
        data_c = self.meanc(numpy.matrix(data[0:self.dataPoints-1]))  #-----------Select first dataPoints data points
      #print(self.spnd_names)
      #print(self.pid)

      #---------------------Calculate SVD-----------------------
      covMatrix = numpy.cov(data_c,rowvar=0)
      S, U = numpy.linalg.eigh(covMatrix)
 
  
  def meanc(self, data):
    return (data - numpy.mean(data, axis=0))      # Converting data to zero mean   
 
  def model_order(self, S):
    m=0
    avg_eigen = numpy.mean(S)
    for eigen_val in S:
      if eigen_val > avg_eigen:
        m += 1
    return m




def build_model(dbName, clusterIdtoSPND, dataPoints=None):
  """ """  
  models = {}

  data_q = multiprocessing.Queue()
  model_q = multiprocessing.Queue() 
  
  for clusterNo in clusterIdtoSPND.keys():
    data_q.put(clusterIdtoSPND[clusterNo])
      
      
#---------------------------------------Calculate SVD--------------------------------------------------      
      #U, S, V = numpy.linalg.svd(numpy.transpose(data_c))
      #columnmean, coordinates, components, eigenvalues = cluster.pca(numpy.transpose(data_c))
      #S, U = numpy.linalg.eigh(covMatrix)      
      #print(eigenvalues)
      #print(numpy.around(components,3))
      #print(numpy.around(U, 4))
      #print(U) 
      #print(S)
      #plot_eigen(S, clusterNo, column)
#------------------------------------------------------------------------------------------------------
      
      #models[clusterNo] = U[:, model_order(S):]      
  process_list = []
  for i in range(len(clusterIdtoSPND)):
    process_list.append(build_model_process(data_q, dbName, dataPoints))
    #p.daemon = True
    process_list[i].start()
  #return models;   
  #print(process_list[0].spnd_names)
  #data_q.join()       



"""def model_order(S):
  m=0
  avg_eigen = numpy.mean(S)
  for eigen_val in S:
    if eigen_val > avg_eigen:
      m += 1
  return m"""

def plot_eigen(S, clusterNo, column):      # Plot Eigen Values
  plt.title("Cluster: {} , Column: {}".format(clusterNo, column))
  plt.plot(S, marker='o', linestyle='--', color='r', label='Square')
  plt.ylabel("Eigen Value")
  plt.show()

if __name__ == "__main__":
  pass
  clusterIdtoSPND = {0: ['Co4', 'Co11', 'Co18', 'Co25', 'Co32', 'Co39'], \
                     1: ['Co3', 'Co10', 'Co17', 'Co24', 'Co31', 'Co38'], \
		     2: ['Co6', 'Co13', 'Co20', 'Co27', 'Co34', 'Co41'], \
		     3: ['Co5', 'Co12', 'Co19', 'Co26', 'Co33', 'Co40'], \
		     4: ['Co7', 'Co14', 'Co21', 'Co28', 'Co35', 'Co42'], \
		     5: ['Co2', 'Co9', 'Co16', 'Co23', 'Co30', 'Co37'],  \
		     6: ['Co1', 'Co8', 'Co15', 'Co22', 'Co29', 'Co36']}
  build_model("SPND_Database/Cobalt/10SPND1-42.db", clusterIdtoSPND)  
