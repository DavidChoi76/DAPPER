###############
# Description #
###############

"""Settings as in `bib.grudzien2020numerical`.

A similar HMM is used with additive noise as a nonlinear map in various other
papers, whereas in this setting the model can be considered a random diffeomorphism,
giving a perfect-random model configuration. This uses two different solvers for the
truth and model twins respectively.

"""

#######################
# imports and exports #
#######################

import numpy as np

import dapper.mods as modelling
from dapper.mods.integration import rk4
from dapper.mods.L96s import l96s_tay2_step
from dapper.mods.Lorenz96 import Tplot, dstep_dx, dxdt, x0

####################
# Main definitions #
####################


# -------------------------------#
# define benchmark configuration #
# -------------------------------#

# Grudzien 2020 uses the below chronology with KObs=25000, BurnIn=5000
ttruth = modelling.Chronology(dt=0.005, dtObs=0.1, T=30, Tplot=Tplot, BurnIn=10)
tmodel = modelling.Chronology(dt=0.01, dtObs=0.1, T=30, Tplot=Tplot, BurnIn=10)

# set the system diffusion coefficient
diff = 0.10

# set the model state vector dimension
Nx = 10

# define the initial condition
x0 = x0(Nx)


# define different numerical step models for the ensemble, to vary the precision
def em_ensemble_step(x0, t, dt):
    # Euler-Maruyama (order 1.0 Weak / Strong)
    return rk4(lambda t, x: dxdt(x), x0, np.nan, dt, s=diff, stages=1)


def rk_ensemble_step(x0, t, dt):
    # 4-stage Runge-Kutta (order 1.0 Weak / Strong)
    return rk4(lambda t, x: dxdt(x), x0, np.nan, dt, s=diff, stages=4)


# define the numerical step model for the truth twin
def truth_step(x0, t, dt):
    # Taylor-Stratonovich (order 2.0 Weak / Strong)
    return l96s_tay2_step(x0, np.nan, dt, diff)


# we define the model configurations for the two ensemble runs and the truth twin
EMDyn = {
    'M': Nx,
    'model': em_ensemble_step,
    'linear': dstep_dx,
    'noise': 0,
}

RKDyn = {
    'M': Nx,
    'model': rk_ensemble_step,
    'linear': dstep_dx,
    'noise': 0,
}

TruthDyn = {
    'M': Nx,
    'model': truth_step,
    'linear': dstep_dx,
    'noise': 0,
}


# ensemble initial condition is shared between the EM and RK ensembles
X0 = modelling.GaussRV(mu=x0, C=0.001)

jj = np.arange(Nx)  # obs_inds
Obs = modelling.partial_Id_Obs(Nx, jj)
Obs['noise'] = 1

# define the two ensemble steppers
HMM_em_ensemble = modelling.HiddenMarkovModel(EMDyn, Obs, tmodel, X0)
HMM_rk_ensemble = modelling.HiddenMarkovModel(RKDyn, Obs, tmodel, X0)

# define the truth twin stepper
HMM_truth = modelling.HiddenMarkovModel(TruthDyn, Obs, ttruth, X0)


####################
# Suggested tuning #
####################
