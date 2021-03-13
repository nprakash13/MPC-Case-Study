import OpenOPC 
import time

import pywintypes

pywintypes.datetime = pywintypes.TimeType

#opc = OpenOPC.open_client('localhost')

#Instantiating OPC client for Python
opc = OpenOPC.client()

# List the servers on the target machine
list1 = opc.servers('192.168.0.1')

#Connect to the target OPC server on target machine
opc.connect('Matrikon.OPC.Simulation.1', '192.168.0.1')

#List out the OPC sections
#print(list1)
#list2 = opc.list()
#list3 = opc.list('Configured Aliases')
#print(list2)

#Read from OPC server
print(opc.read('Random.Int4'))

#Write to OPC server
opc.write( ('Bucket Brigade.Real8', 100.0) )