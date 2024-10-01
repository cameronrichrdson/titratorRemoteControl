import os
from importlib.resources import read_text

import pandas as pd


dir = os.chdir('/Users/cameronrichardson/Documents/School/Thesis/Code/titrations/')
d = read_text(dir[1])

vol =