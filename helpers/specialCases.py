import csv, sys, json



global inputData
with open('InputData.json', 'r') as f:
  inputData = json.load(f)



def specialCases():
  print('inputdata:', inputData)

  with open('InputData/EF2023 - SpecialCases.csv', newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)  
    try:
      for row in reader:
        print(row)
        campSection = row['Camp Section']
        groupName = row['Camp Key']
        size = int(row['Size'])



    except csv.Error as e:
      sys.exit('file {}, line {}: {}'.format(row, reader.line_num, e))
                                             


specialCases()

sys.modules[__name__] = specialCases
