import os
import csv

with open('rename.csv') as f:
    lines = csv.reader(f)
    for line in lines:
        os.rename(line[0], line[1])
