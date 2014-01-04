import sqlite3 as lite
import Pycluster as cluster
import numpy
import re
import matplotlib.pyplot as plt

def get_clusterid(v_co_dbName, vanadium_dbName=None, cobalt_dbName=None):
  ''' Given the database of sensors observation it calculates clusterid for each sensor.
      Module Dependencies - Pycluster, numpy, sqlite3'''

#------------------------------Creating Data & Mask matrix for clustering-----------------------------  
  con_v_co = lite.connect(v_co_dbName)
  con_v_co.row_factory = lite.Row
  
  with con_v_co:
    cur_v_co = con_v_co.cursor()
    cur_v_co.execute("SELECT * FROM sensor")    
    columnNames_v_co = cur_v_co.fetchone()
    columnNames_v_co = columnNames_v_co.keys()
    
  con_v_co = lite.connect(v_co_dbName)
  with con_v_co:
    cur_v_co = con_v_co.cursor()
    cur_v_co.execute("SELECT * FROM sensor")    
    rows_v_co = cur_v_co.fetchall()

    
  ROW_v_co = [row[3:] for row in rows_v_co]
  
  Data_v_co = numpy.matrix(ROW_v_co).astype(float)  
  Data_v_co = numpy.transpose(Data_v_co)    
  
  numRows_v_co, numCols_v_co = Data_v_co.shape  
  mask_v_co = numpy.ones((numRows_v_co, numCols_v_co)).astype(numpy.uint8)     
#-------------------------------------------------------------------------------------------------------


#-------------------------------------Covariance Matrix-----------------------------------------
  #fd = open("covMatrix.txt", 'w')
  #covMatrix = numpy.corrcoef(Data_v_co)
  #ones = numpy.ones(covMatrix.shape)
  #distMatrix = ones - covMatrix
  #for item in list(covMatrix):
  #  for val in item:
  #    fd.write("{}, ".format(str(round(val,3))))
  #  fd.write('\n')
  #print(covMatrix)  
  



#--------------------------------------Generating mask for Data_V----------------------------------------
  counter = 0
  for i in range(numRows_v_co):
    for j in range(numCols_v_co):
      if Data_v_co[i,j] < 0:
        counter += 1          # Counting missing observation
        mask_v_co[i,j] = 0
#---------------------------------------------------------------------------------------------------------  



#--------------------------------------------Clustering SPND----------------------------------------------
  clusterid, error, nfound = cluster.kcluster(data=Data_v_co, nclusters=7, 
                                        mask=mask_v_co, weight=None,
                                        transpose=0, npass=100,
                                        method='a', dist='c', initialid=None)      
  
  print("Number of times solution is found: {0}".format(nfound))
  #print("ClusterId : {}".format(clusterid))
#---------------------------------------------------------------------------------------------------------- 



#--------------------------------------Create clusterid to SPND map----------------------------------------
  clusterIdtoSPND = {}
  lst = []
  for cid in clusterid:
    clusterIdtoSPND[cid] = lst
  for cid, col in zip(clusterid, columnNames_v_co[3:]):
    clusterIdtoSPND[cid] = clusterIdtoSPND[cid] + [col]
    
  #print(clusterIdtoSPND)
#----------------------------------------------------------------------------------------------------------




#--------------------------------------------Storing ClusterId---------------------------------------------  
  con_V_Co = lite.connect(v_co_dbName)
  con_V_Co.row_factory = lite.Row
  
  with con_V_Co:
    cur = con_V_Co.cursor()
    cur.execute("SELECT * FROM sensor")
    columnNames_V_Co = cur.fetchone()
    columnNames_V_Co = columnNames_V_Co.keys()
  
  sensorList = ",".join(columnNames_V_Co[3:])
  numSensor = len(columnNames_V_Co[3:])
  ques = ["?"]*numSensor
  ques = ",".join(ques)
  columnNames = " INT, ".join(columnNames_V_Co[3:])
  columnNames = columnNames + " INT"

  data = tuple([numpy.asscalar(numpy.uint32(item)) for item in clusterid])
  
  con = lite.connect("clusterId.db")  
  with con:
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS clusterid (Timestamp DATETIME CURRENT_TIMESTAMP, {})".format(columnNames))
    cur.execute("INSERT INTO clusterid (Timestamp, {0}) VALUES (DateTime('now'), {1})".format(sensorList, ques), data)
