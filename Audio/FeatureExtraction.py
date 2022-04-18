import glob
import numpy as np
import pandas as pd
import parselmouth
from parselmouth.praat import call

def measurePitch(voiceID, f0min, f0max, unit):
    sound = parselmouth.Sound(voiceID) # read the sound
    pitch = call(sound, "To Pitch", 0.0, f0min, f0max)
    pointProcess = call(sound, "To PointProcess (periodic, cc)", f0min, f0max)#create a praat pitch object
    localJitter = call(pointProcess, "Get jitter (local)", 0, 0, 0.0001, 0.02, 1.3)
    localabsoluteJitter = call(pointProcess, "Get jitter (local, absolute)", 0, 0, 0.0001, 0.02, 1.3)
    rapJitter = call(pointProcess, "Get jitter (rap)", 0, 0, 0.0001, 0.02, 1.3)
    ppq5Jitter = call(pointProcess, "Get jitter (ppq5)", 0, 0, 0.0001, 0.02, 1.3)
    ddpJitter = call(pointProcess, "Get jitter (ddp)", 0, 0, 0.0001, 0.02, 1.3)
    localShimmer =  call([sound, pointProcess], "Get shimmer (local)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    localdbShimmer = call([sound, pointProcess], "Get shimmer (local_dB)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    apq3Shimmer = call([sound, pointProcess], "Get shimmer (apq3)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    aqpq5Shimmer = call([sound, pointProcess], "Get shimmer (apq5)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    ddaShimmer = call([sound, pointProcess], "Get shimmer (dda)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    harmonicity = call(sound, "To Harmonicity (cc)", 0.01, 75, 0.1, 1.0)
    hnr = call(harmonicity, "Get mean", 0, 0)
    return localJitter, localabsoluteJitter, rapJitter, ppq5Jitter, ddpJitter, localShimmer, localdbShimmer, apq3Shimmer, aqpq5Shimmer, ddaShimmer, hnr

# file_list = []
localJitter_list = []
localabsoluteJitter_list = []
rapJitter_list = []
ppq5Jitter_list = []
localShimmer_list = []
localdbShimmer_list = []
apq3Shimmer_list = []
aqpq5Shimmer_list = []
ddpJitter_list = []
hnr_list = []
ddaShimmer_list = []
status_list = []

sound = parselmouth.Sound("AudioTesting\data_audio\ReadText\HC\ID03_hc_0_0_0.wav")
(localJitter, localabsoluteJitter, rapJitter, ppq5Jitter, ddpJitter, localShimmer, localdbShimmer, apq3Shimmer, aqpq5Shimmer, ddaShimmer, hnr) = measurePitch(sound, 75, 1000, "Hertz")
# file_list.append(wave_file) # make an ID list
localJitter_list.append(localJitter) # make a mean F0 list
localabsoluteJitter_list.append(localabsoluteJitter) # make a sd F0 list
rapJitter_list.append(rapJitter)
ppq5Jitter_list.append(ppq5Jitter)
ddpJitter_list.append(ddpJitter)
localShimmer_list.append(localShimmer)
localdbShimmer_list.append(localdbShimmer)
apq3Shimmer_list.append(apq3Shimmer)
aqpq5Shimmer_list.append(aqpq5Shimmer)
ddaShimmer_list.append(ddaShimmer)
hnr_list.append(hnr)
status_list.append(1)


print(localJitter_list[0],",", localabsoluteJitter_list[0],",", rapJitter_list[0],",", ppq5Jitter_list[0],",", ddpJitter_list[0],",", localShimmer_list[0],",", localdbShimmer_list[0],",", apq3Shimmer_list[0],",", aqpq5Shimmer_list[0],",", ddaShimmer_list[0],",", hnr_list[0])
