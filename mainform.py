import time
from tkinter import *
from tkinter.filedialog import askopenfilename
from threading import Thread
from bot import *

####### MainWindow class

class MainFrame:
    "This is the main window of an application"

    ###Constructor

    def __init__ (self):
        "This is a constructor of a frame"
        self.root = Tk()
        self.root.title("ChatBot Coby")
        self.root.geometry("800x450")
        self.v = IntVar()
        self.v.set(1)
        self.animated = True
        #adding widgets to a main frame
        self.root.resizable(width=False, height=False)
        self.draw_frames()
        self.display_copiright_text()
        self.load_images()
        self.display_graphics()
        self.display_scrollable_text_area()
        self.display_chat_inputs()
        #initializing ChatBot
        self.bot = Bot("Coby", "List")
        self.txt = ""
        #starting the animation of a chat bot
        Thread(target=self.thread_function).start()
        self.root.mainloop()
        return

    ###Methods

    def draw_frames(self):
        "Draws containers for widgets"
        #bottom frame - status bar
        self.bottomFrame = Frame(self.root, width=400, height=20, bg="#151515")
        self.bottomFrame.pack_propagate(0)
        self.bottomFrame.pack(side=BOTTOM, fill=X)
        #left frame - images
        self.leftFrame = Frame(self.root, width=400, height=430, bg="#404090")
        self.leftFrame.pack_propagate(0)
        self.leftFrame.pack(side=LEFT)
        #right frame - text widgets
        self.rightFrame = Frame(self.root, width=400, height=430, bg="#5050A0")
        self.rightFrame.pack_propagate(0)
        self.rightFrame.pack(side=RIGHT)
        #inner frame - container for text widget
        self.innerFrame = Frame(self.rightFrame, width=370, height=340, bg="#5050A0")
        self.innerFrame.pack_propagate(0)
        self.innerFrame.pack(pady=15)
        return

    def display_copiright_text(self):
        "Displays copyright text"
        copyrightBar = Label(self.bottomFrame, text="Copyright \u00A9 Stefan, Milan & Marko", bg="#151515", fg="#ebebeb")
        copyrightBar.pack()
        return

    def load_images(self):
        "Loads required images"
        self.images = [
            PhotoImage(file="resources/cloud1.png"),
            PhotoImage(file="resources/cloud2.png"),
            PhotoImage(file="resources/cloud3.png"),
            PhotoImage(file="resources/cloud4.png"),
            PhotoImage(file="resources/bot.png"),
            PhotoImage(file="resources/logo.png"),
            PhotoImage(file="resources/coby.png")
        ]
        return

    def display_graphics(self):
        "Displays logo, robot and a message cloud"
        #Logo
        self.logo = Label(self.leftFrame, image=self.images[5], bg="#404090")
        self.logo.pack()
        self.logo.place(x=75, y=20)
        #Bot name
        self.botnameLbl = Label(self.leftFrame, image=self.images[6], bg="#404090")
        self.botnameLbl.pack()
        self.botnameLbl.place(x=125, y=70)
        #Bot label
        self.botLbl = Label(self.leftFrame, image=self.images[4], bg="#404090")
        self.botLbl.pack()
        self.botLbl.place(x=125, y=170)
        #Cloud
        self.cloud = Label(self.leftFrame, image='', bg="#404090")
        self.cloud.pack()
        self.cloud.place(x=250, y=110)
        #Train from file button
        self.trainBtn = Button(self.leftFrame, width=5, text="Train", bg="#303080", fg="#ebebeb", activebackground="#404090")
        self.trainBtn.pack()
        self.trainBtn.place(x=10, y=395)
        self.trainBtn.bind("<Button-1>", self.train)
        #Set trainer button
        self.setTrainer = Button(self.leftFrame, width=8, text="Set trainer", bg="#303080", fg="#ebebeb", activebackground="#404090")
        self.setTrainer.pack()
        self.setTrainer.place(x=70, y=395)
        self.setTrainer.bind("<Button-1>", self.set_trainer)
        #Chatbot training modes
        self.modeLbl = Label(self.leftFrame, text="Chatbot mode:", bg="#404090", fg="#ebebeb")
        self.modeLbl.pack()
        self.modeLbl.place(x=5, y=310)
        #Chatbot train from file radiobutton
        self.listTrain = Radiobutton(self.leftFrame, text="List trainer", value=1, variable=self.v)
        self.listTrain.pack()
        self.listTrain.place(x=5, y=330)
        self.listTrain.config(bg="#404090", fg="#ebebeb", selectcolor="#404090", activebackground="#404090")
        #Chatbot train from Twitter radiobutton
        self.twitterTrain = Radiobutton(self.leftFrame, text="Twitter trainer", value=2, variable=self.v)
        self.twitterTrain.pack()
        self.twitterTrain.place(x=5, y=360)
        self.twitterTrain.config(bg="#404090", fg="#ebebeb", selectcolor="#404090", activebackground="#404090")
        return

    def display_scrollable_text_area(self):
        "Displays the text area"
        self.T = Text(self.innerFrame, height=3, width=50, bg="#7575C5", fg="#ebebeb", state="disabled", relief=FLAT)
        S = Scrollbar(self.innerFrame, relief=FLAT, command=self.T.yview)
        S.pack(side=RIGHT, fill=Y)
        self.T.pack(side=LEFT, fill=Y)
        self.T.config(yscrollcommand=S.set)
        return

    def display_chat_inputs(self):
        "Displays the inputs required for messaging"
        #Label
        chatLabel = Label(self.rightFrame, text="Enter message:", bg="#5050A0", fg="#A5A5F5")
        chatLabel.pack(side=LEFT, padx=15, pady=20)
        #Text enty
        self.chatInput = Entry(self.rightFrame, width=25, bg="#7575C5", fg="#ebebeb", relief=FLAT)
        self.chatInput.pack(side=LEFT, pady=20)
        self.chatInput.bind("<Return>", self.send_message)
        #Send button
        sendButton = Button(self.rightFrame, width=50, text="Send", bg="#303080", fg="#ebebeb", activebackground="#404090")
        sendButton.pack(side=RIGHT, padx=15, pady=20)
        sendButton.bind("<Button-1>", self.send_message)
        return


    def thread_function(self):
        "This animates the cloud above the robot"
        i = 0
        Thread(target=self.recv_message).start()
        self.cloud.configure(image=self.images[0])
        while self.animated:
            i += 1
            self.cloud.configure(image=self.images[i % 4])
            time.sleep(1)
        self.cloud.configure(image="")
        #self.recv_message()
        return

    ###Event methods

    def send_message(self, event):
        "Sends the message to a ChatBot"
        self.txt = self.chatInput.get()
        self.T.config(state="normal")
        if (self.txt!=""):
            self.T.insert(END, "Me: " + self.txt + "\n")
        self.chatInput.delete(0, END)
        self.T.config(state="disabled")
        self.animated = True
        Thread(target=self.thread_function).start()
        return

    def set_trainer(self, event):
        "Sets the trainer for the chatbot"
        if(self.v.get() == 1):
            self.bot.bot = self.bot.set_trainer("List")
        if(self.v.get() == 2):
            self.bot.bot = self.bot.set_trainer("Twitter")
        return

    def train(self, event):
        "Trains the bot"    
        if (self.v.get() == 1):
            self.train_from_file();
        if (self.v.get() == 2):
            self.train_from_twitter();
        return

    def recv_message(self):
        "A message recieved from ChatBot"
        time.sleep(2)
        self.T.config(state="normal")
        self.T.insert(END, self.bot.reply_message(self.txt) + "\n", "COLORED")
        self.T.tag_config('COLORED', foreground="#202070")
        self.T.config(state="disabled")
        self.animated = False
        return

    def train_from_twitter(self):
        "Trains bot via Twitter"
        self.bot.train_bot_via_twitter()
        return

    def train_from_file(self):
        "Trains bot from file"
        file_path = askopenfilename(
            filetypes =(("Text File", "*.txt"),("All Files","*.*")),
            title = "Choose a file."
        )
        if(file_path == ""):
            return
        fr = open(file_path, "r")
        file_text = fr.read()
        self.bot.train_bot_via_list(file_text)
        return

####### Execution

MainFrame()

