import bcolz
import pickle
import numpy as np
from services.embeddings import sentence_embedding
from sklearn.metrics.pairwise import cosine_similarity

# Remove
from os import listdir
import json

_CACHE_EMBEDDINGS = None;
_NEWS_CACHE = None
_NEWS_DIR = '../data/news/'

def get_suggestions(headline, stance):
	
	embedding = sentence_embedding(headline)

	news_embeddings = get_news_embeddings()

	opposite_view = 'left' if stance == 'right' else 'left'

	central_view_scores = find_most_similar_by_stance(embedding, news_embeddings, 'central')
	opposite_view_scores = find_most_similar_by_stance(embedding, news_embeddings, opposite_view )

	if central_view_scores is None or len(central_view_scores) == 0:
		return []

	if opposite_view_scores is None or len(opposite_view_scores) == 0:
		return []

	central_view_score = central_view_scores[0]
	opposite_view_score = opposite_view_scores[0]

	similar_ids = [central_view_score[0], opposite_view_score[0]]
	
	scores = {
		central_view_score[0] : central_view_score[1],
		opposite_view_score[0] : opposite_view_score[1]
	}

	similar_news = get_news_from_ids(similar_ids)

	for news in similar_news:
		news['similarity'] = scores[news['id']]

	return {
		'headline' : headline,
		'suggestions' : similar_news
	}

def find_most_similar_by_stance(sentence_vector, posts, stance):
	posts_with_stance = [post for post in posts if post[2] == stance]

	return find_most_similar(sentence_vector, posts_with_stance)

def find_most_similar(sentence_vector, posts, amount = 1):
    comparison = [[post[0], cosine_similarity(sentence_vector.reshape(1,-1), post[1].reshape(1,-1))] for post in posts]
    comparison.sort(key=lambda x:x[1],reverse=True)
    
    return [ [similar[0], float(similar[1][0][0])] for similar in comparison[0:amount]]

def get_news_embeddings():
	global _CACHE_EMBEDDINGS
	if _CACHE_EMBEDDINGS:
		return _CACHE_EMBEDDINGS

	_CACHE_EMBEDDINGS = build_embeddings_cache()
	return _CACHE_EMBEDDINGS

def build_embeddings_cache():
	news = get_all_news()
	
	return [[new['id'], sentence_embedding(new['title']), new['stance']] for new in news]

def get_news_from_ids(ids):
	return [_NEWS_CACHE[id] for id in ids]

# TODO - Read news from database
def get_all_news():
	global _NEWS_CACHE	

	with open(_NEWS_DIR + 'posts.json') as f:
		posts = f.read()
		f.close()

	posts_json = json.loads(posts)

	_NEWS_CACHE = {post['id']: post  for post in posts_json}
	return posts_json








