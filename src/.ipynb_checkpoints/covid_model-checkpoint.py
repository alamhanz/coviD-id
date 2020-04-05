import pandas as pd
import scipy.integrate as spi
import numpy as np
import seaborn as sns
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm
import matplotlib.pyplot as plt
import datetime as dt
import pyswarms as ps

## basic sird model
def sird_model_diff(VALUE_ON_T,t,param_bk,param_rk,param_mk):  
    '''The main set of equations'''
    Y=np.zeros((4))
    dS,dI,dR,dD = VALUE_ON_T  
    Y[0] = - param_bk * dS * dI
    Y[1] = (param_bk * dS * dI) - (param_rk * dI) - (param_mk * dI)
    Y[2] = param_rk * dI
    Y[3] = param_mk * dI
    return Y

def sird_model(x,INPUT,T_range):
    param_b,param_r,param_m=x
    RES = spi.odeint(sird_model_diff,INPUT,T_range, args=(param_b,param_r,param_m))
    return RES

def cost_func_sird(x,df,N,with_pred=False):
    ## Parameter
    param_b,param_r,param_m=x
    
    ## time range
    T_start = 0.0
    T_inc=1.0
    T_end=df.shape[0]
    
    ## Initial input
    I0=2/N
    S0=1-I0
    N0=N*1000
        
    INPUT = (S0, I0, 0.0, 0.0)
    col_use=['Sus','Inf','Rec','Dea']
    col_use_pred=[x+'_pred' for x in col_use]
    T_range = np.arange(T_start, T_end+T_inc, T_inc)
    RES = spi.odeint(sird_model_diff,INPUT,T_range, args=(param_b,param_r,param_m))
    df[col_use_pred]=pd.DataFrame(RES)

#     eS=(((df['Sus']-df['Sus_pred'])*df['weight'])**2).sum()*0.15
#     eI=(((df['Inf']-df['Inf_pred'])*df['weight'])**2).sum()*0.35
#     eR=(((df['Rec']-df['Rec_pred'])*df['weight'])**2).sum()*0.3
#     eD=(((df['Dea']-df['Dea_pred'])*df['weight'])**2).sum()*0.2
    
    ## Update 2020/04/04
    eS=(((df['Sus']-df['Sus_pred'])*df['weight'])**2).sum()*0.1
    eI=(((df['Inf']-df['Inf_pred'])*df['weight'])**2).sum()*0.45
    eR=(((df['Rec']-df['Rec_pred'])*df['weight'])**2).sum()*0.3
    eD=(((df['Dea']-df['Dea_pred'])*df['weight'])**2).sum()*0.15

    if with_pred:
        return df,(eS+eI+eR+eD)*N0  
    else:
        return (eS+eI+eR+eD)*N0

def multi_cost_func_sird(x,df,N):
    all_res=[]
    for i in x:
        res=cost_func_sird(i,df,N)
        all_res.append(res)
    return np.array(all_res)
    
def pso_sird(df0,population):
    opt1 = {'c1': 0.15, 'c2': 0.95, 'w':0.25}
    pos_res=[]
    best_pos=[]
    min_func=100
    for i in range(3):
        optimizer1 = ps.single.GlobalBestPSO(n_particles=200, dimensions=3, options=opt1,
#                                              bounds=([0.1,0.005,0.005],[0.7,0.3,0.3]))
                                             bounds=([0.001,0.001,0.001],[0.5,0.4,0.4]))
        # Perform optimization
        cost, pos = optimizer1.optimize(multi_cost_func_sird, iters=20, df=df0, N=population)
        pos_res.append(pos)
        if cost<min_func:
            min_func=cost
            best_pos=pos

    max_bound2=np.array(pos_res).max(axis=0)
    max_bound2=max_bound2+(max_bound2*0.08)
    min_bound2=np.array(pos_res).min(axis=0)
    min_bound2=min_bound2-(min_bound2*0.08)
    optimizer2 = ps.single.GlobalBestPSO(n_particles=150, dimensions=3, options=opt1,
                                             bounds=(min_bound2,max_bound2))
    cost, pos = optimizer2.optimize(multi_cost_func_sird, iters=40, df=df0, N=population)
    pos_res.append(pos)
    if cost<min_func:
        min_func=cost
        best_pos=pos
    return pos,min_func


## Logistic Model

def logistic_model(x,T_range):
    param_a,param_b,param_c,param_d,param_e=x
    RES=[]
    for t0 in T_range:  
        inx=(-param_d*t0)+param_e
        log=param_a/(param_b+(param_c*np.exp(inx)))
        RES.append(log)
        
    return np.array(RES)

def cost_func_logistic(x,df,with_pred=False,factor=1):
    ## time range
    T_start = 0.0
    T_inc=1.0
    T_end=df.shape[0]

    T_range = np.arange(T_start, T_end+T_inc, T_inc)
    RES = logistic_model(x,T_range)
    df['Cumulative_pred']=pd.DataFrame(RES)

    err=(((df['Cumulative']-df['Cumulative_pred'])*df['weight'])**2).mean()*0.05

    if with_pred:
        return df, err*factor
    else:
        return err*factor
    
def multi_cost_func_logistic(x,df,factor=1):
    all_res=[]
    for i in x:
        res=cost_func_logistic(i,df,factor=factor)
        all_res.append(res)
    return np.array(all_res)

def pso_logistic(df0,max_bound,min_bound=[30000, 30, 90, 0.01, 1],factor=1):
    opt1 = {'c1': 0.15, 'c2': 0.95, 'w':0.25}
    pos_res=[]
    best_pos=[]
    min_func=5000000
    for i in range(3):
        optimizer1 = ps.single.GlobalBestPSO(n_particles=350, dimensions=5, options=opt1,
                                             bounds=(min_bound,
                                                     max_bound))
        # Perform optimization
        cost, pos = optimizer1.optimize(multi_cost_func_logistic, iters=40, df=df0, factor=factor)
        pos_res.append(pos)
        if cost<min_func:
            min_func=cost
            best_pos=pos

    max_bound2=np.array(pos_res).max(axis=0)
    max_bound2=max_bound2+(max_bound2*0.08)
    min_bound2=np.array(pos_res).min(axis=0)
    min_bound2=min_bound2-(min_bound2*0.08)
    optimizer2 = ps.single.GlobalBestPSO(n_particles=450, dimensions=5, options=opt1,
                                             bounds=(min_bound2,max_bound2))
    cost, pos = optimizer2.optimize(multi_cost_func_logistic, iters=50, df=df0, factor=factor)
    pos_res.append(pos)
    if cost<min_func:
        min_func=cost
        best_pos=pos
    return pos,min_func