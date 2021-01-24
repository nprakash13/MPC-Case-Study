### Write/read from /to Matrikon OPC server to python


import OpenOPC 
import time

import pywintypes

pywintypes.datetime = pywintypes.TimeType

#opc = OpenOPC.open_client('localhost')

#Instantiating OPC client for Python
opc = OpenOPC.client()
opc.servers()
#opc.connect('Matrikon.OPC.Simulation.1')
# List the servers on the target machine
#list1 = opc.servers('192.168.0.1')

#Connect to the target OPC server on target machine
opc.connect('Matrikon.OPC.Simulation.1', 'localhost')


#Read from OPC server
value = opc.read('MPC.Level')
print(value)

#Write to OPC server
opc.write( ('MPC.F_out', 5.0) )

#def read_level()
    #opc = OpenOPC.client()
    #opc.servers()
    #opc.connect('Matrikon.OPC.Simulation.1', 'localhost')
    #value = opc.read('.Level')
    #return value
