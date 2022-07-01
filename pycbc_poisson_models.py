import numpy
from scipy import stats
from pycbc.inference.models.base import BaseModel
from pycbc.inference.models.base_data import BaseDataModel

"""Simple example of a custom PyCBC model."""

class TestPoisson(BaseModel):
    """A model with a Poisson distribution for the likelihood."""
    name = 'test_poisson'
    
    def _loglikelihood(self):
        # get the current parameters;
        # they should have a mu and a counts
        params = self.current_params
        try:
            mu = params['mu']
            kk = int(params['k'])
        except KeyError:
            raise ValueError("must provide a mu and a k")
        return stats.poisson.logpmf(kk, mu)


class PoissonBurst(BaseModel):
    """A model in which the noise model is Poissonian and the signal model
    is an exponentially decaying burst.
    """
    name = 'poisson_burst'
    
    def __init__(self, times, counts, variable_params, **kwargs):
        super().__init__(variable_params, **kwargs)
        # store the data
        self.times = times
        self.counts = counts
        
    def _loglikelihood(self):
        params = self.current_params
        # the signal model
        amp = params['amp']
        tau = params['tau']
        t0 = params['t0']
        # generate the signal
        times = self.times
        signal = self.get_signal(times, amp, tau, t0)
        # subtract the signal from the observed data
        residual = self.counts - signal
        # make sure the residual is positive
        residual[residual < 0] = 0
        # the noise model parameters
        mu = params['mu']
        # the loglikelihood is the sum over the time series
        return stats.poisson.logpmf(residual, mu).sum()

    @staticmethod
    def get_signal(times, amp, tau, t0):
        """Generate the signal model.
        
        Having a function like this isn't required for the model;
        the signal could just be generated within the ``_loglikelihood``
        function. We break it out to a separate function here to
        make it easier to generate a simulated signal.
        """
        signal = numpy.zeros(len(times))
        mask = times >= t0
        signal[mask] = (amp*numpy.exp(-(times[mask]-t0)/tau)).astype(int)
        return signal
        
    @classmethod
    def from_config(cls, cp, **kwargs):
        """Loads the counts data in addition to the standard parameters.
        
        This requires a [data] section to exist in the config file that
        points to a text file containing the times and counts; example:
        
            [data]
            counts-data = /path/to/txt
        """
        # get the data
        datafn = cp.get('data', 'counts-data')
        data = numpy.loadtxt(datafn)
        times = data[:,0]
        counts = data[:,1]
        args = {'times': times, 'counts': counts}
        args.update(kwargs)
        return super().from_config(cp, **args)


class PoissonBurst2(BaseDataModel):
    """A model in which the noise model is Poissonian and the signal model
    is an exponentially decaying burst.

    This illustrates modifying the ``from_config`` file to load data, and
    inheriting from BaseDataModel. Note that inheriting from BaseDataModel is
    not necessary if a model uses data; the only requirement is that the model
    is an instance of BaseData; the ``from_config`` could be modified just as
    well to load data. BaseDataModel makes it so that functions to compute the
    noise likelihood and likelihood ratio must be defined.
    """
    name = 'poisson_burst2'
    
    @property
    def times(self):
        return self.data['counts'][:, 0]

    @property
    def counts(self):
        return self.data['counts'][:, 1]

    def _lognl(self):
        # the log likelihood assuming no signal exists in the data
        mu = self.current_params['mu']
        return stats.poisson.logpmf(self.counts, mu).sum()

    def _loglikelihood(self):
        # the log likelihood assuming the data consists of the noise model +
        # the signal model
        params = self.current_params
        # the signal model
        amp = params['amp']
        tau = params['tau']
        t0 = params['t0']
        # generate the signal
        times = self.times
        signal = self.get_signal(times, amp, tau, t0)
        # subtract the signal from the observed data
        residual = self.counts - signal
        # make sure the residual is positive
        residual[residual < 0] = 0
        # the noise model parameters
        mu = params['mu']
        # the loglikelihood is the sum over the time series
        self.current_stats['lognl'] = self.lognl
        return stats.poisson.logpmf(residual, mu).sum()

    def _loglr(self):
        # the log likelihood ratio
        return self.loglikelihood - self.lognl

    @staticmethod
    def get_signal(times, amp, tau, t0):
        """Generate the signal model.
        
        Having a function like this isn't required for the model;
        the signal could just be generated within the ``_loglikelihood``
        function. We break it out to a separate function here to
        make it easier to generate a simulated signal.
        """
        signal = numpy.zeros(len(times))
        mask = times >= t0
        signal[mask] = (amp*numpy.exp(-(times[mask]-t0)/tau)).astype(int)
        return signal
        
    @classmethod
    def from_config(cls, cp, **kwargs):
        """Loads the counts data in addition to the standard parameters.
        
        This requires a [data] section to exist in the config file that
        points to a text file containing the times and counts; example:
        
            [data]
            counts-data = /path/to/txt
        """
        # get the data
        datafn = cp.get('data', 'counts-data')
        data = {'counts': FrequencySeries(numpy.loadtxt(datafn), delta_f=1)}
        args = {'data': data}
        args.update(kwargs)
        return super().from_config(cp, **args)

from pycbc.types import FrequencySeries
