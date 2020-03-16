from services.classifier import is_political
from services.classifier import is_biased
from services.classifier import get_stance
from services.suggestions import get_suggestions

def suggest(headline):

	if not is_political(headline):
		return {}

	stance = get_stance(headline)

	if stance is None:
		return {}
	
	if not is_biased(stance):
		return {}

	suggestions = get_suggestions(headline, stance);

	return suggestions