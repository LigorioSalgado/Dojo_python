from tkinter import Tk, Label, RAISED, BOTH
import pyperclip

max_cell_clip = 10

def updateClipboard():
    cliptext = pyperclip.paste()
    processCliping(cliptext=cliptext)
    root.after(ms=100, func=updateClipboard)

def processCliping(cliptext):#Vamos a asignar nuestro texto a un label
     clipTextCleaned = cleanClipText(cliptext=cliptext)
     for l in labelArray:
         if l["text"] is "":
             #index = str(l["label"])
             #my_label = label[index]
             label["text"] = clipTextCleaned
         else:
             print("Ya no hay espcio") 

def cleanClipText(cliptext): #Vamos a remover caracteres raros
    clip = "".join([c for c in cliptext if ord(c) <= 65535])
    return clip

def onClick(labelNum):
    labelElm = labelArray[labelNum]
    labelObj = labelElm["label"]
    if labelObj["text"] is "":
        print("No hay nada")
        return
    print(labelText)
    pyperclip.copy(labelObj["text"])
    


if __name__ == '__main__':
    labelArray = []
    root = Tk() # Iniciamos nuestro lienzo
    for i in range(max_cell_clip):
        label = Label(root, text="", cursor="plus", relief=RAISED, pady=5, wraplength=500)
        label.pack(fill=BOTH, padx=5, pady=2, expand=1)
        label.bind("<Button-1>", lambda event, labelNum=i: onClick(labelNum))
        labelArray.append({
            "label": i,
            "text": "",
            "clickCount": 0,
            "updated": 0
        })
    updateClipboard()
    root.mainloop() # Iniciar nuestra UI


