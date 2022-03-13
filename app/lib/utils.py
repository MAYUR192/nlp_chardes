from flask import Response
import json
import re
import os

path = os.path.dirname(os.path.abspath(__file__))


model_path= os.path.join(path.replace("/lib",""), "ml-models")

with open(os.path.join(model_path,'contraction.json'),'r') as f:
	CONTRACTIONS = json.load(f)

with open('model_path/word_id.pkl', 'rb') as f:
    word2id = pickle.load(f)

with open('model_path/id_word.pkl', 'rb') as f:
    id2word = pickle.load(f)

model = load_model('cbow_model.h5')


class ResponseUtil:
	status = ""

	def __init__(self, status, code):
		self.status = status
		self.code = code

	def json_message_response(self, message):
		return Response(json.dumps({
			"status": self.status,
			"code": self.code,
			"message": message
		}), mimetype="application/json")

	def json_data_response(self, data):
		return Response(json.dumps({
			"status": self.status,
			"code": self.code,
			"data": data
		}), mimetype="application/json")



class PreProcess:

	def replace_contraction(self, text):
		sample = [CONTRACTIONS[word.strip()] if word.strip() in CONTRACTIONS else word.strip() for word in text.split()]
		return " ".join(sample)

	def pre_process(self, text):
		text = text.lower()
		text = re.sub("\s\\'","\'",text)
		text = re.sub(r"´|’",r"'",text)
		text = re.sub('[^a-zA-Z0-9\\s\\%&$\'\:]', ' ', text)
		text = re.sub(' +', ' ',text)
		text = text.strip()
		text = self.replace_contraction(text)
		return text