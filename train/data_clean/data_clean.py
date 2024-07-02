import csv
import random
# from bs4 import BeautifulSoup


csv.field_size_limit(100000000)
outputTrainFileName = "./output/train.csv"
outputTestFileName = "./output/test.csv"

def formatData(prompt, answer):
    return ['<s>[INST] ' + prompt + ' [/INST] ' + answer + ' </s>']

# def extract_text_from_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    return ' '.join(p.get_text() for p in soup.find_all('p'))

def process_and_split_data(file_path, format_func, prompt_index, answer_index, train_writer, test_writer, is_html=False):
    with open(file_path, mode='r') as file:
        csv_reader = csv.reader(file)
        header = next(csv_reader)
        data = []
        for row in csv_reader:
            answer = row[answer_index]
            if is_html:
                answer = extract_text_from_html(answer)
            data.append(format_func(row[prompt_index], answer))
        random.shuffle(data)
        split_idx = int(len(data) * 0.8)
        train_data = data[:split_idx]
        test_data = data[split_idx:]
        train_writer.writerows(train_data)
        test_writer.writerows(test_data)

# Open the train and test files once and write headers
with open(outputTrainFileName, mode='w', newline='') as train_file, \
     open(outputTestFileName, mode='w', newline='') as test_file:
    
    train_writer = csv.writer(train_file)
    test_writer = csv.writer(test_file)
    
    # Write headers
    train_writer.writerow(['Text'])
    test_writer.writerow(['Text'])
    
    # Process each dataset
    
    # normal data
    process_and_split_data("./raw/psych.csv", formatData, 2, 1, train_writer, test_writer)
    # process_and_split_data("./raw/reddit.csv", formatData, 0, 1, train_writer, test_writer)
    # untidy data
    # process_and_split_data("./raw/counselchat.csv", formatData, 2, 7, train_writer, test_writer,is_html=True)



    