# To import models from parent project
import sys
sys.path.insert(0, '..')

from models.text_classifier_model import TextClassifierModel

_POLITICAL_CLASSIFIER = None
_STANCE_CLASSIFIER = None
_POLITICAL_CLASSIFIER_NAME = 'political_classifier'
_STANCE_CLASSIFIER_NAME = 'political_stance_classifier'

def is_political(headline):
	return get_political_classifier().predict(headline) == 'political'
	
def get_stance(headline):
	return get_stance_classifier().predict(headline)

def is_biased(stance):
	return stance != 'central'

def get_political_classifier():
	global _POLITICAL_CLASSIFIER

	if _POLITICAL_CLASSIFIER:
		return _POLITICAL_CLASSIFIER

	model = TextClassifierModel()
	model.load(f'./models/{_POLITICAL_CLASSIFIER_NAME}.pth',f'./models/{_POLITICAL_CLASSIFIER_NAME}.cfg',f'./models/{_POLITICAL_CLASSIFIER_NAME}.vocab')

	_POLITICAL_CLASSIFIER = model
	return _POLITICAL_CLASSIFIER

def get_stance_classifier():
	global _STANCE_CLASSIFIER

	if _STANCE_CLASSIFIER:
		return _STANCE_CLASSIFIER

	model = TextClassifierModel()
	model.load(f'./models/{_STANCE_CLASSIFIER_NAME}.pth',f'./models/{_STANCE_CLASSIFIER_NAME}.cfg', f'./models/{_STANCE_CLASSIFIER_NAME}.vocab')

	_STANCE_CLASSIFIER = model
	return _STANCE_CLASSIFIER