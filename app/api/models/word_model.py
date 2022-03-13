from keras.preprocessing import text
from keras.utils import np_utils
from keras.preprocessing import sequence
import keras.backend as K
from keras.models import Sequential
from keras.layers import Dense, Embedding, Lambda
from keras.models import load_model
from ...lib.utils import word2id, id2word, model, model_path, PreProcess
import numpy as np
import distance
import pickle

pre_process = PreProcess()

def generate_context_word_pairs(wids, vocab_size):
    context_data = []
    label_data = []
    for data in wids:
        context_data.append(data[1:])
        label_data.append(data[0])
    x = sequence.pad_sequences(context_data, maxlen=15)
    y = np_utils.to_categorical(label_data, vocab_size)
    return x, y


def word_train(text_data):
    """
    Input : text_data :- List of Setences
    """
    try:
        text_data = [pre_process(sent) for sent in text_data]
        tokenizer = text.Tokenizer()
        tokenizer.fit_on_texts(text_data)
        word2id = tokenizer.word_index
        word2id['PAD'] = 0
        id2word = {v:k for k, v in word2id.items()}
        wids = [[word2id[w] for w in text.text_to_word_sequence(doc)] for doc in text_data]
        vocab_size = len(word2id)
        embed_size = 100
        
        context_data, label_data = generate_context_word_pairs(wids, vocab_size)
    
        cbow = Sequential()
        cbow.add(Embedding(input_dim=vocab_size, output_dim=embed_size, input_length=15))
        cbow.add(Lambda(lambda x: K.mean(x, axis=1), output_shape=(embed_size,)))
        cbow.add(Dense(vocab_size, activation='softmax'))
        cbow.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    
        cbow.fit(context_data, label_data, epochs=30, batch_size=10, verbose=2)
        with open('model_path/word_id.pkl', 'wb') as f:
            pickle.dump(word2id, f)
        with open('model_path/id_word.pkl', 'wb') as f:
            pickle.dump(id2word, f)
        cbow.save("model_path/cbow_model.h5")
        return True
    except Exception as e:
        raise Exception(e) 


def get_candidate_words(doc, masked_word):
    """
    Input text:- Defination of word
          masked_word:- masked character word
    output word:- generate list of candidate words based on Model and words 
                  are same length as of Masked character word
    """
    candidate_words = []
    wids = [word2id[w] for w in text.text_to_word_sequence(doc)]
    d = sequence.pad_sequences([wids], maxlen=15)
    predictied_prob = model.predict(d)
    id_index = np.argsort(predictied_prob[0])[::-1][0:10]
    for ids in id_index:
        word = id2word[ids]
        if len(word) == len(masked_word):
            candidate_words.append(word)
    return candidate_words

def get_correct_word(masked_word, candidate_words):
    """
    Input masked_word:- maksed character word
          candidate_words :- list of canddate word
    output:- Corrected word based on Hamming distance
    """
    distances = []
    for word in candidate_words:
        distances.append(distance.hamming(masked_word, word))
    return candidate_words[distances.index(min(distances))]

