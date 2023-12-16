import altair as alt
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

r"""
# Logistická rovnice s lovem

Rovnice je logistická rovnice obohacená o konstantní lov. Používá se k modelování ekologicky udržitelného 
lovu v populaci žijící v prostředí s omezenou nosnou kapacitou.

$$ \displaystyle \frac{\mathrm dx}{\mathrm dt}=rx\left(1-\frac xK\right)-h$$

"""

col1, col2 = st.columns(2)

with col1:
    K = st.slider("K", 0.1, 10.0, 1.0)
    r = st.slider("r", .1, 10.0, 1.0)
    h = st.slider("h", 0.0, 1.0, .1)

meze = [0,10]
n = 1000
t = np.linspace(*meze,n)
N = 50
reseni = np.zeros((n,N))

# %%
for i,pp in enumerate(np.linspace(0.05,K*1.4,N)):
    sol = solve_ivp(
                   lambda t,x:0 if x<0 else r*x*(1-x/K)-h,
                   meze,
                   [pp],
                   t_eval=t
                   ).y
    reseni[:sol.size,i] = sol

fig, ax = plt.subplots()    
ax.plot(t,reseni, color='gray')
ax.set(ylim=(0,reseni.max()))

with col2:
    st.pyplot(fig)
