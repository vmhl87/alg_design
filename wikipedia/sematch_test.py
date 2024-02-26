from sematch.semantic.similarity import WordNetSimilarity
wns = WordNetSimilarity()

def similarity(a, b):
	return wns.word_similarity(a, b, 'li')
