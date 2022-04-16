import keras
from numpy import result_type
import preprocessing
import pickle
import sklearn



model = keras.models.load_model('my_model')

with open('encoder.pickle', 'rb') as handle:
	encoder = pickle.load(handle)

def predict(news):
	news = preprocessing.remove_noise(news)
	news = preprocessing.remove_stopwords(news)
	news = preprocessing.truncate(news)
	news = preprocessing.tokenize(news)
	result = model.predict(news)

	if(result[0][0]>=0.5):
		probability = result[0][0]
		result[0][0] = 1
	else:
		probability = 1 - result[0][0]
		result[0][0] = 0

	probability *= 100
	result_ = encoder.inverse_transform(result.astype(int).flatten())
	return(result_[0],probability)


