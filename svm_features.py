import sys, os, gzip, json
import numpy as np
from natsort import natsorted
from operator import itemgetter
from sklearn.svm import LinearSVC
from sklearn.feature_extraction.text import TfidfVectorizer

class FeatureExtractor:
	
	def __init__(self, top_words, C=10000):
		self.clsf = LinearSVC(C=C, penalty="l1", dual=False, class_weight="balanced")
		self.top_words = top_words
		self.vectorizer = TfidfVectorizer(ngram_range=(4,4),analyzer="char", sublinear_tf=True, max_df=0.7)

	def read_clusters(self, where):
		self.clusters = {}
		files = natsorted(os.listdir(where))
		for filei, filen in enumerate(files):
			comments = []
			with gzip.open(where + "/" + filen, "rt") as gzip_f:
				for line in gzip_f:
					if not line: continue
					text = line.split("\t")[1]
					comments.append(text)
			self.clusters[filei] = " ".join(comments)
			
	def extract_top_words(self):
		#X = [k for i in range(0, len(self.clusters)) for k in self.clusters[i]] # :c
		X = [self.clusters[i] for i in range(0, len(self.clusters))]
		self.vectorizer.fit(X)
		for i in range(0, len(self.clusters)):
			true = [self.clusters[i]]
			false = [self.clusters[j] for j in range(0, len(self.clusters)) if j != i]
			#X = true + [val for cluster in false for val in cluster] 
			X = true + [val for val in false]
			y = [1 for i in range(0,len(true))] + [0 for i in range(0, len(X)-len(true))]
			self.clsf.fit(self.vectorizer.transform(X), y)
			pos_words, neg_words = self.get_words()
			self.print_words(pos_words, "positive", i)
			self.print_words(neg_words, "negative", i)
			
	
	def get_words(self):
		features = self.vectorizer.get_feature_names()
		coef = self.clsf.coef_[0]
		nz = np.nonzero(coef)
		feats = []
		for index in nz[0]:
			value = coef[index]
			feature = features[index]
			feats.append([feature, value])
		feats.sort(key=itemgetter(1), reverse=True)
		pos_words, neg_words = feats[:self.top_words], feats[len(feats)-self.top_words:][::-1]
		return pos_words, neg_words
			
	def print_words(self, words, title, cluster_index):
		print("For cluster {} the top {} {} words are:".format(cluster_index, self.top_words, title))
		for word in words:
			print(word)

if __name__ == "__main__":
	
	extractor = FeatureExtractor(top_words=20)
	extractor.read_clusters(sys.argv[1])
	extractor.extract_top_words()