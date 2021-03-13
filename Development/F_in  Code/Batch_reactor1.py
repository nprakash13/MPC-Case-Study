#
#   This file is part of do-mpc
#
#   do-mpc: An environment for the easy, modular and efficient implementation of
#        robust nonlinear model predictive control
#
#   Copyright (c) 2014-2019 Sergio Lucia, Alexandru Tatulea-Codrean
#                        TU Dortmund. All rights reserved
#
#   do-mpc is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Lesser General Public License as
#   published by the Free Software Foundation, either version 3
#   of the License, or (at your option) any later version.
#
#   do-mpc is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Lesser General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with do-mpc.  If not, see <http://www.gnu.org/licenses/>.

import numpy as np
import matplotlib.pyplot as plt
from casadi import *
from casadi.tools import *
import pdb
import sys
sys.path.append('../../')
import do_mpc

#nagaraj
import matplotlib.axes as maxes
from matplotlib.animation import FuncAnimation, FFMpegWriter, ImageMagickWriter
import pdb
import os
from do_mpc.tools import IndexedProperty, Structure

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import time

from template_model1 import template_model1
from template_mpc1 import template_mpc1
from template_simulator1 import template_simulator1
#from Read_write import read_level

import OpenOPC 
from time import sleep
import pywintypes
pywintypes.datetime = pywintypes.TimeType

""" User settings: """
show_animation = True
store_results = False

"""
Get configured do-mpc modules:
"""

model1 = template_model1()
mpc = template_mpc1(model1)
simulator = template_simulator1(model1)
estimator = do_mpc.estimator.StateFeedback(model1)

"""
Set initial state
"""

#X_s_0 = 1.0 # This is the initial concentration inside the tank [mol/l]
#S_s_0 = 0.5 # This is the controlled variable [mol/l]
#P_s_0 = 0.0 #[C]
#V_s_0 = 120.0 #[C]
#x0 = np.array([X_s_0, S_s_0, P_s_0, V_s_0])

#opc = OpenOPC.client()
#opc.servers()
#opc.connect('Matrikon.OPC.Simulation.1', 'localhost')


#value = opc.read('MPC.Level')
#print(value)

#L = float(value[0])
L = 50
#print(L)

#F_in = 10
#F_out = 20
x0 = np.array([L])


mpc.x0 = x0
simulator.x0 = x0
estimator.x0 = x0

# print(SX.sym('x0'))
# print(x0.shape)
mpc.set_initial_guess()

"""
Setup graphic:
"""


# Initialize graphic:
graphics = do_mpc.graphics.Graphics(mpc.data)

# Create figure with arbitrary Matplotlib 'method'
#fig, ax = plt.subplots(1, sharex=True)
#ax.set_ylabel('F_in [l/h]')
#fig.align_ylabels()

#fig, ax, graphics = do_mpc.graphics.default_plot(mpc.data,figsize=(8,5))
#fig, ax, graphics = graphics.add_line(var_type= "_p", 'F_in', )''

# Create figure with arbitrary Matplotlib method  
fig, ax = plt.subplots(3, sharex=True)  



# Configure plot (pass the previously obtained ax objects):  
graphics.add_line(var_type='_x', var_name='L', axis=ax[0])  
graphics.add_line(var_type='_u', var_name='F_out', axis=ax[1])  
#graphics.add_line(var_type='_p', var_name='F_in', axis=ax[2])  

# Optional configuration of the plot(s) with matplotlib:  
ax[0].set_ylabel('Level')  
ax[1].set_ylabel('F_out')  
#ax[2].set_ylabel('F_in')  
fig.align_ylabels()


#fig, ax, graphics = do_mpc.graphics.default_plot(mpc.data_fields, figsize=(8,5))
#fig, ax, graphics = do_mpc.graphics.default_plot(, figsize=(8,5))
#fig, ax[1], graphics = do_mpc.graphics.default_plot(mpc.data,figsize=(8,5))


plt.ion()

#F_list = []

"""
Run MPC main loop:
"""


for k in range(50):
    #time.sleep(5)
    u0 = mpc.make_step(x0)
    y_next = simulator.make_step(u0)
    x0 = estimator.make_step(y_next)
    #F_list.append(mpc.data['_x','L'])
    if show_animation:
        graphics.plot_results(t_ind=k)
        graphics.plot_predictions(t_ind=k)
        #graphics.add_line(var_type='_p', var_name='F_in', axis=ax[1])
        graphics.reset_axes()
        plt.show()
        plt.pause(0.01)
   
#print(F_list)
input('Press any key to exit.')

# Store results:
if store_results:
    do_mpc.data.save_results([mpc, simulator], 'batch_reactor_MPC')
  


