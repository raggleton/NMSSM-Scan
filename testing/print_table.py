#!/usr/bin/env python

import pandas as pd
import sys

pd.set_option('display.max_columns', 200)
pd.set_option('colheader_justify', 'left')
pd.set_option('display.width', None)

df = pd.read_csv(sys.argv[1])
print df.to_json()
