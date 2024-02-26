from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("all-MiniLM-L12-v2")

query_embedding = model.encode("Population of the USA")
passsage_embedding = model.encode([
	"North American Cities",
	"American Military",
	"London census",
	"USA census 2023"
])

print("Similarity:", util.dot_score(query_embedding, passage_emedding))
