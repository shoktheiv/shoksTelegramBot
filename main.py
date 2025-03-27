import os
import random
import telebot
from words import words as l

from telebot import types
from pymongo import MongoClient
from PyMultiDictionary import MultiDictionary as myDictionary
API_KEY = "bruv"
DB_KEY = "bruv"

cluster = MongoClient(DB_KEY)
db = cluster['telegram']
database = db['points']

bot = telebot.TeleBot(API_KEY)

words = "about ability above able abandon abandoned abroad absence absent absolute absolutely absorb abuse academic accent accept acceptable access accident accidental accidentally accommodation accompany according to account accurate accurately accuse achieve achievement acknowledge acquire across act action active actively activity actor; actress actual actually adapt addition additional address adequate adequately adjust admire admit adopt adult advance advanced advantage adventure advertise advertisement advertising advice advise affair affection afford afraid after afternoon afterwards again against age agency aggressive ago agree agreement ahead aim airport alarm alarming alcohol alcoholic alive all right allow ally almost alone along aloud alphabet alphabetical alphabetically already alternative although altogether always amaze amazing ambition ambulance among(amongst) amount amuse amusing analyse analyze analysis ancient anger angle angrily angry animal ankle anniversary announce annoy annoyed annoying annual annually another answer anticipate anxiety anxious anxiously any anyone anybody anything anyway anywhere apart apartment apologize apparent apparently appeal appear appearance apple application apply appoint appointment appreciate approach appropriate approval approve approving approximate approximately april area argue argument arise arm armed army around arrange arrangement arrest arrival arrive arrow art article artificial artist artistic ashamed aside ask asleep aspect assist assistance assistant associate association assume assure atmosphere attach attached attack attempt attend attention attitude attorney attract attraction attractive audience august aunt authority automatic automatically available average avoid awake award aware away awful awfully awkward awkwardly back background backwards bad bad-tempered badly bag baggage bake balance ball ban bandage bank bar bargain barrier base basic basically basis bath bathroom battle bay beach bear beard beat beautiful beautifully beauty because become bed bedroom beef beer before begin beginning behalf behave behavior behind belief believe belong below belt bend benefit beside bet better best between beyond bicycle bid big bill biology bird birth birthday bit bite bitter black blame blank blind block blood blow blue boat body boil bone book boot border bored boring born borrow boss both bother bottle bottom bound bowl box boy brain branch brand brave bread break breakfast breast breath breathe breathing brick bridge brief briefly bright brightly brilliant bring broad broadcast broadly brother brown brush bubble budget build building bunch burn burst bury bus bush business businessman businesswoman busy but butter button buy by bye cabinet cable cake calculate call calm calmly camera camp can cancel cancer candidate candy capable capacity capital captain capture car card cardboard career careful carefully careless carelessly carpet carry case cash castle catch cause ceiling celebrate celebration cellphone cent center century ceremony certainly certificate chain chair chairman chairwoman challenge chance change channel chapter character characteristic charge charity chase chat cheap cheat check cheek cheerful cheerfully chemical chemist chemistry chest chew chicken chief child chin chocolate choice choose church cigarette cinema circle circumstance citizen city civil claim clap class classic classroom clean clear clearly clerk clever client climate climb climbing clock close closely closet clothes clothing cloud coach coat coffee coin cold collapse colleague collect collection college color combination combine come comedy comfort comfortable command comment commission commit commitment committee common commonly communicate communication community company compare comparison compete competition competitive complain complaint complete completely complex complicate complicated computer concentrate concentration concern concerned concert conclude conclusion concrete condition conduct conference confidence confident confine confirm conflict confront confuse confused confusing confusion congratulations congress connect connection consequence conservative consider considerable considerably consideration consist of constant constantly construct construction consult consumer contact contain content contest context continent continue continuous continuously contract contrast contribute contribution control convenient convention conventional conversation convert convince cook cooker cookie cooking cool cope core corner correct cost cottage cough could count counter country countryside couple courage course court cousin cover cow crack crash crazy cream create creature credit crime crisis critical criticism criticize crop cross crowd crowded crown crucial cruel crush cry cultural culture cup cupboard cure curious curl curly current currently curtain curve custom customer cut cycle dad daily damage damp dance dancer danger dangerous dare dark data date daughter day dead deaf deal dear death debate debt decade decay december decide decision declare decline decorate decoration decrease deep deeply defeat defend define definite definitely definition degree delay deliberate deliberately delicate delight deliver delivery demand demonstrate dentist deny department departure depend deposit depress depressed depth describe description desert deserted deserve design desire desk desperate desperately despite destroy destruction detail detailed determination determine determined develop development device devote devoted diagram diamond diary dictionary die diet difference different differently difficult difficulty dig dinner direct direction directly director dirt dirty disadvantage disagree disappear disappoint disappointed disappointment disapproval disapprove disaster discipline discount discover discovery discuss discussion disease disgust disgusted disgusting dish dishonest dislike dismiss dissolve distance distinguish distribute district disturb divide divorce do doctor document dog dollar domestic dominate door dot double doubt down downstairs dozen draft drag dramatic dramatically draw drawing dream dress drink drive driver driving drop drug drum drunk dry due dull during dust duty each ear early earn earth ease easily east eastern easy economic economy edge edition educate education effect effective effectively efficient efficiently effort egg either elbow elderly elect election electric electrical electronic elegant elevator else elsewhere embarrass embarrassed embarrassing embarrassment emerge emergency emotion emotional emphasis emphasize employ employee employer employment empty enable encounter encourage encouragement end ending enemy energy engaged engine engineer engineering enjoy enjoyable enormous enough ensure enter entertain entertaining entertainment enthusiasm enthusiastic entire entirely entitle entrance entry envelope environment environmental equal equally equipment equivalent error escape especially essay essential essentially establish estate estimate etc (et cetera) euro even evening event eventually ever every everyone everything everywhere evidence evil exact exactly exaggerate exam examine example excellent except exception exchange excited excitement exciting exclude excuse executive exercise exhibit exhibition exist existence exit expand expect expectation expense expensive experience experiment expert explain explanation explode explore explosion export expose express expression extend extensive extent extra extraordinary extreme extremely eye"

