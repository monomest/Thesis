import torch
import fairseq

cp_path = '/srv/scratch/z5160268/2020_TasteofResearch/wav2vec_large.pt'
model, cfg, task = fairseq.checkpoint_utils.load_model_ensemble_and_task([cp_path])
model = model[0]
model.eval()

wav_input_16khz = torch.randn(1,10000)
z = model.feature_extractor(wav_input_16khz)
c = model.feature_aggregator(z)

print("Context representations c: ", c)
print("Latent speech representations z: ", z)
