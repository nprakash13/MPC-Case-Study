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


def template_mpc1(model1):
    """
    --------------------------------------------------------------------------
    template_mpc: tuning parameters
    --------------------------------------------------------------------------
    """
    mpc = do_mpc.controller.MPC(model1)
    
    setup_mpc = {
        'n_horizon': 20,
        'n_robust': 1,
        'open_loop': 0,
        't_step': 1,
        'state_discretization': 'collocation',
        'collocation_type': 'radau',
        'collocation_deg': 2,
        'collocation_ni': 2,
        'store_full_solution': True
        # Use MA27 linear solver in ipopt for faster calculations:
        #'nlpsol_opts': {'ipopt.linear_solver': 'MA27'}
    }

    mpc.set_param(**setup_mpc)

    #Setting Objective Function
    mterm = (((model1._x['L']) - 40)**2)
    lterm = (((model1._x['L']) - 40)**2)


    mpc.set_objective(mterm= mterm, lterm=lterm)
    mpc.set_rterm(F_out = 1) #Penalty function
   
    #setting bounds
    mpc.bounds['lower', '_x', 'L'] = 20.0
    mpc.bounds['upper', '_x', 'L'] = 80.0
    mpc.bounds['lower', '_u', 'F_out'] = 0.0
    mpc.bounds['upper', '_u', 'F_out'] = 50.0

    #Possible values for Uncertain value simulation
    mpc.set_uncertainty_values(F_in = np.array([1.0, 5.0, 10.0])) 

    mpc.setup()

    return mpc