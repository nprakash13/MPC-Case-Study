#
#   This file part of our MPC controller for Level Control project
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
    T = 1

    # States struct (optimization variables):
    L = model1.set_variable('_x', 'L') # Level of tank
 
    
    
    # Input struct (optimization variables):
    F_out = model1.set_variable('_u', 'F_out') # Out flow from tank
    

    # Fixed parameters:
    F_in = model1.set_variable('_p', 'F_in') # Inlet flow (FC10)   

    # Differential equations
    model1.set_rhs('L', 1/T*(F_in-F_out))

    # Build the model
    model1.setup()

    return model1