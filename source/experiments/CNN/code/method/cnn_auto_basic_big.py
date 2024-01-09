from tensorflow.keras.models import Model
from tensorflow.keras.layers import Embedding, Conv1D, Dense, Input, Conv1DTranspose


class CNN_Auto_Basic_Big:
    def __init__(self, tokenizer_en, tokenizer_fr, max_len, max_vocab_fr_len):
        self.tokenizer_en = tokenizer_en
        self.tokenizer_fr = tokenizer_fr
        self.max_len = max_len
        self.max_vocab_fr_len = max_vocab_fr_len

    def build_model(self):
        # Encoder
        encoder_inputs = Input(shape=(None,))
        enc_emb_layer = Embedding(input_dim=len(self.tokenizer_en.word_index) + 1, output_dim=32)
        enc_emb = enc_emb_layer(encoder_inputs)

        encoder_cnn1 = Conv1D(1024, kernel_size=5, padding='same', activation='relu')(enc_emb)
        encoder_cnn2 = Conv1D(512, kernel_size=5, padding='same', activation='relu')(encoder_cnn1)
        encoder_cnn3 = Conv1D(256, kernel_size=5, padding='same', activation='relu')(encoder_cnn2)
        encoder_cnn4 = Conv1D(128, kernel_size=3, padding='same', activation='relu')(encoder_cnn3)
        encoder_cnn5 = Conv1D(64, kernel_size=3, padding='same', activation='relu')(encoder_cnn4)
        encoder_cnn6 = Conv1D(32, kernel_size=3, padding='same', activation='relu')(encoder_cnn5)
        encoder_cnn7 = Conv1D(16, kernel_size=3, padding='same', activation='relu')(encoder_cnn6)

        # Decoder
        decoder_inputs = Input(shape=(None,))
        dec_emb_layer = Embedding(input_dim=len(self.tokenizer_fr.word_index) + 1, output_dim=32)
        dec_emb = dec_emb_layer(decoder_inputs)
        decoder_cnn1 = Conv1DTranspose(512, kernel_size=5, padding='same', activation='relu')(dec_emb)
        decoder_cnn2 = Conv1DTranspose(256, kernel_size=5, padding='same', activation='relu')(decoder_cnn1)
        decoder_cnn3 = Conv1DTranspose(128, kernel_size=5, padding='same', activation='relu')(decoder_cnn2)
        decoder_cnn4 = Conv1DTranspose(64, kernel_size=3, padding='same', activation='relu')(decoder_cnn3)
        decoder_cnn5 = Conv1DTranspose(32, kernel_size=3, padding='same', activation='relu')(decoder_cnn4)
        decoder_cnn6 = Conv1DTranspose(16, kernel_size=3, padding='same', activation='relu')(decoder_cnn5)
        decoder_cnn6 = Conv1D(64, kernel_size=3, padding='same', activation='relu')(decoder_cnn6)
        decoder_dense = Dense(self.max_vocab_fr_len + 1, activation='relu')
        decoder_outputs = decoder_dense(decoder_cnn6)

        # Model
        model = Model([encoder_inputs, decoder_inputs], decoder_outputs)

        # Compile the model
        model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
        return model