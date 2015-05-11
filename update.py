# this file contains the update and calculation functions used for the string simulation

import numpy as np
import scipy.sparse as sparse

# parameter imports
from parameters import b_h, m_h
from parameters import labda, kappa, rho
from parameters import b1, b2, zeta_l, zeta_b
from parameters import c, dx, dt, n

# update the vector with eta values
# eta -> vector with eta values
# f0 -> force at the point x0
def update_eta(eta, f0):

    d1 = 2/(1+b_h*dt/(2*m_h))
    d2 = (b_h*dt/(2*m_h)-1)/(1+b_h*dt/(2*m_h))
    d_f = (-dt**2/m_h)/(1+b_h*dt/(2*m_h))
            
    eta = np.append(eta, d1*eta[-1]+d2*eta[-2]+d_f*f0)
    print eta
    return eta

# update the displacement vector according to
# u(n+1) = A*u(n) + B*u(n-1) + C*F
#
# NB: C and F are optional
def update_displacement(u, u_previous,  A, B, C = None, F = None):

    u_next = A*u + B*u_previous
    if (C is not None) and (F is not None):
        u_next += C*F

    return u_next, u

# calculate the matrices A and B for the update of eta
def calculate_AB():

    mu = (kappa/(c*dx))**2
    nu = 2*b2*dt/dx**2

    a1 = -mu*labda**2/(1+b1*dt)
    a2 = (nu + (1+4*mu)*labda**2)/(1+b1*dt)
    a3 = (2 - 2*nu - (2+6*mu)*labda**2)/(1+b1*dt)
    a4 = (b1*dt + 2* nu - 1)/(1+b1*dt)
    a5 = -nu/(1+b1*dt)

    A = a3*sparse.eye(n,n,0) + a2*(sparse.eye(n,n,-1) + sparse.eye(n,n,1)) \
        + a1*(sparse.eye(n,n,-2) + sparse.eye(n,n,2))
    B = a4*sparse.eye(n,n,0) + a5*(sparse.eye(n,n,-1) + sparse.eye(n,n,1))

    # br1 = 2.-(2*mu-2)*labda**2 / (1 + b1*dt + zeta_b*labda)
    # br2 = (4*mu+2)*labda**2 / (1 + b1*dt + zeta_b*labda)
    # br3 = -2*mu*labda**2 / (1 + b1*dt + zeta_b*labda)
    # br4 = (-1 + b1*dt + zeta_b*labda)/(1 + b1*dt + zeta_b*labda)
    # bl1 = 2.-(2*mu-2)*labda**2 / (1 + b1*dt + zeta_l*labda)
    # bl2 = (4*mu+2)*labda**2 / (1 + b1*dt + zeta_l*labda)
    # bl3 = -2*mu*labda**2 / (1 + b1*dt + zeta_l*labda)
    # bl4 = (-1 + b1*dt + zeta_l*labda)/(1 + b1*dt + zeta_l*labda)
    #
    # # boundary conditions
    # A[-2,n-2] = a3-a1
    # A[-2,n-1] = 2*a1+a2
    # A[1,1] = a3-a1
    # A[1,0] = 2*a1+a2
    #
    # A[-1,-1] = br1
    # A[-1,-2] = br2
    # A[-1,-3] = br3
    # B[-1,-1] = br4
    # B[-1,-2] = 0.
    #
    # A[0,0] = bl1
    # A[0,1] = bl2
    # A[0,2] = bl3
    # B[0,0] = bl4
    # B[0,1] = 0.

    return A, B

# calculate the matrix C for the update of eta
def calculate_C():

    C = (dt**2/rho)/(1+b1*dt)*np.ones(n)

    # boundary conditions
    C[0] = (dt**2/rho)/(1 + b1*dt + zeta_l*labda)
    C[-1] = (dt**2/rho)/(1 + b1*dt + zeta_b*labda)

    return sparse.diags(C,0)