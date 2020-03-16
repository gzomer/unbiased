import nltk
import bcolz
import pickle
import numpy as np
from nltk.corpus import stopwords

_STOP_WORDS = set(stopwords.words('english'))
_GLOVE = None
_GLOVE_PATH = '../data/glove-embeddings'
_NUM_FEATURES = 50

def clean_tokens(tokens):
    return [w for w in tokens if w not in _STOP_WORDS]

def sentence_embedding(sentence):

	model = get_glove_model()
	feature_vec = np.zeros((_NUM_FEATURES,), dtype="float32")
	nwords = 0

	tokens = nltk.word_tokenize(sentence.lower())
	tokens = clean_tokens(tokens)

	for token in tokens:
	    if token in model:
	        nwords = nwords+1
	        feature_vec = np.add(feature_vec, model[token])

	if nwords > 0:
	    feature_vec = np.divide(feature_vec, nwords)
	return feature_vec

def generate_glove_model():	
	words = []
	idx = 0
	word2idx = {}
	vectors = bcolz.carray(np.zeros(1), rootdir=f'{_GLOVE_PATH}/6B.50.dat', mode='w')

	with open(f'{_GLOVE_PATH}/glove.6B.50d.txt', 'rb') as f:
	    for l in f:
	        line = l.decode().split()
	        word = line[0]
	        words.append(word)
	        word2idx[word] = idx
	        idx += 1
	        vect = np.array(line[1:]).astype(np.float)
	        vectors.append(vect)
	vectors = bcolz.carray(vectors[1:].reshape((400001, _NUM_FEATURES)), rootdir=f'{_GLOVE_PATH}/6B.50.dat', mode='w')
	vectors.flush()
	pickle.dump(words, open(f'{_GLOVE_PATH}/6B.50_words.pkl', 'wb'))
	pickle.dump(word2idx, open(f'{_GLOVE_PATH}/6B.50_idx.pkl', 'wb'))
	    
def get_glove_model():
	global _GLOVE

	if _GLOVE:
		return _GLOVE
	vectors = bcolz.open(f'{_GLOVE_PATH}/6B.50.dat')[:]
	words = pickle.load(open(f'{_GLOVE_PATH}/6B.50_words.pkl', 'rb'))
	word2idx = pickle.load(open(f'{_GLOVE_PATH}/6B.50_idx.pkl', 'rb'))

	_GLOVE = {w: vectors[word2idx[w]] for w in words}

	return _GLOVE   