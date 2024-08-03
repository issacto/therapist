
from textblob import TextBlob
import math
import re
from readability import Readability


####################1.Sentiment change -> sentiment between question and answer
def analyse_sentiment(text):
  sentiment = TextBlob(text).sentiment.polarity
  return sentiment

def sigmoid(x):
  return 1 / (1 + math.exp(-x))

def sentiment_change(question, response):
  question_polarity = analyse_sentiment(question)
  response_polarity = analyse_sentiment(response)
  change = response_polarity - question_polarity
  
  print('response_polarity', change, question_polarity)
  if(change==0 or question_polarity==0):
     return 0
  percentage_change = (change / abs(question_polarity)) 
  print('percentage_change', percentage_change)
  return percentage_change

def sentiment_analyse(question, response):
    percentage_change = sentiment_change(question, response)
    normalized_change = sigmoid(percentage_change)
    return normalized_change
####################



####################2.Simplicity

def simplicity_analyse(text):
   try:
    results=Readability(text)
    return results.flesch_kincaid().score
   except:
    return "under 100words"

####################


####################3.Recycling Elements

def remove_symbols(text):
    # Remove any non-alphanumeric characters (except spaces) using regex
    return re.sub(r'[^\w\s]', '', text)

fluff_words = ["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves",
                   "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their",
                   "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are",
                   "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an",
                   "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about",
                   "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from", "up",
                   "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once"]

def compare_words(question, answer):
    # Define the list of fluff words
    # Convert both strings to lower case and split them into words
    question_words = question.lower().split()
    answer_words = answer.lower().split()
    # Filter out the fluff words from both lists
    question_words_filtered = [word for word in question_words if word not in fluff_words]
    answer_words_filtered = [word for word in answer_words if word not in fluff_words]
    # Count how many words from compare_words_filtered exist in main_words_filtered
    answer_word_count = sum(1 for word in answer_words_filtered if word in question_words_filtered)
    return answer_word_count

def recylcing_analyse(question, response):
    result = compare_words(remove_symbols(question), remove_symbols(response))
    return result
    print("Number of matching words:", result)

####################



def call_chatgpt(prompt):
    print("calling gpt")
    response = model.generate(prompt=prompt)
    print("calling gpt", response)
    print(response['results'][0]['generated_text'])



####################4.Active Learning

# active_listening_system = "Respond to the prompt exactly and provide strictly a number. With no clarification."


# def active_listening_analyse(question, response):
active_listening_prompt = """From 0 which indicates weak active listening, to 10, which indicates strong active listening, give a rating for the level of active listening between the question and response. Active listening involves how response captures the central message, topic, and reasoning discussed within the question. Say for example, the question says I suffer from depression, abuse, and divorce, and response says it can be challenging to suffer from multiple issues at the same time. This would constitute high active listening because while the words of the question aren’t repeated in
answer, the central message is repeated. If in response to the question, the reponse just said I agree, that would be a low active listening score since it doesn’t capture the content or reasoning of the question. What matters is just whether the central messaging, topic, and reasoning is discussed in the response. 
"""

####################5.Helpfulness
helpfulness_prompt = """From 0, indicating not helpful, to 10, indicating highly helpful, rate the response based on how effectively it addresses the question's concerns and provides meaningful support or guidance. Consider whether the response offers practical advice, empathy, relevant information, or resources that directly address the issue raised in the question. A high rating should reflect how well the response assists the person in understanding, coping with, or resolving their concern, even if it doesn't directly answer with specific solutions."""
####################