#------------------------------------------------------------------------------------------------------------------------  



#----------------------------------------------Cluster Plot-------------------------------------------
  #plot_cluster(clusterIdtoSPND)
#-----------------------------------------------------------------------------------------------------


#--------------------------------------Return clusterId to SPND maping--------------------------------  
  return clusterIdtoSPND
#-----------------------------------------------------------------------------------------------------  
  
   
   
  #print("ClusterId : {}".format(clusterid))
  #print("nfound : {}".format(nfound))
  #print("error : {}".format(error))
  
  #print("Number of missing observation : {}".format(counter + 40))
  #print("No. of rows : {}, No. of Cols : {}".format(numRows, numCols))


  #clusterid, error, nfound = cluster.kmedoids(distance=distMatrix, nclusters=7, npass=20, initialid=None)
  #print("ClusterId : {}".format(clusterid))
  #print("nfound : {}".format(nfound))
  #print("error : {}".format(error))


def plot_cluster(clusterIdtoSPND):
  pattern = re.compile(r'(\d{1}|\d{2}|\d{3})$')
  clusterIdtoSPND_Num = { key:[int(pattern.search(sensorName).groups()[0]) for sensorName in val] for key, val in clusterIdtoSPND.items()}
  cluster_x_axis = [[key]*len(val) for key, val in clusterIdtoSPND_Num.items()]
  #print(clusterIdtoSPND_Num.values())
  #print(cluster_x_axis)
  color = ('#FFFF00', '#FF0000', '#FFBF00', '#40FF00', '#0000FF', '#FF00FF', '#000000', '#848484', '#0B610B', '#FA5858', '#0B0B3B', '#886A08', '#8181F7', '#FF0040', '#FAAC58', '#0B3B39', '#2E64FE')
  for y_axis, index in zip(clusterIdtoSPND_Num.values(), range(0,17)):
    for point in y_axis:
      x_axis = [point]*len(y_axis)
      plt.plot(x_axis, y_axis, marker='o', color=color[index], ls='')
  plt.grid(b=True, which='both', color='0.65',linestyle='-')    
  plt.yticks(numpy.arange(29, 130, 3.0))
  plt.xticks(numpy.arange(29, 130, 3.0))
  plt.ylabel("V SPND No.")
  plt.xlabel("V SPND No.")
  plt.show()
      
  
  '''for x_axis, y_axis in zip(cluster_x_axis, clusterIdtoSPND_Num.values()):
    plt.plot(x_axis, y_axis, marker='o', color='r')
  plt.grid(b=True, which='both', color='0.65',linestyle='-')
  plt.yticks(numpy.arange(29, 130, 1.0))
  plt.xlim([-1,17])
  plt.ylabel("Co SPND No.")
  plt.xlabel("Cluster No.")
  plt.show()'''
  
if __name__ == "__main__":
  """vanadiumSensors = "V29"," ,V30"," ,V31"," ,V32"," ,V33"," ,V34"," ,V35"," ,V36"," ,V37"," ,V38"," ,V39"," ,V40"," ,V41"," ,V42"," ,V43"\
                    ,"V44","V45","V46","V47","V48","V49","V50","V51","V52","V53","V54","V55","V56","V57","V58","V59","V60"\
		    ,"V61","V62","V63","V64","V65","V66","V67","V68","V69","V70","V71","V72","V73","V74","V75","V76","V77"\
		    ,"V78","V79","V80","V81","V82","V83","V84","V85","V86","V87","V88","V89","V90","V91","V92","V93","V94"\
		    ,"V95","V96","V97","V98","V99","V100","V101","V102","V103","V104","V105","V106","V107","V108","V109","V110"\
		    ,"V111","V112","V113","V114","V115","V116","V117","V118","V119","V120","V121 V122 V123 V124 V125
		     V126 V127 V128 V129 V130" """
  #get_clusterid("SPND_Database/Vanadium/10F29-130.db", "SPND_Database/Cobalt/10SPND1-42.db", "SPND_Database/F29-130_SPND1-42.db" )
  get_clusterid("SPND_Database/Cobalt/10SPND1-42.db", "SPND_Database/Cobalt/10SPND1-42.db", "SPND_Database/F29-130_SPND1-42.db" )
