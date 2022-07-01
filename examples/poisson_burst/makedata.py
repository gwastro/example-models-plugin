#!/usr/bin/env python

"""Makes simulated data that consists of some noise with a burst signal added.
The data are written to a text file.
"""

import numpy
from scipy import stats
from pycbc_poisson import PoissonBurst

# set a seed to make this reproducible
numpy.random.seed(10)

duration = 32
times = numpy.arange(duration)
# noise parameters
mu = 4
# generate some fake noise
noise = stats.poisson.rvs(mu, size=duration)

# simulated signal properties
t0 = duration/4
# we'll make the signal be a 10 sigma
# deviation from the noise
amp = 10 * mu**0.5 + mu
tau = duration/8
print('Signal parameters:')
print('amp: {}, tau: {}, t0: {}'.format(amp, tau, t0))
signal = PoissonBurst.get_signal(times, amp, tau, t0)

# the "observed" data
data = signal + noise
# save the data to a file
numpy.savetxt('simulated_data.txt', numpy.vstack((times, data)).T)
