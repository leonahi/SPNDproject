import numpy
from scipy import stats
import matplotlib.pyplot as plt

def error_detect(clusterIdtoSPND, models, residuals):
  """ """    
  alpha = 0.05  #----------Significance level
   
  for clusterNo in clusterIdtoSPND.keys():     #----------For each cluster do the following 
    A = numpy.transpose(models[clusterNo])     #----------Model of cluster No.=clusterNo
    res = numpy.matrix(residuals[clusterNo])   #----------Residual of cluster No.=clusterNo
    #false_alarm_counter=0
    
    res_covMat = numpy.matrix(numpy.cov(res, rowvar=0))    #----------Calculate covariance matrix of residuals
    res_inv = numpy.matrix(numpy.linalg.inv(res_covMat))   #----------Inverse of covariance matrix
    
    gammacheck = numpy.zeros(res.shape[0])
    threshold  = numpy.zeros(res.shape[0])
    
    identmat = numpy.matrix(numpy.eye(res.shape[1]+1))
    #print(type(A))
    #print(type(identmat))
    #print(type(res_inv))    
    #print(A.shape)
    #print(res.shape[1])
    #print(res_inv.shape)
    gross_error(res.shape[0], A, res, res_inv, gammacheck, threshold, identmat, alpha, clusterIdtoSPND, clusterNo)
    
    


def gross_error(clusterWidth, A, res, res_inv, gammacheck, threshold, identmat, alpha, clusterIdtoSPND, clusterNo):
  false_alarm_counter = 0
  for row in range(clusterWidth):
    gammacheck[row] = numpy.dot(numpy.dot(res[row,:], res_inv), numpy.transpose(res[row,:]))  #---------Test statistic
    threshold[row] = 1 - stats.chi2.cdf(gammacheck[row], 5)
    if(threshold[row] < alpha):
      false_alarm_counter += 1   
      for col in range(len(clusterIdtoSPND[clusterNo])):
        fk = A*identmat[:,col]
        dk = numpy.transpose(numpy.transpose(fk)*res_inv*numpy.transpose(res[row, :]))
        pk = numpy.matrix(numpy.linalg.inv(numpy.transpose(fk)*res_inv*(fk)))
        jk = numpy.transpose(fk)*res_inv*numpy.transpose(res[row, :])
        Lk = dk*pk*jk
        bk = pk*jk
          #print(Lk)
          #print(A.shape)
          #print(identmat[:,col].shape)
          #print(dk.shape)
          #print(bk)
        #print("Stop")
    #plot_gammacheck(threshold)
  print(false_alarm_counter)
  

def Lk():
  pass

    
def plot_gammacheck(gammacheck):
  plt.title("Gamma Check")
  plt.plot(gammacheck, color='r', marker='o', linestyle='')
  #plt.ylim([0,50])
  plt.show()
  
  
if __name__ == "__main__":
  pass
  #error_detect("SPND_Database/Cobalt/10SPND1-42.db")