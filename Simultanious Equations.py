import math
import random


def rand():
    return random.randint(1, 10)


def createlist(selfy):
    selfy.qdict = {
        "a": [rand(), rand(), rand()],
        "b": [rand(), rand(), rand()],
    }
    a0 = selfy.qdict["a"][0]
    a1 = selfy.qdict["a"][1]
    a2 = selfy.qdict["a"][2]
    b0 = selfy.qdict["b"][0]
    b1 = selfy.qdict["b"][1]
    b2 = selfy.qdict["b"][2]
    selfy.q = f'{a0}x + {a1}y = {a2} \n' \
             f'{b0}x + {b1}y = {b2} \n '
    if a0 % b0 == 0 or b0 % a0 or a1 % b1 == 0 or b1 % a1 == 0:
        return
    else:
        createlist()


class question:
    def __init__(self):
        self.qdict = {}
        self.q = ""
        self.ansdict = {}
        self.ans = ""

    def makequestion(self):
        createlist(self)
        return self.q

    def checkquestion(self):
        self.ansdict = self.qdict
        x = (self.ansdict["a"][2]*self.ansdict["b"][1]-self.ansdict["a"][1]*self.ansdict["b"][2])/(self.ansdict["a"][0]*self.ansdict["b"][1]-self.ansdict["a"][1]*self.ansdict["b"][0])
        y = (self.ansdict["a"][0]*self.ansdict["b"][2]-self.ansdict["a"][2]*self.ansdict["b"][0])/(self.ansdict["a"][0]*self.ansdict["b"][1]-self.ansdict["a"][1]*self.ansdict["b"][0])
        return [x, y]


def createquestions():
    qinput = input(currentquestion.makequestion())
    if str.find(qinput, "/"):
        spltinput = str.split(qinput, "/")
        qinput = int(spltinput[0])/int(spltinput[1])
    if qinput == currentquestion.checkquestion()[0] or qinput == currentquestion.checkquestion()[1]:
        print("Correct")
        createquestions()
    else:
        print("Incorrect")
        print(str(currentquestion.checkquestion()))
        createquestions()


currentquestion = question()
createquestions()