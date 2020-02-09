import pandas as pd 

import numpy as np

from engines import recognize as re

df = pd.read_csv("./engines/date.csv")

x = re.Recognize(df.loc[1:1000 ,:])

a = x.make_table()
