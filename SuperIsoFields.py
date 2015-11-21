"""Declare all the fields & associated regexes you want for pulling info from SuperIso spectrum file"""


from collections import namedtuple
import re


Field = namedtuple('Field', ['block', 'regex', 'name', 'type'])

superiso_fields = []