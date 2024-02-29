import tensorflow as tf
import tensorflow_hub as hub

tfhub_handle_preprocess = "https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3"
tfhub_handle_encoder = "https://tfhub.dev/tensorflow/bert_en_uncased_L-12_H-768_A-12/3"


class BertModel:
    def __init__(self, text: list[str]):
        self.t = (text,)
        self.bert_model = hub.KerasLayer(tfhub_handle_encoder)
        self._build_classifier_model()

    @staticmethod
    def _build_classifier_model():
        # Load options for the BERT model
        load_options = tf.saved_model.LoadOptions(
            experimental_io_device="/job:localhost"
        )
        # Creates an input layer for your model where you'll feed in your text data
        text_input = tf.keras.layers.Input(shape=(), dtype=tf.string, name="text")
        # Creates a preprocessing layer using a model from TensorFlow Hub
        preprocessing_layer = hub.KerasLayer(
            tfhub_handle_preprocess, name="preprocessing", options=load_options
        )
        # Applies the preprocessing model to your input
        encoder_inputs = preprocessing_layer(text_input)
        # Creates a BERT encoder layer, also using a model from TensorFlow Hub
        encoder = hub.KerasLayer(
            tfhub_handle_encoder,
            trainable=True,
            name="BERT_encoder",
            options=load_options,
        )
        # Applies the BERT encoder to your preprocessed input
        outputs = encoder(encoder_inputs)
        # Gets the pooled output of the BERT encoder, which is a fixed-length summary of the input
        net = outputs["pooled_output"]
        # Applies dropout for regularization
        net = tf.keras.layers.Dropout(0.1)(net)
        # Creates a dense output layer for classification
        net = tf.keras.layers.Dense(1, activation=None, name="classifier")(net)
        # Constructs a Keras Model instance
        return tf.keras.Model(text_input, net)

    @property
    def bert_raw_result(self):
        bert_results = self.bert_model(self.t)
        return bert_results

    @property
    def preprocessing_m_output(self):
        return tf.sigmoid(self.bert_raw_result).numpy()

    def predict(self):
        """
        Predicts the class of a text.

        :return: The predicted class of the text.
        """
        return self.m.predict(self.t)
