import csv
import wikipediaapi

def get_wikipedia_summary(topic):
    wiki_wiki = wikipediaapi.Wikipedia(
            language='en',
            extract_format=wikipediaapi.ExtractFormat.WIKI,
            user_agent='therapist'
        )
    page = wiki_wiki.page(topic)
    if page.exists():
        return page.summary
    else:
        return f"Page '{topic}' does not exist on Wikipedia."

def read_disorders_from_csv(file_path):
    disorders = []
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip the header row
        for row in csv_reader:
            if row:  # Check if the row is not empty
                disorders.append(row[0].strip())
    return disorders

def write_summary_to_txt(file_path, summary):
    with open(file_path, mode='a', encoding='utf-8') as file:
        file.write(f"{summary}\n\n")
        file.write("<end-of-paragraph>")
        # file.write(f"Summary for {disorder}:\n{summary}\n\n")
#
def main():
    file_input_path = './raw/disorders.csv'
    file_output_path = './output/disorders_description.txt'
    disorders = read_disorders_from_csv(file_input_path)
    
    for disorder in disorders:
        summary = get_wikipedia_summary(disorder)
        write_summary_to_txt(file_output_path,summary)
        # print(f"Summary for {disorder}:\n{summary}\n")

if __name__ == "__main__":
    main()