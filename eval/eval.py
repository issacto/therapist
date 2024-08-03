import csv
import function
import sys

sys.path.insert(0, "../predict")
from itertools import zip_longest

from predict import predict

input_file = "./data/questions.csv"
delimiter="∞"

## Open the CSV file
def process_file(output_file, mode):
    with open(input_file, mode="r", newline="") as input_csvfile:
        csvreader = csv.DictReader(input_csvfile)
        # Open the output CSV file
        with open(output_file, mode="w", newline="") as output_csvfile:
            csvwriter = csv.writer(output_csvfile)
            csvwriter.writerow(["Text"])
            # Iterate over each row in the input CSV file
            for row in csvreader:
                question = row["Text"]
                print("question")
                print(question)
                resopnse = predict(question, mode)
                # preiction
                csvwriter.writerow([question, resopnse])


# sentiment_analyse(question, response), simplicity_analyse, recylcing_analyse
## Open the CSV file
def evaluate(output_file):
    with open(input_file, mode="r", newline="") as f1, open(
        output_file, mode="r", newline=""
    ) as f2:
        reader1 = csv.reader(f1, delimiter= delimiter)
        reader2 = csv.reader(f2, delimiter= delimiter)

        # Read and skip the headers
        header1 = next(reader1)
        header2 = next(reader2)

        # Verify that headers match
        if header1 != header2:
            raise ValueError("CSV files have different headers")
        totalI = 15
        simpI = 0
        sentiment_score = 0
        simplicity_score = 0
        recylcing_score = 0
        # Loop over the rows of both files simultaneously, using None to fill shorter file
        for row1, row2 in zip_longest(reader1, reader2, fillvalue=None):
            sentiment_score = sentiment_score +function.sentiment_analyse(row1[0],  row2[0])
            # simplicity_analyse
            simplicity_tmp_score = function.simplicity_analyse( row2[0])
            if(simplicity_tmp_score!="under 100words"):
                simpI+=1
                simplicity_score=simplicity_score+simplicity_tmp_score
            recylcing_score = recylcing_score+ function.recylcing_analyse(row1[0],  row2[0])

        print('sentiment_score ',sentiment_score, sentiment_score/totalI)
        if(simpI!=0):
            print('simplicity_score ',sentiment_score/simpI )
        print('recylcing_score ',recylcing_score/totalI)

def printForGPT(output_file):
    with open(input_file, mode="r", newline="") as f1, open(
        output_file, mode="r", newline=""
    ) as f2:
        reader1 = csv.reader(f1, delimiter= delimiter)
        reader2 = csv.reader(f2, delimiter= delimiter)

        # Read and skip the headers
        header1 = next(reader1)
        header2 = next(reader2)

        # Verify that headers match
        if header1 != header2:
            raise ValueError("CSV files have different headers")
        # Loop over the rows of both files simultaneously, using None to fill shorter file
        i=1
        for row1, row2 in zip_longest(reader1, reader2, fillvalue=None):
            print(f"{i}. Message: {row1[0]}, \nResponse: {row2[0]} \n")
            i+=1

def main():
    ############# PROCESS FILES
    # process_file("./data/therapist-ft.csv",'ft')
    # process_file("./data/vanilla.csv",'vanilla')
    # process_file("./data/therapist-pe.csv",'pe')
    ############# EVALUATE FILES
    # evaluate("./data/vanilla.csv")
    # evaluate("./data/therapist-pe.csv")
    # evaluate("./data/therapist-ft.csv")
    ############# PRINT FILES
    # printForGPT("./data/vanilla.csv")
    # printForGPT("./data/therapist-pe.csv")
    printForGPT("./data/therapist-ft.csv")



main()
