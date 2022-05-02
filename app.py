import json
import pickle
import cv2
import parselmouth
import sklearn
import numpy as np
import pandas as pd
from parselmouth.praat import call
from flask import Flask, request, jsonify, url_for, redirect, send_file
from flask_cors import CORS, cross_origin
from skimage import feature
from sklearn.preprocessing import MinMaxScaler
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib import colors

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# Questionnaire List
resultQuestionnaire = []
questions = [{
            "question" : "Do you have any slow movement in your limbs, face, walking, or overall body?",
            "option_1" : "Yes, I do",
            "option_2" : "Sometimes",
            "option_3" : "No, I don't"
        },{
            "question" : "Do you have a tremor, or shaking, in one of your limbs, most commonly your hand or fingers?",
            "option_1" : "Yes, I do",
            "option_2" : "Sometimes",
            "option_3" : "No, I don't"
        },{
            "question" : "Do you have muscle stiffness that is both unpleasant and limits your range of motion?",
            "option_1" : "Yes, I do",
            "option_2" : "Sometimes",
            "option_3" : "No, I don't"
        },{
            "question" : "Do you find yourself losing your sense of balance?",
            "option_1" : "Yes, I do",
            "option_2" : "Sometimes",
            "option_3" : "No, I don't"
        },{
            "question" : "Have you noticed a lack of automatic movements such as blinking, smiling, or swinging your arms as you walk?",
            "option_1" : "Yes, I do",
            "option_2" : "Sometimes",
            "option_3" : "No, I don't"
        },{
            "question" : "Do you have a problem with your sense of smell?",
            "option_1" : "Yes, I do",
            "option_2" : "Sometimes",
            "option_3" : "No, I don't"
        },{
            "question" : "Do you have difficulties sleeping and find yourself thrashing around in bed or acting out nightmares while you're deeply asleep?",
            "option_1" : "Yes, I do",
            "option_2" : "Sometimes",
            "option_3" : "No, I don't"
        },{
            "question" : "Have others commented on how soft your voice is or how hoarse you sound?",
            "option_1" : "Yes, I do",
            "option_2" : "Sometimes",
            "option_3" : "No, I don't"
        },{
            "question" : "Have you ever been told that you have a serious, depressed, or enraged expression on your face, even when you are not upset?",
            "option_1" : "Yes, I do",
            "option_2" : "Sometimes",
            "option_3" : "No, I don't" 
        },{
            "question" : "Do you find yourself feeling dizzy when you get out of a seat?",
            "option_1" : "Yes, I do",
            "option_2" : "Sometimes",
            "option_3" : "No, I don't"
        }]

# Audio Features Lists
localJitter_list = [] 
localabsoluteJitter_list = [] 
rapJitter_list = [] 
ppq5Jitter_list = [] 
localShimmer_list =  [] 
localdbShimmer_list = [] 
apq3Shimmer_list = [] 
aqpq5Shimmer_list = [] 
apq11Shimmer_list =  [] 
ddpJitter_list = []
ddaShimmer_list = []
hnr05_list = [] 
hnr15_list = [] 
hnr25_list = [] 
voiceStatus_list = []

# Spiral Result
spiralResult = []

