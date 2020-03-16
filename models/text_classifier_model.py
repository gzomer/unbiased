import torch
import re
from torchtext.data.utils import ngrams_iterator
from torchtext.data.utils import get_tokenizer
from models.multi_label_text_classifier import MultiLabelTextClassifier
import pickle

class TextClassifierModel():

	def load(self, model_path, config_path, vocab_path):
		config = self._load_pickle(config_path)

		self.vocab = self._load_pickle(vocab_path)
		self.vocab_size = len(self.vocab)
		self.labels = config['labels'] 
		self.ngrams = config['ngrams']
		self.embeddings_dim = config['embeddings_dim']
		self.num_classes = len(self.labels)

		self.model = self._load_model(model_path)	

	def _load_pickle(self, path):
		print (path)
		with open(path,'rb') as f:
			data = pickle.load(f)
			f.close()
			return data


	def _load_model(self, model_path):	
		model = MultiLabelTextClassifier(self.vocab_size, self.embeddings_dim, self.num_classes)
		model.load_state_dict(torch.load(model_path))
		model.eval()

		return model

	def predict(self, text):
		tokenizer = get_tokenizer("basic_english")
		with torch.no_grad():
			text = torch.tensor([self.vocab[token]
								for token in ngrams_iterator(tokenizer(text), self.ngrams)])
			output = self.model(text, torch.tensor([0]))
			result = output.argmax(1).item()
			label = self.labels[result+1]
			return label
