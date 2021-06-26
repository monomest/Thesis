# Preliminary experiments
# Based on this: https://github.com/pytorch/fairseq/blob/master/examples/wav2vec/README.md
import soundfile as sf
import torch
# For managing audio files
import librosa
# For getting datasets
from datasets import load_dataset
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor

# load pretrained model
processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-base-960h")
model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base-960h")


librispeech_samples_ds = load_dataset("patrickvonplaten/librispeech_asr_dummy", "clean", split="validation")

# load audio
print("====== Loading audio file ======")
audio_input, sample_rate = librosa.load("example-audio/OREGON_ks50i030_archrival.wav", sr = 16000)
#audio_input, sample_rate = sf.read(librispeech_samples_ds[0]["file"])


# Taking an input value. Pass the audio (array) into tokensizer
# Get tensors into PyTorch format instead of Python integers using
# return_tensors = "pt"
input_values = processor(audio_input, sampling_rate=sample_rate, return_tensors="pt").input_values
print("input values: " + str(input_values))
# INFERENCE
print("====== Recognising Speech... ======")
# Storing logits (non-normalized prediction values)
logits = model(input_values).logits
# Storing predicted id's
predicted_ids = torch.argmax(logits, dim=-1)

# Passing the prediction to the tokenizer decode to get the transcription
print("====== Transcription ======")
transcription = processor.decode(predicted_ids[0])
print("Transcription: " + transcription)
# FINE-TUNE
print("====== Fine Tune ======")
target_transcription = "ARCH RIVAL"
#target_transcription = "A MAN SAID TO THE UNIVERSE I EXIST"
print("Target transcription: " + target_transcription)
# encode labels
with processor.as_target_processor():
    labels = processor(target_transcription, return_tensors="pt").input_ids

# compute loss by passing labels
loss = model(input_values, labels=labels).loss
loss.backward()
print("Loss: " + str(loss))
