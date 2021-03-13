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
from casadi import *
from casadi.tools import *
import pdb
import sys
sys.path.append('../../')
import do_mpc


def template_model1():
    """
    --------------------------------------------------------------------------
    template_model1: Variables / RHS / AUX
    --------------------------------------------------------------------------
    """
    model_type = 'continuous' # either 'discrete' or 'continuous'
    model1 = do_mpc.model.Model(model_type)

    # Certain parameters
    # mu_m  = 0.02
    # K_m	  = 0.05
    # K_i	  = 5.0
    # v_par = 0.004
    # Y_p	  = 1.2

    T = 1 

    # States struct (optimization variables):
    # X_s = model.set_variable('_x',  'X_s')  # bio mass
    # S_s = model.set_variable('_x',  'S_s')  # Substrate
    # P_s = model.set_variable('_x',  'P_s')  # Product
    # V_s = model.set_variable('_x',  'V_s')  # Reactor volume

    L = model1.set_variable('_x', 'L') # Level of tank

    

    # Input struct (optimization variables):
    # inp = model.set_variable('_u',  'inp')
    F_out = model1.set_variable('_u', 'F_out') # Output flow (FC25)

    # Fixed parameters:
    # Y_x = model.set_variable('_p',  'Y_x')
    # S_in = model.set_variable('_p', 'S_in')
 
    F_in = model1.set_variable('_p', 'F_in') # Inlet flow (FC10)   



    # mu_S	= mu_m*S_s/(K_m+S_s+(S_s**2/K_i))

    # Differential equations
    # model.set_rhs('X_s', mu_S*X_s - inp/V_s*X_s)
    # model.set_rhs('S_s', -mu_S*X_s/Y_x - v_par*X_s/Y_p + inp/V_s*(S_in-S_s))
    # model.set_rhs('P_s', v_par*X_s - inp/V_s*P_s)
    # model.set_rhs('V_s', inp)

    model1.set_rhs('L', 10*1/T*(F_in-F_out))

    # Build the model
    model1.setup()

    return model1