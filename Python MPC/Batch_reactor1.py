#
#   This file is the main py script. Start the python MPC controller by running this file
#
#   The Project is developed by Nagaraj Prakash, Prathamesh Kolekar and Srinidhi Subbanna
#   as part of our Case-Study for comparision of MPC and Override Control strategies.
#
#   This project is a free software: you can redistribute it and/or modify
#   it under the terms of the GNU Lesser General Public License as
#   published by the Free Software Foundation, either version 3
#   of the License, or (at your option) any later version.
#
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
Get initial state
"""
opc = OpenOPC.client()
opc.servers()
opc.connect('Matrikon.OPC.Simulation.1', 'PRATHAM')

value = opc.read('MPC.Level')

"""
Set initial state
"""
L = float(value[0])
x0 = np.array([L])

mpc.x0 = x0
simulator.x0 = x0
estimator.x0 = x0

mpc.set_initial_guess()

"""
Setup graphic:
"""
# Initialize graphic:
graphics = do_mpc.graphics.Graphics(mpc.data)

fig, ax, graphics = do_mpc.graphics.default_plot(mpc.data,figsize=(8,5))

plt.ion()

"""
Run MPC main loop:
"""

try : 
    P = 0

    while (opc.read('MPC.Level')[1]) == 'Good':
        time.sleep(5)
        u0 = mpc.make_step(x0)
        opc.write( ('MPC.F_out', float(u0[0][0])))
        y_next = simulator.make_step(u0)
        y_next1 = np.array([[float(opc.read('MPC.Level')[0])]])  #reading value from OPC server
        x0 = estimator.make_step(y_next1)
        if show_animation:
            graphics.plot_results(t_ind=P)
            graphics.plot_predictions(t_ind=P)
            graphics.reset_axes()
            plt.show()
            plt.pause(0.01)
        P = P+1
except KeyboardInterrupt:
    print('Program was stopped by interrupt')
    opc.close()

# Store results:
if store_results:
    do_mpc.data.save_results([mpc, simulator], 'batch_reactor_MPC')