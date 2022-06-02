import csv, sys
import json

with open('InputData.json', 'r') as f:
  data = json.load(f)
  print(data)
  
filename = 'Solutions.csv'
with open(filename, newline='') as f:
    reader = csv.reader(f)
    try:
        for row in reader:
            print(row)
    except csv.Error as e:
        sys.exit('file {}, line {}: {}'.format(filename, reader.line_num, e))