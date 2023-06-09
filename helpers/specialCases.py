import csv, sys, json


def specialCases(inputData):

  OmittedCamps = {}
  with open('InputData/EF2023 - Special Requests.csv', newline='', encoding='utf-8') as f:
    SpecialRequests = csv.DictReader(f)  

    try:
      for row in SpecialRequests:
        # print(row)
        camp_section = row['Camp Section']
        camp_key = row['Camp Key']
        inputData["CampSectionData"][camp_section]["size"]-=inputData["Camps"][camp_key]
        OmittedCamps[camp_key] = inputData["Camps"][camp_key]
        del inputData["Camps"][camp_key]

    except csv.Error as e:
      sys.exit('file {}, line {}: {}'.format(row, SpecialRequests.line_num, e))

    inputData["OmittedCamps"] = OmittedCamps
    with open("InputData.json", "w") as outfile:
            json.dump(inputData, outfile)   
    return inputData


def reAddSpecialCases(solution, camps):
  data = {
        "Sections": solution.sectionsSortedNames,
        "CampAreas": solution.sectionSolutions,
        "Camps":solution.campsSolutions,
        "CampLengths":solution.campLengthsSolutions,
    }
  print('data',data)
  

  with open('InputData/EF2023 - Special Requests.csv', newline='', encoding='utf-8') as f:
    SpecialRequests = csv.DictReader(f)  

    try:
      for row in SpecialRequests:
        camp_section = row['Camp Section']
        camp_key = row['Camp Key']
        section_width = row['Section Width']
        # find and add camp to solution
        index = data["Sections"].index(camp_section)
        data["Camps"][index].insert(0,camp_key)
        data["CampAreas"][index].insert(0,camps[camp_key])
        data["CampLengths"][index].insert(0,round(int(camps[camp_key])/int(section_width)))

    except csv.Error as e:
      sys.exit('file {}, line {}: {}'.format(row, SpecialRequests.line_num, e))

    print('new data',data)

    return data
                          