# commands is the aliases of discord so its quite useful
# Returning the meanings

os.chdir("C:\\Users\\ergas\\PycharmProjects\\Showdown")


def open_account(user_id, username):

    if database.find({"_id": user_id}) is not None:
        return True
    else:
        database.insert_one({'_id': user_id, 'username': username, 'points': 0, 'expected_answer': 'null'})
        return False


def handle_query(call):
    open_account(call.from_user.id, call.from_user.username)
    user_id = call.from_user.id
    user = database.find_one({"_id": user_id})

    if len(call.data.split('#')) < 2:
        return

    call_back = call.data.split('#')[1]


    if call.data.split('#')[0] == 'quiz':
        if user['expected_answer'] == call_back and str(user_id) == call.data.split('#')[2]:
            add_points = random.randrange(2, 5)
            database.update_one({"_id": user_id}, {"$set":{"points": user['points'] + add_points}})
            markup = types.InlineKeyboardMarkup()

            database.update_one({"_id": user_id}, {"$set": {"expected_answer": "null"}})

            user = database.find_one({"_id": user_id})

            markup.add(types.InlineKeyboardButton(text="Play again", callback_data="play_again#"))

            bot.send_message(call.message.chat.id, f"Congratulations {call_back} was the right answer! \nYou've earned yourself {add_points} \nYou have: {user['points']} points", reply_markup=markup)

            return
        elif user['expected_answer'] == 'null':
            bot.send_message(call.message.chat.id, "Please start a new game, /play")

        elif user['expected_answer'] != call_back and str(user_id) == call.data.split('#')[2]:
            bot.send_message(call.message.chat.id, "You have selected the wrong answer :(")
            database.update_one({"_id":user_id}, {"$set":{"expected_answer" : "null"}})

    elif call.data.split('#')[0] == "play_again":
        play(user_id, call.message.chat.id, call.from_user.username)

meaning_aliases = ['meaning', 'definition']
def get_meaning(message):
    try:
        dictionary = myDictionary()

        request = message.text.split()
        if len(request) > 3:
            request.remove(request[0])
            request.remove(request[1])
            word = ""
            for i in request:
                word = word + " " + i

            definition = dictionary.meaning('en', word)
            bot.reply_to(message, f"{definition[1]}")
            return
        elif len(request) < 2:
            bot.reply_to(message, "Please specify a word, for example '/definition car'")
            return
        else:
            definition = dictionary.meaning('en', request[1])
            bot.reply_to(message, f"{definition[1]}")
    except:
        print("Smth went wrong bro")


