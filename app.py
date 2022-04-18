from flask import Flask
import json

app = Flask(__name__)

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
count = 0

def increment(count):
    count +=1
    return count

@app.route('/')
def home():
    return questions

@app.route('/questionnaire')
def questionnaire():
    if count == 10:
        return(json.dump({"question" : "none"}))
    value = questions[count] 
    count = increment(count)
    return value
  

if __name__ == '__main__':
    app.run()