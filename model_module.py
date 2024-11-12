import os
import pathlib
import librosa
from IPython import display
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tensorflow as tf
import tensorflow_hub as hub
import tensorflow_io as tfio


@tf.function
def load_wav_16k_mono(filename):
    # Convert filename to string if it's a WindowsPath object
    if isinstance(filename, pathlib.WindowsPath):
        filename = str(filename)

    file_contents = tf.io.read_file(filename)
    wav, sample_rate = tf.audio.decode_wav(
          file_contents,
          desired_channels=1)
    wav = tf.squeeze(wav, axis=-1)
    sample_rate = tf.cast(sample_rate, dtype=tf.int64)
    wav = tfio.audio.resample(wav, rate_in=sample_rate, rate_out=16000)
    return wav


def get_mym_model( audio_file ):
   #list of labal
   my_classes = ['avion', 'applaudissement', 'claxon', 'tam_tam', 'moteur', 'helicoptere', 'rire', 'sirenne', 'tonnerre', 'mouton', 'vache', 'chat', 'chien', 'music', 'cri_bebe', 'coq', 'feu_artifice', 'arme_a_feu', 'oiseau', 'voix_humaine']
   # Load yamnet model
   yamnet_model = hub.load('https://tfhub.dev/google/yamnet/1')
   #yamnet_model = tf.saved_model.load('yamnet-tensorflow2-yamnet-v1')
   # Load the model
   loaded_model = tf.keras.models.load_model('mym_save_model.h5')

#    wav_file_name = pathlib.Path( audio_file )
   converted_wav_file = load_wav_16k_mono( audio_file )
   scores, embeddings, spectrogram = yamnet_model( converted_wav_file )
   result = loaded_model(embeddings).numpy()
   inferred_class = my_classes[result.mean(axis=0).argmax()]
   return  inferred_class


# ***************************************************************************************************************************

#get_mym_model("sandaga.wav")