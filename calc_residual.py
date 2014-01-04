import sqlite3 as lite
import numpy
import matplotlib.pyplot as plt 

def calc_residual(dbName, clusterIdtoSPND, models, dataPoints=None):
  residuals = {}
  
  con = lite.connect(dbName)
  
  with con:
    cur = con.cursor()

    for clusterNo in clusterIdtoSPND.keys():
      column = ", ".join(clusterIdtoSPND[clusterNo])
      cur.execute("SELECT {0} FROM sensor".format(column))
      data = cur.fetchall()
      if(dataPoints==None):
        data_c = meanc(numpy.matrix(data)) #-----------Select all data points
      else:
        data_c = meanc(numpy.matrix(data[0:dataPoints-1])) #-----------Select first 7000 data points

      #print("cluster No. {} : {}".format(clusterNo, column))
      
#--------------------------------------Calculate Residual----------------------------------------------
      res = calc_resid(models[clusterNo], data_c)      
      plot_residual(res, clusterNo, column)
      #print(res.shape)
      #res_covMat = numpy.cov(res, rowvar=0)
      #res_inv = numpy.linalg.inv(res_covMat)
      #print(numpy.round(res_inv,4))
#------------------------------------------------------------------------------------------------------      
      residuals[clusterNo] = res
      
      
  return residuals;   
        


  
def calc_resid(A, data_c):    # Calculate Residual
  return numpy.dot(data_c, A)

def meanc(data):
  return (data - numpy.mean(data, axis=0))      # Converting data to zero mean

def plot_residual(res, clusterNo, column):     # Plot Residual
  color = ('#FFFF00', '#FF0000', '#FF00FF', '#0000FF', '#0B0B3B', '#FAAC58', '#0B3B39', '#2E64FE')
  for col in range(0, res.shape[1]):
    plt.plot(res[:,col], color=color[col])
  #plt.ylim([-5,5])
  plt.title("Cluster_{} : {}".format(clusterNo, column))
  #plt.legend(loc='best')
  plt.show()



if __name__ == "__main__":
  pass
  #build_model("SPND_Database/Cobalt/10SPND1-42.db")  
