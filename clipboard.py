from tkinter import Tk, Label, Frame, Menu
import pyperclip


class Clipboard(Frame):
    def __init__(self, parent=None):
        self.parent = parent
        Frame.__init__(self,parent,height=600, width=600)
        parent.title("Clipboard History")
        parent.resizable(False, False)
        self.initDefaultValues()
        self.pack_propagate(0)
        self.pack()
        self.pollingFrequency = 100 #Esto esta en MS
        self.truncateTextLength = 100 #Maximo de caracteres
        self.maxLabelsOnApp = 10
        self.labelArray = []

        self.initMenu()

    
    def initDefaultValues(self):
        self.clipBoardContent = set()
        self.contentMapping = {}
        self.labelUpdateValue = 0
    
    def initMenu(self):
        menu = Menu(self)
        optionBar = Menu(menu, tearoff=0)
        optionBar.add_command(label="Clear all text", command=self.clearAll)
        menu.add_cascade(label="Options", menu=optionBar)
        self.parent.config(menu=menu)

    def createLayout(self):
        for i in range(self.maxLabelsOnApp):
            label = Label(self, text="", cursor="plus", relief="raised", pady=5, wraplength=500)
            label.pack(fill="both", padx=5, pady=2, expand=1)
            label.bind("<Button-1>", lambda event, labelNum=i: self.onClick(labelNum))
            self.labelArray.append({
                "label": label,
                "text":"",
                "clickCount": 0,
                "updateCount": 0
            })

    def processClip(self,text):
        cliptext, clipShortext = self.cleanClipText(text) #unpacking

        if cliptext not in self.clipBoardContent and clipShortext:
            if clipShortext not in self.contentMapping:
                self.labelUpdateValue += 1
                labelArrSortByUpdate = sorted(self.labelArray, key= lambda t:t["updateCount"])
                labelArrSortByClicked =  sorted(labelArrSortByUpdate, key= lambda t:t["clickCount"] )

                labelElem = labelArrSortByClicked[0]
                label = labelElem["label"]
                labelText = label["text"]
                if labelText in self.contentMapping:
                    self.clipBoardContent.discard(self.contentMapping[labelText])
                    self.contentMapping.pop(labelText)
                label["text"] = clipShortext
                label["relief"] = "raised"
                labelElem["updateCount"] = self.labelUpdateValue
                labelElem["text"] = clipShortext
                labelElem["clickCount"] = 0
            else:
                self.clipBoardContent.discard(self.contentMapping[labelText])

            self.clipBoardContent.add(cliptext)
            self.contentMapping[clipShortext] = cliptext

            self.update()
            self.parent.update()
            self.pack()


    def updateClipboard(self):
        try:
            cliptext = pyperclip.paste()
            self.processClip(cliptext)
        except Exception as e: 
            print("Exception:", e ) 

        self.after(ms=500, func=self.updateClipboard)  


    def cleanClipText(self, cliptext):
        clip = "".join([char for char in cliptext if ord(char) < 65535])
        if len(clip) > self.truncateTextLength:
            cliptextShort = cliptext[:self.truncateTextLength] + "..." #"Hola como estan ..."
        else:
            cliptextShort = cliptext
        
        cliptextShort = cliptextShort.replace("\n", "").strip()
        return (clip, cliptextShort) #tuple 


    def clearAll(self):
        if True:
            for labelElem in self.labelArray:
                labelElem["label"]["text"] = ""
                labelElem["label"]["relief"] = "raised"
                labelElem["text"] = ""
                labelElem["clickCount"] = 0
                labelElem["updated"] = 0
            self.initDefaultValues()

    def onClick(self, labelNum):
        labelElem = self.labelArray[labelNum]
        label = labelElem["label"]
        if label["text"] == "":
            return
        pyperclip.copy(self.contentMapping[label["text"]])
        label["relief"] = "sunken"
        labelElem["clickCount"] = labelElem["clickCount"] + 1


if __name__ == '__main__':
    root = Tk()
    clip = Clipboard(root)
    clip.createLayout()
    clip.updateClipboard()
    clip.mainloop()

