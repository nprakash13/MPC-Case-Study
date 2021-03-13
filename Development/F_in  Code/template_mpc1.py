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


def template_mpc1(model1):
    """
    --------------------------------------------------------------------------
    template_mpc: tuning parameters
    --------------------------------------------------------------------------
    """
    mpc = do_mpc.controller.MPC(model1)
    
    setup_mpc = {
        'n_horizon': 20,
        'n_robust': 0,
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

    # mterm = -model.x['P_s']
    # lterm = -model.x['P_s']
    #mterm = -model1.x('F_out',)
    #lterm = -model1.x('F_out',)
    #mterm = -((50-model1._x['L'])/(model1._x['L']-50))
    #lterm = ((50-model1._x['L'])/(model1._x['L']-50))
    #p_values = np.array([1])
    
    #mterm = ((model1._x['L'])*(1-((model1._x['L'])/100)))
    #lterm = ((model1._x['L'])*(1-((model1._x['L'])/100)))

    #mterm = (((model1._x['L']) - 65)**2)
    #lterm = (((model1._x['L']) - 65)**2)


    mterm = (((model1._x['L']) - 40)**2)
    lterm = (((model1._x['L']) - 40)**2)


    mpc.set_objective(mterm= mterm, lterm=lterm)
    #mpc.set_objective(mterm= None, lterm= None)
    mpc.set_rterm(F_out = 1)
   
    #mpc.bounds['lower', '_x', 'X_s'] = 0.0
    #mpc.bounds['lower', '_x', 'S_s'] = -0.01
    #mpc.bounds['lower', '_x', 'P_s'] = 0.0
    #mpc.bounds['lower', '_x', 'V_s'] = 0.0
    

    #mpc.bounds['upper', '_x','X_s'] = 3.7
    #mpc.bounds['upper', '_x','P_s'] = 3.0
    mpc.bounds['lower', '_x', 'L'] = 20.0
    mpc.bounds['upper', '_x', 'L'] = 80.0
    mpc.bounds['lower', '_u', 'F_out'] = 0.0
    mpc.bounds['upper', '_u', 'F_out'] = 50.0

    #mpc.bounds['lower', '_p', 'F_in'] = 0.0
    #mpc.bounds['upper', '_p', 'F_in'] = 40.0

    #mpc.bounds['lower','_u','inp'] = 0.0
    #mpc.bounds['upper','_u','inp'] = 0.2
    #mpc.bounds['lower','_u','L_set'] = 20.0
    #mpc.bounds['upper','_u','L_set'] = 80.0


    #Y_x_values = np.array([1.0, 5.0, 10.0])
    #S_in_values = np.array([200.0, 220.0, 180.0])
    
    mpc.set_uncertainty_values(F_in = np.array([10.0, 15.0, 20.0]))
    #mpc.set_p_fun()
    #mpc.set_p_fun
    

    mpc.setup()

    return mpc