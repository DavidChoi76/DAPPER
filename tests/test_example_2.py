"""Just stupidly compare the full results table."""

import numpy as np
import pytest

import dapper as dpr

statkeys = ["err.rms.a", "err.rms.f", "err.rms.u"]

##############################
# L63
##############################
from dapper.mods.Lorenz63.sakov2012 import HMM

HMM.t.BurnIn = 0
HMM.t.KObs = 10

dpr.set_seed(3000)

# xps
xps = dpr.xpList()
xps += dpr.Climatology()
xps += dpr.OptInterp()
xps += dpr.Var3D(xB=0.1)
xps += dpr.ExtKF(infl=90)
xps += dpr.EnKF("Sqrt", N=3, infl=1.30)
xps += dpr.EnKF("Sqrt", N=10, infl=1.02, rot=True)
xps += dpr.EnKF("PertObs", N=500, infl=0.95, rot=False)
xps += dpr.EnKF_N(N=10, rot=True)
xps += dpr.iEnKS("Sqrt", N=10, infl=1.02, rot=True)
xps += dpr.PartFilt(N=100, reg=2.4, NER=0.3)
xps += dpr.PartFilt(N=800, reg=0.9, NER=0.2)
xps += dpr.PartFilt(N=4000, reg=0.7, NER=0.05)
xps += dpr.PFxN(xN=1000, N=30, Qs=2, NER=0.2)

# Run
xps.launch(HMM, store_u=True)

table = xps.tabulate_avrgs(statkeys, decimals=4)
old = """
    da_method     infl  upd_a       N  rot      xN  reg   NER  |  err.rms.a  1σ      err.rms.f  1σ      err.rms.u  1σ
--  -----------  -----  -------  ----  -----  ----  ---  ----  -  -----------------  -----------------  -----------------
 0  Climatology                                                |     7.7676 ±1.2464     7.7676 ±1.2464     7.2044 ±2.4251
 1  OptInterp                                                  |     1.1648 ±0.1744     7.1198 ±1.1388     1.8578 ±0.4848
 2  Var3D                                                      |     1.0719 ±0.1192     1.7856 ±0.3686     1.2522 ±0.1616
 3  ExtKF        90                                            |     1.1932 ±0.4338     3.0113 ±1.1553     2.0016 ±0.8629
 4  EnKF          1.3   Sqrt        3  False                   |     0.5003 ±0.1105     1.1807 ±0.2613     0.8284 ±0.2526
 5  EnKF          1.02  Sqrt       10  True                    |     0.5773 ±0.0715     1.6134 ±0.4584     0.8839 ±0.1746
 6  EnKF          0.95  PertObs   500  False                   |     0.7422 ±0.308      2.0616 ±1.0183     1.3171 ±0.4809
 7  EnKF_N        1                10  True      1             |     1.605  ±0.5066     3.6838 ±0.7965     2.3756 ±0.4367
 8  iEnKS         1.02  Sqrt       10  True                    |     0.3927 ±0.2562     1.9267 ±0.7922     0.3172 ±0.1362
 9  PartFilt                      100               2.4  0.3   |     0.3574 ±0.1387     2.2799 ±1.5794     1.0327 ±0.7116
10  PartFilt                      800               0.9  0.2   |     0.5229 ±0.0832     1.337  ±0.4291     0.8152 ±0.2085
11  PartFilt                     4000               0.7  0.05  |     0.2481 ±0.0474     0.647  ±0.2298     0.3855 ±0.1051
12  PFxN                           30         1000       0.2   |     0.5848 ±0.0926     0.9573 ±0.2248     0.7203 ±0.187
"""[1:-1]


def test_len():
    assert len(old) == len(table)


table = [row.rstrip() for row in table.splitlines()]
old = [row.rstrip() for row in old.splitlines()]

L63 = dict(table=table, old=old)

##############################
# L96
##############################
from dapper.mods.Lorenz96.sakov2008 import HMM

HMM.t.BurnIn = 0
HMM.t.KObs = 10

dpr.set_seed(3000)

# xps
xps = dpr.xpList()
xps += dpr.Climatology()
xps += dpr.OptInterp()
xps += dpr.Var3D(xB=0.02)
xps += dpr.ExtKF(infl=6)
xps += dpr.EnKF("PertObs", N=40, infl=1.06)
xps += dpr.EnKF("Sqrt", N=28, infl=1.02, rot=True)

xps += dpr.EnKF_N(N=24, rot=True)
xps += dpr.EnKF_N(N=24, rot=True, xN=2)
xps += dpr.iEnKS("Sqrt", N=40, infl=1.01, rot=True)

xps += dpr.LETKF(N=7, rot=True, infl=1.04, loc_rad=4)
xps += dpr.SL_EAKF(N=7, rot=True, infl=1.07, loc_rad=6)

xps.launch(HMM, store_u=True)

table = xps.tabulate_avrgs(statkeys, decimals=4)
old = """
    da_method    infl  upd_a     N  rot    xN  loc_rad  |  err.rms.a  1σ      err.rms.f  1σ      err.rms.u  1σ
--  -----------  ----  -------  --  -----  --  -------  -  -----------------  -----------------  -----------------
 0  Climatology                                         |     0.8334 ±0.2326     0.8334 ±0.2326     0.8334 ±0.2326
 1  OptInterp                                           |     0.1328 ±0.0271     0.8345 ±0.233      0.1328 ±0.0271
 2  Var3D                                               |     0.1009 ±0.008      0.0874 ±0.0085     0.1009 ±0.008
 3  ExtKF        6                                      |     0.0269 ±0.001      0.0269 ±0.0012     0.0269 ±0.001
 4  EnKF         1.06  PertObs  40  False               |     0.0318 ±0.0018     0.0317 ±0.0016     0.0318 ±0.0018
 5  EnKF         1.02  Sqrt     28  True                |     0.0375 ±0.0018     0.0375 ±0.0019     0.0375 ±0.0018
 6  EnKF_N       1              24  True    1           |     0.0311 ±0.0009     0.031  ±0.001      0.0311 ±0.0009
 7  EnKF_N       1              24  True    2           |     0.0304 ±0.0012     0.0304 ±0.0013     0.0304 ±0.0012
 8  iEnKS        1.01  Sqrt     40  True                |     0.0254 ±0.0009     0.0255 ±0.0009     0.0254 ±0.0008
 9  LETKF        1.04            7  True    1        4  |     0.0319 ±0.0013     0.0317 ±0.0013     0.0319 ±0.0013
10  SL_EAKF      1.07            7  True             6  |     0.026  ±0.0017     0.0256 ±0.0014     0.026  ±0.0017
"""[1:-1]

table = [row.rstrip() for row in table.splitlines()]
old = [row.rstrip() for row in old.splitlines()]

L96 = dict(table=table, old=old)


##############################
# Test definitions
##############################
@pytest.mark.parametrize(("lineno"), np.arange(len(L63["table"])))
def test_tables_L63(lineno):
    assert L63["table"][lineno] == L63["old"][lineno]


@pytest.mark.parametrize(("lineno"), np.arange(len(L96["table"])))
def test_tables_L96(lineno):
    assert L96["table"][lineno] == L96["old"][lineno]
