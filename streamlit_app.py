import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import plotly.io as pio
import plotly.graph_objects as go
from scipy.integrate import solve_ivp

st.set_page_config(layout="wide")

r"""
# Logistická rovnice s lovem

Rovnice je logistická rovnice obohacená o konstantní lov. Používá se k modelování ekologicky udržitelného 
lovu v populaci žijící v prostředí s omezenou nosnou kapacitou.

$$ 
\frac{\mathrm dx}{\mathrm dt}=rx\left(1-\frac xK\right)-h
$$

"""

col1, col2 = st.columns(2)

with col1:
    K = st.slider(r"$K$ (nosná kapacita prostředí)", 0.1, 10.0, 1.0)
    r = st.slider(r"$r$ (rychlost růstu)", .1, 10.0, 1.0)
    h = st.slider(r"$h$ (intenzita lovu)", 0.0, 1.0, .1)

meze = [0,10]
n = 1000
t = np.linspace(*meze,n)
N = 50
reseni = np.empty((n,N))
reseni[:,:] = np.nan

def destrukce_populace(t,x):  # Pokud x klesne na nulu, zastavíme výpočet
    return x
destrukce_populace.terminal = True

# %%
for i,pp in enumerate(np.linspace(0.05,K*1.4,N)):
    sol = solve_ivp(
                   lambda t,x: r*x*(1-x/K)-h,
                   meze,
                   [pp],
                   t_eval=t,
                   events=destrukce_populace,
                   ).y
    reseni[:sol.size,i] = sol

# %%

fig = go.Figure()

for res in reseni.T:
    # if np.isnan(res).any():
    if (r*K/2*(1-K/2/K)<h) or (res[0]< K/2 and r*res[0]*(1-res[0]/K)-h)<0:
        color='red'
    else:
        color='gray'
    fig.add_trace(go.Scatter(x=t, y=res, mode='lines', line=dict(color=color)))
fig.update_xaxes(title_text="Čas")
fig.update_yaxes(title_text="Velikost populace")
fig.update_layout(showlegend=False)

# %%
# fig2,ax2 = plt.subplots()
x = np.linspace(0,1.3*K,500)
# ax2.plot(x,r*x*(1-x/K), color='blue')
# ax2.plot(x,h+x*0, color='red')
# ax2.set(ylim=(0,None))
fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=x, y=r*x*(1-x/K), mode='lines', line=dict(color='blue')))
fig2.add_trace(go.Scatter(x=x, y=x*0+h, mode='lines', line=dict(color='red')))
fig2.update_layout(showlegend=False)
fig2.update_yaxes(range = [0,None])


with col2:
    tab1,tab2 = st.tabs(["Časový vývoj","Graf pravé strany"])
    with tab1:
        st.plotly_chart(fig)
    with tab2:
        st.plotly_chart(fig2)
