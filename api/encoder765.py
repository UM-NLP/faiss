from tensorflow.keras.losses import CategoricalCrossentropy, BinaryCrossentropy
from tensorflow.keras.metrics import BinaryAccuracy
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
import tensorflow_text
#tf.compat.v1.disable_eager_execution()
if tf.config.list_physical_devices('GPU'):
    strategy = tf.distribute.MirroredStrategy()
else:  # Use the Default Strategy
    strategy = tf.distribute.get_strategy()
tf.keras.backend.clear_session()
tf.compat.v1.reset_default_graph()
def tf_hub_model_generation():
    with strategy.scope():
        text_input = tf.keras.layers.Input(shape=(), dtype=tf.string, name='text')
        preprocessing_layer = hub.KerasLayer("/Users/mohammadsaloot/IdeaProjects/persona/machine_learning/unsafe/search_operations/vector_encoding/bert_en_uncased_preprocess_3", name='preprocessing', trainable=False)
        bert_layer = hub.KerasLayer("/Users/mohammadsaloot/IdeaProjects/persona/machine_learning/unsafe/search_operations/vector_encoding/universal-sentence-encoder-cmlm_multilingual-base_1", name='bert', trainable=False)
        encoder_in = preprocessing_layer(text_input, 0)
        encoder_out = bert_layer(encoder_in)
        model= tf.keras.Model(text_input, encoder_out)
        opt = tf.keras.optimizers.Adam(learning_rate=0.001)
        model.compile(
            optimizer = opt,
            loss = BinaryCrossentropy(from_logits=False),
            metrics = [BinaryAccuracy('accuracy')])
        result=model.save('encoder.bin')
        return model
def model_loading(path):
    model= tf.keras.models.load_model(path)
    return model

def predict_single(text, model):
    matrix= model.predict([text],verbose = 0)['sequence_output']
    result=matrix.mean(axis=1)
    return (result)

def predict_serial(text, model):
    matrix=[]
    for row in text:
        row_encode= model.predict([row],verbose = 0)['sequence_output'][0]
        matrix.append( row_encode)
    matrix=np.array(matrix)
    result=matrix.mean(axis=1)
    return (result)
def predict_batch(text, model):
    matrix= model.predict(text,verbose = 0)['sequence_output']
    result=matrix.mean(axis=1)
    return (result)

