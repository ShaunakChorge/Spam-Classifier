import argparse  # Import argparse for handling command-line arguments
import pickle  # Import pickle for loading the trained model and vectorizer
import string  # Import string for handling punctuation
from nltk.corpus import stopwords  # Import stopwords from NLTK
import nltk  # Import NLTK for text processing
from nltk.stem.porter import PorterStemmer  # Import PorterStemmer for stemming words

ps = PorterStemmer()  # Initialize the PorterStemmer

def transform_text(text):
    text = text.lower()  # Convert text to lowercase
    text = nltk.word_tokenize(text)  # Tokenize the text into words
    y = []
    for i in text:
        if i.isalnum():  # Check if the word is alphanumeric
            y.append(i)  # Append alphanumeric words to the list
    text = y[:]  # Copy the list of alphanumeric words
    y.clear()  # Clear the list for reuse
    for i in text:
        if i not in stopwords.words('english') and i not in string.punctuation:  # Remove stopwords and punctuation
            y.append(i)  # Append non-stopwords and non-punctuation words
    text = y[:]  # Copy the list of filtered words
    y.clear()  # Clear the list for reuse
    for i in text:
        y.append(ps.stem(i))  # Stem each word and append to the list
    return " ".join(y)  # Join the stemmed words into a single string

tfidf = pickle.load(open('vectorizer.pkl','rb'))  # Load the TF-IDF vectorizer
model = pickle.load(open('model.pkl','rb'))  # Load the trained model

def main():
    parser = argparse.ArgumentParser(description='Classify an SMS as spam or not spam.')  # Create an argument parser
    parser.add_argument('sms', type=str, help='The SMS message to classify')  # Add an argument for the SMS message
    args = parser.parse_args()  # Parse the command-line arguments
    transformed_sms = transform_text(args.sms)  # Preprocess the input SMS
    vector_input = tfidf.transform([transformed_sms])  # Transform the preprocessed text using the vectorizer
    result = model.predict(vector_input)[0]  # Predict the class (spam or not spam)
    print('spam' if result == 1 else 'not spam')  # Print the result

if __name__ == '__main__':
    main()  # Call the main function if the script is run directly
