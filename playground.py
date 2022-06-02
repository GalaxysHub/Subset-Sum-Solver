import csv, sys
import json

global data
with open('InputData.json', 'r') as f:
  data = json.load(f)


campdata = list(data['CampSectionData'].values())
print(campdata)
res = [d['size'] for d in campdata]
print(res)

# filename = 'Solutions.csv'
# with open(filename, newline='') as f:
#     reader = csv.reader(f)
#     try:
#         for row in reader:
#             print(row)
#     except csv.Error as e:
#         sys.exit('file {}, line {}: {}'.format(filename, reader.line_num, e))