from textblob import TextBlob
import codecs
import emoji
import csv
import re
import os

# Takes a .csv file and scrapes all of its rows and columns 
# then puts of its data in a single column
def formatFile():
    with open('tweets.csv', 'r') as input_file:
        with open('formated.csv', 'w', newline='') as output_file:
            reader = csv.reader(input_file)
            writer = csv.writer(output_file)
            for row in reader:
                for cell in row:
                    writer.writerow([cell])
    input_file.close()
    output_file.close()

# Makes the emojis readable for the program
def decode(input):
    string = codecs.decode(input, 'unicode_escape')
    encodedTweet = string.encode('latin-1')
    decodedTweet = encodedTweet.decode('utf-8')
    return decodedTweet

# Cleans the text of any links, usernames, and # before a hashtag
# it also converts emoji into its word meaning so textblob can evaluate it's seniment score
def filter(input):
    filteredString = emoji.demojize(input)
    filteredString = re.sub(r'https?://\S+', '' , filteredString)
    filteredString = re.sub(r'@\S+', '' ,filteredString)
    filteredString = re.sub(r'[:_]', ' ', filteredString)
    filteredString = re.sub(r'#', '', filteredString)
    return filteredString

# Calculates the input's sentiment score on a scale from -1 to 1
def sentimentScore(input):
    string = TextBlob(input)
    sentiment = string.sentiment.polarity
    return sentiment

# Classifies the score as positive, negitive, or neutral
def sentimentClassification(input):
    if input > 0:
        classification = "positive"
    elif input < 0:
        classification = "negitive"
    else:
        classification = "neutral"
    return classification

print("Calulating the sentiment score of tweets...")

formatFile()

with open('formated.csv', 'r', encoding='utf-8') as input_file:
    
    with open('sentiment_score_of_tweets.csv', 'w', newline='') as output_file:

        reader = csv.reader(input_file)
        writer = csv.writer(output_file)
        
        for row in reader:

            tweet = decode(row[0])
            text = filter(tweet)
            rating = sentimentScore(text)
            classification = sentimentClassification(rating)

            writer.writerow([rating, classification, row[0]])

input_file.close()
output_file.close()    
os.remove("formated.csv")

print("Done, the sentiment scores of the tweets have been compiled in sentiment_score_of_tweets.csv")