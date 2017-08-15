import json, os, gzip, sys

class DataFormatter:
	
	'''Format solr grabbed data out of JSON-format '''
	
	def __init__(self, input_folder, format, words, window_size):
		self.input_folder = input_folder
		self.format = format
		self.words = words
		self.window_size = window_size
		
	def format_data(self):
		files = os.listdir(self.input_folder)
		for filei, filen in enumerate(files):
			with gzip.open(self.input_folder + "/" + filen, "rt") as data_file:
				data = json.loads(data_file.read())
				if self.format == "thread_text":
					self.format_thread_text(data)
				elif self.format == "comment_text":
					self.format_comment_text(data)
				elif self.format == "comment_text_window":
					self.format_comment_text_window(data)
			
	def format_comment_text(self, data, output_file):
		for comment_id, comment in data.items():
			if self.comment_is_okay(comment):
				text = comment["text"]
				output_file.write(text + "\n")
			
		
	def format_thread_text(self, data, output_file):
		for thread_id, thread in data.items():
			text = self.thread_to_text(thread)
			if len(text) == 0:
				continue
			output_file_file.write(text + "\n")
			
	def format_comment_text_window(self, data):
		for comment_id, comment in data.items():
			if self.comment_is_okay(comment):
				id = str(comment["id"])
				lemma = comment["lemma"]
				text = comment["text"]
				token_ids = self.find_matching_token(lemma)
				token_id = token_ids[0] ## Just using first found token for now....
				start_pos, end_pos = self.find_text_match_pos(text, token_id)
				if start_pos < self.window_size/2:
					ll = 0
					rr = end_pos + (self.window_size-start_pos)
				else:
					ll = start_pos - int(self.window_size/2)
					rr = end_pos + int(self.window_size/2)
				lr = start_pos
				rl = end_pos
				sys.stdout.write(id + "\t" + text[ll:lr] + text[rl:rr] + "\n")
				
	def find_text_match_pos(self, text, token_id):
		matching_word = text.split(" ")[token_id]
		start_pos = text.index(matching_word)
		end_pos = start_pos + len(matching_word)
		return start_pos, end_pos
			
				
	
	def find_matching_token(self, lemma):
		matches = []
		for word_i, word in enumerate(lemma.split(" ")):
			if word in self.words:
				matches.append(word_i)
		
		return matches
					
	def thread_to_text(self, thread):
		text = []
		for comment in thread["docs"]:
			if self.comment_is_okay(comment):
				text.append(comment["lemma"])
		return " ".join(text)
	
	def comment_is_okay(self, comment):
		if "lemma" not in comment or "This message has been removed by ." in comment["text"]:
			return False
		else:
			return True
		
''' formats:
			comment_text_window - extract only the window around the matching word '''

	
if __name__ == "__main__":
	input_folder = "comments"
	words = ["köyhä", "rutiköyhä", "ruti#köyhä", "rahaton", "persaukinen", "pers#aukinen", "vähävarainen", "vähä#varainen", "perseaukinen", "perse#aukinen", "tyhjätasku", "tyhjä#tasku", "pienituloinen", "pieni#tuloinen",  "sossupummi", "sossu#pummi", "saita", "sosiaalipummi", "sosiaali#pummi", "varaton", "eläkeläinen", "pienipalkkainen", "pieni#palkkainen"]
	formatter = DataFormatter(input_folder=input_folder, format="comment_text_window", words=words, window_size=220)
	formatter.format_data()
	
