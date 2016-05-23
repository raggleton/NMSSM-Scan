"""Declare all the fields & associated regexes you want for pulling info from NMSSMTools spectrum file"""


from collections import namedtuple
import re


Field = namedtuple('Field', ['block', 'regex', 'name', 'type'])


higgsbounds_fields = [
    # HiggsBounds results
    Field(block='HiggsBoundsResults', name="HBresult", type=float,
          regex=re.compile(r' +\d +\d +([01\-]) +\# HBresult')),
    Field(block='HiggsBoundsResults', name="HBobsratio", type=float,
          regex=re.compile(r' +\d +\d +([E\d\.\-\+]+) +\# obsratio')),
    Field(block='HiggsBoundsResults', name="HBchannel", type=float,
          regex=re.compile(r' +\d +\d +([E\d\.\-\+]+) +\# channel id number')),
]

higgssignals_fields = [
    # Higgssignals results
    Field(block='HiggsSignalsResults', name='HSprob', type=float,
          regex=re.compile(r' +13 +([E\d\.\-\+]+) +\# Probability ')),
    Field(block='HiggsSignalsResults', name='HSchi2', type=float,
          regex=re.compile(r' +12 +([E\d\.\-\+]+) +\# chi\^2 \(total\)')),
    Field(block='HiggsSignalsResults', name='HSnobs', type=int,
          regex=re.compile(r' +7 +([E\d\.\-\+]+) +\# Number of observables \(total\)')),

]

# Observation-specific fields
for chan in range(1, 86):
  chan_field = Field(block='HiggsSignalsPeakObservables', name='HS_%d_muPred' % chan, type=float,
                     regex=re.compile(r' +%d +17 +([E\d\.\-\+]+) +\# Total predicted signal strength modifier mu' % chan))
  higgssignals_fields.append(chan_field)
  chi2_field = Field(block='HiggsSignalsPeakObservables', name='HS_%d_chi2' % chan, type=float,
                     regex=re.compile(r' +%d +20 +([E\d\.\-\+]+) +\# Chi\-squared value \(total\)' % chan))
  higgssignals_fields.append(chi2_field)
  # chan_field = Field(block='HiggsSignalsPeakObservables', name='HS_%d_muObs' % chan, type=float,
  #                    regex=re.compile(r' +%d +9 +([E\d\.\-\+]+) +\# Observed signal strength modifier \(mu\)' % chan))
  # higgssignals_fields.append(chan_field)
