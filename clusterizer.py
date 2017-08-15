import sys, json, gzip, os, pickle
import numpy as np
from operator import itemgetter
from sklearn.cluster import MiniBatchKMeans
import logging
logging.basicConfig(level=logging.INFO)

def read_vectors(where):
	vectors = []
	with gzip.open(where, "rt") as gzf:
		for line in gzf:
			vect = [float(val) for val in line.strip().split(" ")]
			vectors.append(vect)
	return vectors

def read_data(where):
	texts = []
	with gzip.open(where, "rt") as gzf:
		for line in gzf:
			texts.append(line.strip())
	return texts

def clusterize_data(vectors, texts, n_clusters, where):
	logging.info("Fitting clusterizer...")
	clusterizer = MiniBatchKMeans(n_clusters=n_clusters, batch_size=1000, random_state=0)
	clusterizer.fit(vectors)
	dist = clusterizer.transform(vectors)
	clusters = clusterizer.predict(vectors)
	logging.info("Extracting clusters...")
	extract_top_texts(dist, clusters, texts, 100000000000000, n_clusters, where)
	logging.info("Extracting cluster centers...")
	extract_cluster_centers(clusterizer, where)

	
def extract_cluster_centers(clusterizer, where):
	centers = clusterizer.cluster_centers_.tolist()
	with gzip.open(where + "/centers.gz", "wt") as gzip_file:
		gzip_file.write(json.dumps(centers))
		
def extract_top_texts(dist, cluster_labels, texts, k_texts, n_clusters, where):
	clusters = {}
	for i in range(0, len(texts)): ## i = sample
		label = cluster_labels[i]
		distances = dist[i]
		text = texts[i]
		clusters[label] = clusters.get(label, [])
		clusters[label].append([text, min(distances)])
	# sort clusters
	for key, value in clusters.items():
		clusters[key] = sorted(value, key=itemgetter(1))
	save_clusters(clusters, where)
	
def save_clusters(clusters, where):
	cl = 0
	if not os.path.exists(where):
		os.makedirs(where)
	for key, value in clusters.items():
		with gzip.open("{}/cluster_{}.gz".format(where, cl), "wt") as gzf:
			for text, val in value:
				gzf.write(text + "\t" + str(val) + "\n")
		cl += 1

#def save_cluster(text, i, where):
#	with gzip.open("{}/cluster_{}.gz".format(where, i), "wt") as gzf:
#		for txt in text:
#			gzf.write(txt + "\n")
			
''' Read vectors, texts, clusterize
	Vectors file = one vector per line, values are seperated by a whitespace
	Texts file = one text per line
	Matching vector and text must have the same index in their files
	'''
			
if __name__ == "__main__":

	
	logging.info("Loading comments...")
	vectors = read_vectors("comments_window_v.gz")
	logging.info("Loading texts...")
	texts = read_data("comments_text_window.gz")
	#texts = []
	logging.fino("Clusterizing...")
	clusterize_data(vectorsvectors, texts=texts, n_clusters=100, where="clusters_comments_all_small")
	