# Get audio features 
def measurePitch(voiceID, f0min, f0max, unit):
    sound = parselmouth.Sound(voiceID) # read the sound
    pitch = call(sound, "To Pitch", 0.0, f0min, f0max)
    pointProcess = call(sound, "To PointProcess (periodic, cc)", f0min, f0max)
    localJitter = call(pointProcess, "Get jitter (local)", 0, 0, 0.0001, 0.02, 1.3)
    localabsoluteJitter = call(pointProcess, "Get jitter (local, absolute)", 0, 0, 0.0001, 0.02, 1.3)
    rapJitter = call(pointProcess, "Get jitter (rap)", 0, 0, 0.0001, 0.02, 1.3)
    ppq5Jitter = call(pointProcess, "Get jitter (ppq5)", 0, 0, 0.0001, 0.02, 1.3)
    ddpJitter = call(pointProcess, "Get jitter (ddp)", 0, 0, 0.0001, 0.02, 1.3)
    localShimmer =  call([sound, pointProcess], "Get shimmer (local)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    localdbShimmer = call([sound, pointProcess], "Get shimmer (local_dB)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    apq3Shimmer = call([sound, pointProcess], "Get shimmer (apq3)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    aqpq5Shimmer = call([sound, pointProcess], "Get shimmer (apq5)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    apq11Shimmer =  call([sound, pointProcess], "Get shimmer (apq11)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    ddaShimmer = call([sound, pointProcess], "Get shimmer (dda)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    harmonicity05 = call(sound, "To Harmonicity (cc)", 0.01, 500, 0.1, 1.0)
    hnr05 = call(harmonicity05, "Get mean", 0, 0)
    harmonicity15 = call(sound, "To Harmonicity (cc)", 0.01, 1500, 0.1, 1.0)
    hnr15 = call(harmonicity15, "Get mean", 0, 0)
    harmonicity25 = call(sound, "To Harmonicity (cc)", 0.01, 2500, 0.1, 1.0)
    hnr25 = call(harmonicity25, "Get mean", 0, 0)
    harmonicity35 = call(sound, "To Harmonicity (cc)", 0.01, 3500, 0.1, 1.0)
    hnr35 = call(harmonicity35, "Get mean", 0, 0)
    harmonicity38 = call(sound, "To Harmonicity (cc)", 0.01, 3800, 0.1, 1.0)
    hnr38 = call(harmonicity38, "Get mean", 0, 0)
    return localJitter, localabsoluteJitter, rapJitter, ppq5Jitter, ddpJitter, localShimmer, localdbShimmer, apq3Shimmer, aqpq5Shimmer, apq11Shimmer, ddaShimmer, hnr05, hnr15 ,hnr25

# Get round off Values for the audio values
def roundOffInputValues(num, dec=4):
    num = str(num)[:str(num).index('.')+dec+2]
    if num[-1]>='5':
        return float(num[:-2-(not dec)]+str(int(num[-2-(not dec)])+1))
    return float(num[:-1])

# Extracting features of the image
def imageFeatureExtraction(image):
    image_features = feature.hog(image, orientations=9,
    pixels_per_cell=(10, 10), cells_per_block=(2, 2),
    transform_sqrt=True, block_norm="L1")
    return image_features

# Pre-processing and predicting the spiral image
def spiralPredictionProcess(model, imagePath):
    image = cv2.imread(imagePath)
    output = image.copy() 
    output = cv2.resize(output, (128, 128))
    # Pre-process the image
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = cv2.resize(image, (200, 200))
    image = cv2.threshold(image, 0, 255,
                          cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    # Extracting features
    features = imageFeatureExtraction(image)
    preds = model.predict([features])
    label = "Parkinsons" if preds[0] else "Healthy"
    return label

@app.route('/')
def home():
    return questions

# Questionnaire Endpoint
@app.route('/questionnaire', methods=["GET","POST"])
def questionnaire():
    if request.method == 'POST':
        questionnaireResponseResult = request.get_json(force=True)['questionnaire_result']
        for result in questionnaireResponseResult:
            resultQuestionnaire.append(result)
        return jsonify({"Endpoint" : "/voice"})
    else:
        return jsonify({'Questions': questions})

# Voice Endpoint
@app.route('/voice', methods=["POST"])
def voice():
    # todo >>>>>> get audio from the request and pass to "sound" below
    if "file" not in request.files:
        return redirect(request.url)

    audioFile = request.files["file"]
    audioFile.save
    if audioFile.filename == "":
        return redirect(request.url)
    
    sound = parselmouth.Sound(audioFile)
    (localJitter, localabsoluteJitter, rapJitter, ppq5Jitter, ddpJitter, localShimmer, localdbShimmer, apq3Shimmer, aqpq5Shimmer, apq11Shimmer, ddaShimmer, hnr05, hnr15 ,hnr25) = measurePitch(sound, 75, 1000, "Hertz")
    localJitter_list.append(localJitter) # make a mean F0 list
    localabsoluteJitter_list.append(localabsoluteJitter) # make a sd F0 list
    rapJitter_list.append(rapJitter)
    ppq5Jitter_list.append(ppq5Jitter)
    localShimmer_list.append(localShimmer)
    localdbShimmer_list.append(localdbShimmer)
    apq3Shimmer_list.append(apq3Shimmer)
    aqpq5Shimmer_list.append(aqpq5Shimmer)
    apq11Shimmer_list.append(apq11Shimmer)
    ddaShimmer_list.append(ddaShimmer)
    ddpJitter_list.append(ddpJitter)
    hnr05_list.append(hnr05)
    hnr15_list.append(hnr15)
    hnr25_list.append(hnr25)

    # Loading the Model
    with open("D:/STUDIES/FINAL YEAR/FYP/IMPLEMENTATION/ParkinsonsDetection/Audio/VoiceModel.pkl", 'rb') as audioFile:  
        model = pickle.load(audioFile)

    input_data = (roundOffInputValues(localJitter_list[0]), roundOffInputValues(localabsoluteJitter_list[0]), roundOffInputValues(rapJitter_list[0]), roundOffInputValues(ppq5Jitter_list[0]), roundOffInputValues(ddpJitter_list[0]), roundOffInputValues(localShimmer_list[0]), roundOffInputValues(localdbShimmer_list[0]), roundOffInputValues(apq3Shimmer_list[0]), roundOffInputValues(aqpq5Shimmer_list[0]), roundOffInputValues(apq11Shimmer_list[0]), roundOffInputValues(ddaShimmer_list[0]), roundOffInputValues(hnr05_list[0]), roundOffInputValues(hnr15_list[0]), roundOffInputValues(hnr25_list[0]))
    
    # Converting the data to numpy array
    input_data_array = np.asarray(input_data)

    # Reshaping the array 
    reshape_input_data = input_data_array.reshape(1, -1)

    # Scaling the features
    scale = MinMaxScaler((-1,1)) #(-1,1)

    # Standardizing the input data
    standardize_input_data = scale.transform(reshape_input_data)

    # Predicting
    model_prediction = model.predict(standardize_input_data)
    voiceStatus_list.append(model_prediction)
    
    return jsonify({"Endpoint" : "/spiral"})

# Spiral Endpoint
@app.route('/spiral', methods=["POST"])
def spiral():
    # Loading the Model
    with open("D:/STUDIES/FINAL YEAR/FYP/IMPLEMENTATION/ParkinsonsDetection/SpiralDrawing/SpiralModel.pkl", 'rb') as file:  
        model = pickle.load(file)
    # todo >>>>>> get image from the request and pass to "prediction" below
    imagefile = request.files.get('imagefile', '')

    prediction = spiralPredictionProcess(model, imagefile)
    spiralResult.append(prediction)

    return jsonify({"Endpoint" : "/result"})

# Reult Endpoint
@app.route('/result', methods=["GET"])
def result():
    # todo >>>>>> create PDF as report
    fileName = 'ParkD_Result.pdf'
    documentTitle = 'Result'
    title = 'ParkD'
    titleDefinition = "Detecting Parkinson's Disease using vocal measurement and spiral hand drawing"

    questionnaireTitle = 'Questionnaire Result'
    voiceTitle = 'Voice Detection Result'
    spiralResult = 'Spiral Detection Result'
    questionnaireTextLines = [
        f'{questions[0]["question"]}                                                               No',
        f'{questions[1]["question"]}                                                No',
        f'{questions[2]["question"]}                                                      No',
        f'{questions[3]["question"]}                                                                                         No',
        f'{questions[4]["question"]}                               No',
        f'{questions[5]["question"]}                                                                                             No',
        f'{questions[6]["question"]}          No',
        f'{questions[7]["question"]}                                                                   No',
        f'{questions[8]["question"]}               No',
        f'{questions[9]["question"]}                                                                             No'
    ]

    voiceTextLines = [
        f'Jitter Local                                                {localJitter_list[0]}',
        f'Jitter (Abs)                                                {localabsoluteJitter_list[0]}',
        f'Jitter RAP                                                  {rapJitter_list[0]}',
        f'Jitter PPQ5                                                 {ppq5Jitter_list[0]}',
        f'Jitter DDP                                                  {ddpJitter_list[0]}',
        f'Shimmer local                                               {localShimmer_list[0]}',
        f'Shimmer local db                                            {localdbShimmer_list[0]}',
        f'Shimmer apq3                                                {apq3Shimmer_list[0]}',
        f'Shimmer aqpq5                                               {aqpq5Shimmer_list[0]}',
        f'Shimmer aqpq11                                              {apq11Shimmer_list[0]}',
        f'Shimmer DDA                                                 {ddaShimmer_list[0]}',
        f'HNR 05                                                      {hnr05_list[0]}',
        f'HNR 15                                                      {hnr15_list[0]}',
        f'HNR 25                                                      {hnr25_list[0]}'
    ]

    image = 'D:/STUDIES/FINAL YEAR/FYP/IMPLEMENTATION/ParkinsonsDetection/SpiralDrawing/testing_parkinsons.png'

    # creating a pdf object
    pdf = canvas.Canvas(fileName)
    
    # setting the title of the document
    pdf.setTitle(documentTitle)

    # Page 1
    pdf.setFillColorRGB(0.58,0.10,0.00)
    pdf.setFont("Courier-BoldOblique", 20)
    pdf.drawCentredString(300, 800, title)

    pdf.setFillColor(colors.black)
    pdf.setFont("Courier", 10)
    pdf.drawString(80, 770, titleDefinition)

    pdf.setFont("Times-Bold", 10)
    pdf.drawString(40, 740, questionnaireTitle)

    text = pdf.beginText(40, 720)
    text.setFont("Courier", 6)
    text.setFillColor(colors.black)
    text.leading = 24
    for line in questionnaireTextLines:
        text.textLine(line)
        text.textLine("")
    pdf.drawText(text)

    pdf.setFont("Courier-BoldOblique", 8)
    pdf.drawString(40, 570, "Findings")

    percent = 0
    pdf.setFont("Courier", 6)
    pdf.drawString(40, 560, f"{percent}% has been detected from the questionnaire")
    pdf.showPage()

    # Page 2
    pdf.setFillColorRGB(0.58,0.10,0.00)
    pdf.setFont("Courier-BoldOblique", 20)
    pdf.drawCentredString(300, 800, title)

    pdf.setFillColor(colors.black)
    pdf.setFont("Courier", 10)
    pdf.drawString(80, 770, titleDefinition)

    pdf.setFont("Times-Bold", 10)
    pdf.drawString(40, 740, voiceTitle)

    text = pdf.beginText(40, 720)
    text.setFont("Courier", 6)
    text.setFillColor(colors.black)
    text.leading = 24
    for line in voiceTextLines:
        text.textLine(line)
        text.textLine("")
    pdf.drawText(text)

    pdf.setFont("Courier-BoldOblique", 8)
    pdf.drawString(40, 500, "Findings")

    voiceResult = "Not Detected"
    pdf.setFont("Courier", 6)
    pdf.drawString(40, 490, f"Disease is {voiceResult} based on the auditory input.")
    pdf.showPage()

    # Page 3
    pdf.setFillColorRGB(0.58,0.10,0.00)
    pdf.setFont("Courier-BoldOblique", 20)
    pdf.drawCentredString(300, 800, title)

    pdf.setFillColor(colors.black)
    pdf.setFont("Courier", 10)
    pdf.drawString(80, 770, titleDefinition)

    pdf.setFont("Times-Bold", 10)
    pdf.drawString(40, 740, spiralResult)

    pdf.drawInlineImage(image, 130, 300)

    pdf.setFont("Courier-BoldOblique", 8)
    pdf.drawString(40, 180, "Findings")

    voiceResult = "Not Detected"
    pdf.setFont("Courier", 6)
    pdf.drawString(40, 170, f"Disease is {voiceResult} based on the image input.")
    pdf.showPage()

    # saving the pdf
    pdf.save()

    with open(fileName, 'rb') as resultFile:
        return send_file(resultFile, attachment_filename=fileName)

if __name__ == '__main__':
    app.run()