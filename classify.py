import io, json, csv, sys
from datetime import datetime

#convert csv to json in order to ensure column strict-ness
def convert_csv_to_json(csv_file_path, json_file_path):
    data = []
    with open(csv_file_path, 'r', newline='', encoding='ANSI') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for row in csv_reader:
            data.append(row)

    with open(json_file_path, 'w', encoding='ANSI') as jsonfile:
        json.dump(data, jsonfile, indent=4)

def formatTempFileName(inputFileName):
    formattedFileName = 'converted_' + inputFileName[:-3] + '.json'
    return formattedFileName

try:
    testCSVFile = sys.argv[1]
    classCSVFile = sys.argv[2]
except IndexError:
    print("Please specify two csv files to compare. ex:")
    print()
    print("python classify.py \"FilePath_To_Sample_Data_Set.csv\" \"FilePath_To_Classifications.csv\"")
    print()
    print("Exiting with error code 1")
    sys.exit(1)

testJsonFile = formatTempFileName(testCSVFile)
classJsonFile = formatTempFileName(classCSVFile)

convert_csv_to_json(testCSVFile, testJsonFile)
convert_csv_to_json(classCSVFile, classJsonFile)

testFile = open(testJsonFile)
testData = json.load(testFile)

classFile = open(classJsonFile)
trainedCellClassificationData = json.load(classFile)

positiveClassifications = {}

#first build positive classification dictionary to make lookups fast AF
for trainedClassification in trainedCellClassificationData:
    for c in trainedClassification:
        if trainedClassification[c] == '1':
            if c in positiveClassifications:
                positiveClassifications[c] += ", " + trainedClassification['Cell Type']
            else:
                positiveClassifications[c] = trainedClassification['Cell Type']

#then iterate over sample data and inject new kvp which is PositiveClassifications v a csv string of its associations
for test in testData:
    tmp = test['Classification'].split(':')
    for t in tmp:
        t = t.strip()
        if t in positiveClassifications:
            test['PositiveClassifications'] = positiveClassifications[t]

outputFileName = 'classificationOutput-' + datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '.json'

with io.open(outputFileName, 'w', encoding='utf-8') as f:
  f.write(json.dumps(testData, ensure_ascii=False))