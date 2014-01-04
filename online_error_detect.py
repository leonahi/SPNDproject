import numpy
from scipy import stats
import matplotlib.pyplot as plt
import socket
import re

def online_error_detect(clusterIdtoSPND, models, residuals):
  """ """    
  alpha = 0.05  #----------Significance level
  
  clusterIdtoSPND_Num = clusterIdtoSPND_Number(clusterIdtoSPND)
  #print(clusterIdtoSPND_Num)

  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  #host = s.gethostname()
  s.bind(("", 25252))
  s.listen(10)
  print("Starting server...")
  
  while True:
    clisock, (remhost, remport) = s.accept()
    print("Got conection from {0}".format(remhost))
    data = clisock.recv(300)
    data = data.decode('utf-8')
    data = [float(val) for val in data.split(",")]
    print("Sensor data: {}".format(data))
    clisock.close()
    
    for clusterNo in clusterIdtoSPND.keys():     #----------For each cluster do the following 
      A = numpy.transpose(models[clusterNo])     #----------Model of cluster No.=clusterNo
      res = numpy.matrix(residuals[clusterNo])   #----------Residual of cluster No.=clusterNo
      false_alarm_counter=0
    
      res_covMat = numpy.matrix(numpy.cov(res, rowvar=0))    #----------Calculate covariance matrix of residuals
      res_inv = numpy.matrix(numpy.linalg.inv(res_covMat))   #----------Inverse of covariance matrix
      
      #print(res_covMat)
      #gammacheck = numpy.zeros(res.shape[0])
      #threshold  = numpy.zeros(res.shape[0])
      
      identmat = numpy.matrix(numpy.eye(res.shape[1]+1))
      #print(type(A))
      #print(type(identmat))
      #print(type(res_inv))    
      #print(A.shape)
      #print(res.shape[1])
      #print(res_inv.shape)
      
      data_c = numpy.matrix([data[index-1] for index in clusterIdtoSPND_Num[clusterNo]])
      #print(A.shape)
      #print(data_c.shape)
      curnt_res = calc_resid(A, numpy.transpose(data_c))
      
      gammacheck = numpy.dot(numpy.dot(curnt_res, res_inv), numpy.transpose(curnt_res))  #------Test statistic
      threshold = 1 - stats.chi2.cdf(gammacheck, 5)
      print(threshold)
      if(threshold < alpha):
        false_alarm_counter += 1   
        for col in range(len(clusterIdtoSPND[clusterNo])):
          fk = A*identmat[:,col]
          dk = numpy.transpose(numpy.transpose(fk)*res_inv*numpy.transpose(curnt_res))
          pk = numpy.matrix(numpy.linalg.inv(numpy.transpose(fk)*res_inv*(fk)))
          jk = numpy.transpose(fk)*res_inv*numpy.transpose(curnt_res)
          Lk = dk*pk*jk
          bk = pk*jk
          #print(Lk)
          #print(A.shape)
          #print(identmat[:,col].shape)
          #print(dk.shape)
          #print("Stop")
    #print(false_alarm_counter)           
    
    

def calc_resid(A, data_c):    # Calculate Residual
  return numpy.transpose(numpy.dot(A, data_c))


def clusterIdtoSPND_Number(clusterIdtoSPND):
  pattern = re.compile(r'(\d{1}|\d{2}|\d{3})$')
  clusterIdtoSPND_Num = { key:[int(pattern.search(sensorName).groups()[0]) for sensorName in val] for key, val in clusterIdtoSPND.items()}
  return clusterIdtoSPND_Num

def plot_gammacheck(gammacheck):
  plt.title("Gamma Check")
  plt.plot(gammacheck, color='r', marker='o', linestyle='')
  #plt.ylim([0,50])
  plt.show()
  
  
if __name__ == "__main__":
  pass
  #error_detect("SPND_Database/Cobalt/10SPND1-42.db")
