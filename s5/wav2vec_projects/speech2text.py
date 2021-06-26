# speec2text
# Source: https://github.com/sdhilip200/speech-to-text/blob/main/speech.ipynb
#         https://www.kdnuggets.com/2021/03/speech-text-wav2vec.html

# Import necessary libraries

# For managing audio file
print("====== Importing libraries ======")
import librosa
#Importing Pytorch
import torch
#Importing Wav2Vec tokenizer
from transformers import Wav2Vec2ForCTC, Wav2Vec2Tokenizer

# Importing Wav2Vec pretrained model
# Model is wav2vec 2.0
# Use tokenizer for decoding
print("====== Importing wav2vec 2.0 pretrained model ======")
tokenizer = Wav2Vec2Tokenizer.from_pretrained("facebook/wav2vec2-base-960h")
model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base-960h")

# Loading the audio file and ensure 16kHz sampling
print("====== Loading audio file ======")
audio, rate = librosa.load("example-audio/OREGON_ks50i030_archrival.wav", sr = 16000)

# Taking an input value. Pass the audio (array) into tokensizer
# Get tensors into PyTorch format instead of Python integers using
# return_tensors = "pt"
input_values = tokenizer(audio, return_tensors = "pt").input_values

print("====== Recognising Speech... ======")
# Storing logits (non-normalized prediction values)
logits = model(input_values).logits

# Storing predicted id's
prediction = torch.argmax(logits, dim = -1)

# Passing the prediction to the tokenizer decode to get the transcription
print("====== Transcription ======")
transcription = tokenizer.batch_decode(prediction)[0]
print(transcription)
