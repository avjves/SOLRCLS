import sys, json, gzip
import lwvlib
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def check_nearest_words(vector, vector_i, wv):
	wv_vectors = wv.vectors
	wv_words = wv.words
	sims = cosine_similarity(np.array(vector).reshape(1, -1), wv_vectors)[0]
	indexes = np.argsort(sims)[::-1]
	for index in indexes[:10]:
		print(wv_words[index])
		
	print()
	
		
	#print(vector)
	#print(wv.nearest(vector))

if __name__ == "__main__":
	wv=lwvlib.load("/home/ginter/w2v/pb34_wf_200_v2.bin",max_rank=400000)

	for line in sys.stdin:
		vectors = json.loads(line)
		for vector_i, vector in enumerate(vectors):
			check_nearest_words(vector, vector_i, wv)