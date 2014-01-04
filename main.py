import numpy
from build_cluster import get_clusterid
from build_model import build_model
from calc_residual import calc_residual
from error_detect import error_detect

import re
import cProfile

def main(dbName):
  clusterIdtoSPND = get_clusterid(dbName)
  models          = build_model(dbName, clusterIdtoSPND, dataPoints=7000)
  residuals       = calc_residual(dbName, clusterIdtoSPND, models, dataPoints=None)  
  error_detect(clusterIdtoSPND, models, residuals)
  
  
  
  #print(models)
  #print(resuduals)
  



  
def profile_get_clusterid():
  cProfile.run('get_clusterid("SPND_Database/Cobalt/10SPND1-42.db")')

def profile_build_model():
  cProfile.run('build_model("SPND_Database/Vanadium/10F29-130.db", get_clusterid("SPND_Database/Vanadium/10F29-130.db"), dataPoints=7000)')  

def profile_calc_residual():
  cProfile.run('calc_residual("SPND_Database/Cobalt/10SPND1-42.db", get_clusterid("SPND_Database/Cobalt/10SPND1-42.db"), build_model("SPND_Database/Cobalt/10SPND1-42.db", get_clusterid("SPND_Database/Cobalt/10SPND1-42.db"), dataPoints=7000), dataPoints=None)')

def profile_error_detect():
  cProfile.run('error_detect(get_clusterid("SPND_Database/Cobalt/10SPND1-42.db"), build_model("SPND_Database/Cobalt/10SPND1-42.db", get_clusterid("SPND_Database/Cobalt/10SPND1-42.db"), dataPoints=7000), calc_residual("SPND_Database/Cobalt/10SPND1-42.db", get_clusterid("SPND_Database/Cobalt/10SPND1-42.db"), build_model("SPND_Database/Cobalt/10SPND1-42.db", get_clusterid("SPND_Database/Cobalt/10SPND1-42.db"), dataPoints=7000), dataPoints=None))')
  
if __name__ == "__main__":
  main("SPND_Database/Cobalt/10SPND1-42.db")
  #main("SPND_Database/Vanadium/10F29-130.db")
