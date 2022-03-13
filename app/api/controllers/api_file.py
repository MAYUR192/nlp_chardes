from flask import Flask, request
import numpy as np
import os
from app import app, loggers
from ..models.word_model import word_train, get_candidate_words, get_correct_word
from ...lib.utils import ResponseUtil



@app.route('/status')
def index():
	return ResponseUtil(True, 200).json_message_response('Its working!')

@app.route('/train', methods=['POST'])
def train_model():
	try:
		json_data = request.get_json(force=True)
		text_list = json_data['text_list']
		word_train(text_list)
		return ResponseUtil(True, 200).json_message_response("Model Trained on Given Data")
	except Exception as e:
		loggers["error"].error("Exception occurred while model training:{}".format(e))
		return ResponseUtil(False, 403).json_message_response("Exception Occured:{}".format(e))


@app.route('/predict', methods=['GET'])
def predict_model():
	try:
		defination = request.args.get("defination")
		masked_word = request.args.get("maskedWord")
		candidates_words = get_candidate_words(defination, masked_word, )
		corrected_word = get_correct_word(masked_word, candidates_words)
		return ResponseUtil(True, 200).json_data_response(corrected_word)
	except Exception as e:
		loggers["error"].error("Exception occurred while predicting:{}".format(e))
		return ResponseUtil(False, 403).json_message_response("Exception Occured:{}".format(e))