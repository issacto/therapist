import csv

csv.field_size_limit(100000000)
outputTrainFileName="output/train.csv"
outputTestFileName="output/test.csv"

def writeToFile(csv_file, new_data):
    with open(csv_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(new_data)

def formatData(prompt, answer):
    return ['<s>[INST] ' + prompt + ' [/INST] ' + answer + ' </s>']

################## Write starts here
writeToFile(outputTrainFileName,[['Text']])
writeToFile(outputTestFileName,[['Text']])

reddit_csv = "raw/reddit.csv"
### ['prompt', 'completion']
with open(reddit_csv, mode='r') as file:
    csv_reader = csv.reader(file)
    header = next(csv_reader)
    data=[]
    for row in csv_reader:
        data.append(formatData(row[0],row[1]))
    writeToFile(outputTrainFileName,data)

psych_csv = "raw/psych.csv"
### ['', 'Answer', 'Question', 'Therapist', 'time'

with open(psych_csv, mode='r') as file:
    # Create a CSV reader object
    csv_reader = csv.reader(file)
    header = next(csv_reader)
    data=[]
    for row in csv_reader:
        data.append(formatData(row[2],row[1]))
    writeToFile(outputTrainFileName,data)



counselchat_csv = "raw/counselchat.csv"
#['questionID', 'questionTitle', 'questionText', 'questionUrl', 'topics', 'therapistName', 'therapistUrl', 'answerText', 'upvotes']
with open(counselchat_csv, mode='r') as file:
    # Create a CSV reader object
    csv_reader = csv.reader(file)
    header = next(csv_reader)
    data=[]
    for row in csv_reader:
         data.append(formatData(row[2],row[7]))
    writeToFile(outputTestFileName,data)
