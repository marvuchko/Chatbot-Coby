import random
from chatterbot import ChatBot
from settings import *
import logging
import re

####### Bot class

class Bot:
    "This class defines our chatbot's behaviour"

    ###Constructor

    def __init__(self, name, bottype):
        "This is a constructor of our bot's class"
        self.name = name
        self.bot = self.createBot(bottype)
        self.begin_conversation = True
        return

    ###Methods

    def createBot(self, bottype):
        "This method creates a chatbot with a defined trainer"
        chatbot = "" 
        if (bottype == "Twitter"):
            chatBot = ChatBot(
                "Coby",
                 preprocessors=[
                    'chatterbot.preprocessors.convert_to_ascii'
                ],
                filters=["chatterbot.filters.RepetitiveResponseFilter"],
                database="./twitter-database.db",
                twitter_language="en",
                twitter_consumer_key=TWITTER["CONSUMER_KEY"],
                twitter_consumer_secret=TWITTER["CONSUMER_SECRET"],
                twitter_access_token_key=TWITTER["ACCESS_TOKEN"],
                twitter_access_token_secret=TWITTER["ACCESS_TOKEN_SECRET"],
                trainer="chatterbot.trainers.TwitterTrainer")
        else :
            chatBot = ChatBot(
                "Coby", 
                trainer="chatterbot.trainers.ListTrainer",
                database="./sqliteFileDatabase")
        return chatBot

    def train_from_file(self, text):
        "This metod trains chat bot from a specific text file"
        self.bot = self.createBot("List")
        self.bot.train(text)
        return

    def set_trainer(self, bottype):
        "Sets a trainer of a chatbot"
        self.bot = self.createBot(bottype)
        self.begin_conversation = False
        return self.bot

    def greeting_message(self):
        "This method returns a random greet message"
        messages = [
            "Hello!", "Hi!", "Greetings!", "Hi there!", "Howdey partner!"
        ]
        return random.choice(messages)

    def reply_message(self, text):
        "This method returns a reply from a bot"
        message = ""
        if(self.begin_conversation):
            message = self.greeting_message()
            self.begin_conversation = False
        else:
            message = self.bot.get_response(text).text
        return self.name + " says: \"" + self.format_message(message) + "\""

    def split_sentences(self, text):
        "Splits input text"
        self.splited_sentences = [s.strip() for s in re.split('[\.\?!]', text) if s]
        count = len(self.splited_sentences)
        if self.splited_sentences[count - 1] is '':
            self.splited_sentences.pop(count - 1)

    def train_bot_via_twitter(self):
        "Trains the bot via Twitter"
        Thread(target=self.twitter_training).start()

    def train_bot_via_list(self, text):
        "Trains the bot from a conversation string"
        self.split_sentences(text)
        self.train_from_file(self.splited_sentences)

    def format_message(self, text):
        "Formats message to be appropriate for chatbot"
        text = re.sub('@[^ ]* ', '', text)
        text = re.sub('http[^ ]* ', '', text)
        return text

    def twitter_training(self):
        "This method collects required knowledge from the Twitter"
        logging.basicConfig(level=logging.INFO)
        self.bot = self.createBot("Twitter")
        self.bot.train();
        return

######
