import csv
import json
import pandas as pd
import re


def getDictFromJsonPath(jsonPath):
    with open(jsonPath, 'r') as file:
        jsonString = file.read()
        return json.loads(jsonString)


def saveDataFramesAsCSV(dataframe, savePath):
    dataframe.to_csv(savePath)


def cleanText(text):
    badPhrasesRE = re.compile("\\u00b7|\\u2022|\(cid:173\)")
    text = re.sub(badPhrasesRE, "", text)
    return text


speakerRE = re.compile(
    "M[rs]{1,2}\.\s[A-Z]{2,}\s[A-Z]\.\s[A-Z]{2,}\."
    "|M[rs]{1,2}\.\s[A-Z ]{2,}\."
    "|The VICE PRESIDENT."
    "|The PRESIDENT."
    "|M[rs]{1,2}\. SPEAKER"
    "|The PRESIDING OFFICER."
    "|M[rs]{1,2}\. [A-Z ]{2,} of [A-Z][a-z]+\."
    # "|STATEMENT BY [ A-Z]{2,}\s"
)

startingYear = 1974
endingYear = 1974  # 2018

for year in range(startingYear, endingYear + 1):

    rawRecordsPath = '../../data/json/raw/raw_json-{:d}.json'.format(year)
    rawRecords = getDictFromJsonPath(rawRecordsPath)
    for year, partDict in rawRecords.items():
        yearlyResults = []
        for part, pageDict in partDict.items():
            for page, text in pageDict.items():

                text = cleanText(text)

                speakers = re.findall(speakerRE, text)
                speeches = speakerRE.split(text)

                for i in range(len(speakers)):
                    speaker = speakers[i]
                    speech = speeches[i + 1]
                    yearlyResults.append({
                        'year': year,
                        'part': part,
                        'page': page,
                        'speaker': speaker,
                        'speech': speech,
                    })
        savePath = '../../data/csv/processed/record-{:s}.csv'.format(year)
        yearlyResultsDF = pd.DataFrame(yearlyResults)
        saveDataFramesAsCSV(yearlyResultsDF, savePath)
