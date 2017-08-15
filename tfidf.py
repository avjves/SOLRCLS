from sklearn.feature_extraction.text import TfidfVectorizer
import os,gzip,json,argparse, numpy
from natsort import natsorted

class TfidfCalc:
	
	def __init__(self, cluster_folder):
		self.cluster_folder = cluster_folder
		self.vectorizer = TfidfVectorizer(max_df=0.7, sublinear_tf=True, ngram_range=(1,1), analyzer="word")
		self.top_k_words = 50
		self.lines_to_read = 50
		
	def run(self):
		print("Loading data..")
		data = self.load_clusters(wordperline=False)
		print("Extracting words..")
		self.extract_words(data)
		
	def extract_words(self, data):
		self.vectorizer.fit(data)
		vectors = self.vectorizer.transform(data)
		vocabulary = self.vectorizer.get_feature_names()
		for vector_i, vector in enumerate(vectors):
			print("Cluster: {}".format(vector_i))
			dense = vector.toarray()[0]
			sorted_indexes = numpy.argsort(dense)[::-1][:self.top_k_words]
			for index in sorted_indexes:
				print("Feature value: {}\t Feature name: {}".format(dense[index], vocabulary[index]))
				
			
		
	def load_clusters(self, wordperline):
		files = natsorted(os.listdir(self.cluster_folder))
		clusters = []
		for filename in files:
			if "center" in filename:
				continue
				data = []
				with gzip.open(self.cluster_folder + "/" + filename, "rt") as gzip_file:
					for line_i, line in enumerate(gzip_file):
						if not line:
							continue
						if wordperline:
							data.append(line.strip())
						else:
							if line_i >= self.lines_to_read:
								break
							b = line.split("\t")[1]
							texts.append(b)
				clusters.append(" ".join(data))
		return clusters


if __name__ == "__main__":
	
	parser = argparse.ArgumentParser(description="Tfidf for clusters")
	parser.add_argument("--cluster_folder", required=True)
	args = parser.parse_args()
	
	tfidf = TfidfCalc(args.cluster_folder)
	tfidf.run()
	
	