# Returning Synonyms
synonym_aliases = ['synonym']
def get_synonym(message):
    #try:
        open_account(message.from_user.id, message.from_user.username)
        user = database.find_one({"_id": message.from_user.id})
        dictionary = myDictionary()
        request = message.text.split()
        print(request)
        if "expected_answer" in user and user["expected_answer"] != "null":
            bot.reply_to(message , "We have canceled your previous quiz")
            database.update_one({'_id': message.from_user.id}, {"$set": {"expected_answer": 'null'}})

        word = ""

        if len(request) < 2:
            bot.reply_to(message, "Please specify a word, for example '/synonym good'")
        elif len(request) >= 3:
            del request[0]
            del request[0]
            print(request)
            for i in request:
                word = word + " " + i

        synonyms = dictionary.synonym('en', word)
        random.shuffle(synonyms)

        if len(synonyms) > 4:
            synonyms = synonyms[:4]
        elif len(synonyms) == 0:
            bot.send_animation(message.chat.id, "https://media.tenor.com/videos/4d25296899b9adacb771b138b1c05005/mp4?c=VjFfZGlzY29yZA", caption=f"Sorry couldn't find any synonyms for <{request[1]}>")
            return

        markup = types.InlineKeyboardMarkup()

        for value in synonyms:
            markup.add(types.InlineKeyboardButton(text=value, callback_data="synonym#" + value))

        bot.reply_to(message, f"Here are some synonyms for {word}: ", reply_markup=markup, parse_mode='HTML')
    #except:
    #    print("something is wrong bro")


def help_command(message):
    try:
        text = "Here are all the commands you can try out!"
        markup = types.InlineKeyboardMarkup()

        markup.add(types.InlineKeyboardButton(text="/definition word", callback_data="[meaning]"),
                   types.InlineKeyboardButton(text="/d word", callback_data="[meaning]"))

        markup.add(types.InlineKeyboardButton(text="/synonym word", callback_data="[synonym]"),
                   types.InlineKeyboardButton(text="/s word", callback_data="[synonym]"))

        markup.add(types.InlineKeyboardButton(text="/play", callback_data="play_again#"))

        bot.reply_to(message, text, reply_markup=markup)
    except:
        print("Smth went wrong bro")



def play(user_id, chat_id, username):

        open_account(user_id, username)
        user = database.find_one({"_id": user_id})

        if "expected_answer" in user and user["expected_answer"] != "null":
            bot.send_message(chat_id, "Whooa, answer the previous question first")
            return

        dictionary = myDictionary()

        l = words.split()

        word = random.choice(l)
        words.remove(word)

        word_meaning = dictionary.synonym(lang='en' , word=word)

        if len(word_meaning) < 1:
            bot.send_message(chat_id, "Please try again, failed to fetch a game")
            return

        database.update_one({"_id": user_id}, {"$set": {"expected_answer": word_meaning[0]}})

        options = []
        for i in range(3):
            option = random.choice(l)
            words.remove(option)
            options.append(option)

        print(word_meaning[0])

        options.append(word_meaning[0])
        random.shuffle(options)

        markup = types.InlineKeyboardMarkup()

        for i in options:
            markup.add(types.InlineKeyboardButton(text=i, callback_data=f"quiz#{str(i)}#{str(user_id)}"))

        bot.send_message(chat_id, f"Which of these words best match '{word}'", reply_markup=markup)


def listener(messages):
    for message in messages:
        if message.content_type == "text":
            content = message.text.split()
            print(content[0])
            if content[0] in ['/start', '/help']:
                help_command(message)
            elif content[0] in meaning_aliases and content[1] == 'of':
                get_meaning(message)
            elif content[0] in synonym_aliases and content[1] == 'of':
                get_synonym(message)
            elif content[0] == 'play':
                play(message.from_user.id, message.chat.id, message.from_user.username)


bot.set_update_listener(listener)
bot.polling()
