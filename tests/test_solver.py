#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Marin Lauber"
__copyright__ = "Copyright 2019, Marin Lauber"
__license__ = "GPL"
__version__ = "1.0.1"
__email__  = "M.Lauber@soton.ac.uk"

import numpy as np
import matplotlib.pyplot as plt
from src.fluid import Fluid
from src.field import TaylorGreen, ShearLayer, McWilliams

def test_diagnostics():
    flow = Fluid(64, 64, 1.)
    flow.init_solver()
    flow.init_field(McWilliams)
    flow._get_psih()
    assert np.isclose(np.round(flow.tke(),1), 0.5, atol=1e-3),\
           "Error: TKE do not match"
    assert flow.enstrophy!=0.0, "Error: Enstrophy is zero"
    flow._compute_spectrum(200)


def test_plots():
    flow = Fluid(16, 16, 1.)
    flow.init_solver()
    flow.init_field(ShearLayer)
    plt.ion()
    flow.plot_spec()
    plt.close()
    flow.display()
    plt.close()
    flow.display_vel()
    plt.close()


def test_update():
    # build field
    flow = Fluid(32, 32, 1.)
    flow.init_solver()
    flow.init_field(TaylorGreen)
    # start update
    while(flow.time<=0.1):
        flow.update()
    # get final results
    flow.wh_to_w()
    w_n = flow.w.copy()
    # exact solution
    w_e  = TaylorGreen(flow.x, flow.y,flow.Re, time=flow.time)
    assert np.allclose(w_n, w_e, atol=1e-6), "Error: solver diverged."


if __name__=="__main__":
     test_diagnostics()
     test_plots()
     test_update()
