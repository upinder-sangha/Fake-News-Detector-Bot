import re
import nltk
import tensorflow as tf
nltk.download('stopwords')
from nltk.corpus import stopwords
from keras.preprocessing.sequence import pad_sequences
import pickle


def remove_noise(input):
   input = str(input).lower()
   new_text = re.sub('[^a-z+]', ' ', input)
   return new_text



stopwords_list = stopwords.words('english')
stopwords_list.append(['the', 'a', 'an'])
def remove_stopwords(input_text):
    # input_text = str(input_text).lower()
   words = str(input_text).split()
   clean_words = [word for word in words if (
   	word not in stopwords_list) and len(word) > 1]
   return " ".join(clean_words)



max_length = 20
def truncate(input_text):
	words = str(input_text).split() 
	if len(words)>max_length:
		del words[max_length:]
	elif len(words)<max_length:
		words = words + ['nan'] * (max_length-len(words)) 
	return " ".join(words)



def tokenize(test_news):
	test_news = [test_news]

	with open('tokenizer.pickle', 'rb') as handle:
		tokenizer = pickle.load(handle)

	test_news_ = pad_sequences(tokenizer.texts_to_sequences(test_news), maxlen=max_length)
	return test_news_
