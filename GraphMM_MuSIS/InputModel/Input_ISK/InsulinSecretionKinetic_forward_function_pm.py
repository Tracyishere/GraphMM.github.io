'''    
	Author: Chenxi Wang(chenxi.wang@salilab.org) 
	Date: 2020.11.17
	
    refer to https://pubmed.ncbi.nlm.nih.gov/18515381/

'''
####################################################################

import numpy as np
from InputModel.Input_ISK.InsulinSecretionKinetic_parameter_pm import *

def _f_mem_V(t):

    Vrest=-73; Vburst=-23
    tstep=0.0; ton=6.0-1e-10; toff=6.0

    ton=48/60; toff=10/60
    tcycle = ton + toff
    V = Vrest + (Vburst - Vrest)*(heav(np.mod(t, tcycle)-1e-10) - heav(np.mod(t, tcycle) - toff))     

    return V

# Heaviside function
def heav(x):
    return .5*(1+np.sign(x))

def minf(V):
    return 1./(1 + np.exp((Vm-V)/Sm))

def _f_Ca_md(V_t, Cmd, Ci, ts):
    IL=gL*minf(V_t)*(V_t - Vca)
    JL = alpha*IL/vmd
    Cmd_t = Cmd + ts*time_scale*(-fmd*JL - fmd*B*(Cmd - Ci))
    return Cmd_t
        
def _f_Ca_ic(V_t, Cmd, Ci, ts):
    Jserca = Jsercamax*Ci**2/(Kserca**2 + Ci**2)
    Jpmca = Jpmcamax*Ci/(Kpmca + Ci)
    Jncx = Jncx0*(Ci - 0.25)
    L = Jserca + Jpmca + Jncx + Jleak
    IR = 0.25*gL*minf(V_t)*(V_t - Vca)
    JR = alpha*IR/vcell
    Ci_t  = Ci + ts*time_scale*(-fi*JR + fv*fi*B*(Cmd - Ci) - fi*L)
    return Ci_t

def _f_r2(Ci_t):
    # r2_t = r2_0*Ci_t/(Ci_t+kp)
    r2_t = r20*Ci_t/(Ci_t + Kp2)
    return r2_t

def _f_r3(Ci_t):
    r3_t = GlucFact*r30*Ci_t/(Ci_t+Kp)
    return r3_t

def _f_N1(Cmd, N1, N2, N5, ts):
    return N1 + ts*time_scale*(-3*k1*Cmd*N1 - rm1*N1 + km1*N2 + r1*N5)

def _f_N2(Cmd, N1, N2, N3, ts):
    return N2 + ts*time_scale*(3*k1*Cmd*N1 -(2*k1*Cmd + km1)*N2 + 2*km1*N3)

def _f_N3(Cmd, N2, N3, N4, ts):
    return N3 + ts*time_scale*(2*k1*Cmd*N2 -(2*km1 + k1*Cmd)*N3 + 3*km1*N4)

def _f_N4(Cmd, N3, N4, ts):
    return N4 + ts*time_scale*(k1*Cmd*N3 - (3*km1 + u1)*N4)

def _f_N5(N1, N5, N6, Ci, ts):
    return N5 + ts*time_scale*(rm1*N1 - (r1 + rm2)*N5 + _f_r2(Ci)*N6)

def _f_N6(N5, N6, Ci, ts):    
    return N6 + ts*time_scale*(_f_r3(Ci) + rm2*N5 - (rm3 + _f_r2(Ci))*N6)

def _f_NF(N4, NF, ts):
    return NF + ts*time_scale*(u1*N4 - u2*NF)

def _f_NR(NF, NR, ts):
    return NR + ts*time_scale*(u2*NF - u3*NR)

def _f_SE(SE, NR, ts):
    return SE + ts*time_scale*(u3*NR)