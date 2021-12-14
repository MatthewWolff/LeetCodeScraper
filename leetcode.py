#!/usr/bin/env python3
import argparse
import os
import sys
from glob import glob

import pandas as pd

# change to script's directory for relative paths
os.chdir(sys.path[0])

# adjust pandas printing
pd.options.display.max_colwidth = 180
pd.set_option("display.max_rows", None)

# update choices based on local files
companies = [os.path.basename(file).replace("_problems.csv", "") for file in glob(os.path.join("outputs", "*.csv"))]

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--company", choices=companies, default="amazon")
parser.add_argument("-d", "--difficulty", choices=["any", "easy", "medium", "hard"], default="any")
parser.add_argument("-n", "--num", help="show at most this many problems", default=15, type=int)
args = parser.parse_args()

df: pd.DataFrame = pd.read_csv(os.path.join("outputs", args.company + "_problems.csv"))
difficulty = ~df.difficulty.isna() if args.difficulty == "any" else df.difficulty == args.difficulty
df = df[difficulty].head(args.num)
print(df[["title", "difficulty", "times", "link"]])
