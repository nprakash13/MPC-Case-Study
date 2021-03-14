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


def template_simulator1(model1):
    """
    --------------------------------------------------------------------------
    template_simulator: tuning parameters
    --------------------------------------------------------------------------
    """
    simulator = do_mpc.simulator.Simulator(model1)

    params_simulator = {
        'integration_tool': 'cvodes',
        'abstol': 1e-10,
        'reltol': 1e-10,
        't_step': 1
    }

    simulator.set_param(**params_simulator)

    p_num = simulator.get_p_template()
    p_num['F_in'] = 10
    
    def p_fun(t_now):
        return p_num

    simulator.set_p_fun(p_fun)

    simulator.setup()

    return simulator