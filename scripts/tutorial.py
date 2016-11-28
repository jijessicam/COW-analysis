import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
pd.set_option('max_columns', 50)


# Part 1: series
# Create series with arbitrary list
s = pd.Series([7, 'Heisenberg', 3.14, -12312412512, 'Happy Eating!'])
# can specify index when creating series
print s

# reading in a CSV

from_csv = pd.read_csv("interstate_wars.csv")
from_csv.head()