from update import *
from plot_and_save import *
from Parameters.parametersA2 import n, n_t, n0

animate = False          # animate the wave in the string upon completion
plot = False             # plot the waveform and frequency spectrum on the piano bridge
write_file = True       # write the waveform on the bridge to a .wav file
filename = "./Notes/pianoA2.wav"

# calculate matrices
A, B = calculate_AB()
C = calculate_C()

# initialize eta and u
eta = update_eta(init=True)
u = u_old = 1.*np.zeros(n)

ims = np.zeros((n_t/10, n))
u_bridge = np.zeros(n_t)
for i in range(n_t):

    u_bridge[i] = u[-1]
    if i%10==0 and animate:
        ims[i/10,:] = u

    if eta[1] >= 0.: # eta[0]:
        force = calculate_force(eta[1], u[n0])
        u, u_old = update_displacement(u, u_old, A, B, C, force)
        eta = update_eta(eta, force[n0])
    else:
        u, u_old = update_displacement(u, u_old, A, B)

    # print float(i)/n_t

# animate, plot and save
if animate: animate_string(ims)
if plot:
    plot_u_bridge(u_bridge)
    plot_frequency(u_bridge)
if write_file: save_to_wav(u_bridge, filename)