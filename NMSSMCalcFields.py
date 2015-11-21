"""Declare all the fields & associated regexes you want for pulling info from NMSSMCalc spectrum file"""


from collections import namedtuple
import re


Field = namedtuple('Field', ['block', 'regex', 'name', 'type'])

nmssmcalc_fields = []