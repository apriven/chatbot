"""
This is the template server side for ChatBot
"""
import requests as requests
from bottle import route, run, template, static_file, request
import json
from random import choice

reactions = ["afraid", "bored", "confused", "crying", "dancing", "dog", "excited", "giggling", "heartbroke", "inlove", "laughing", "money", "no", "ok", "takeoff", "waiting"]

#user input
love = ["love", "loving", "heart", "lov"]
money = ["money", "dollar", "cash", "gold", "plata"]
curses = ["fuck", "bitch", "asshole", "shit", "ass", "fucking", ""]
animals = ["dog", "dogs", "cat", "cats", "animal", "animals", "pet", "pets"]
jokes_in = ["joke", "jokes", "laugh", "hahaha"]

#bot output
jokes = ["Did you hear about the restaurant on the moon? Great food, no atmosphere.",
         "What do you call a fake noodle? An Impasta.", "How many apples grow on a tree? All of them",
         "Want to hear a joke about paper? Nevermind it's tearable",
         "I just watched a program about beavers. It was the best dam program I've ever seen."]
question_answer = ["Great question!", "Hmmmm...I have no idea", "Google it!", "Ahhn???"]
curses_answer = ["Sorry, I don't talk to animals...", "Where did you learn this words?", "Do your mom knows taht your are "]

@route('/', method='GET')
def index():
    return template("chatbot.html")


@route("/chat", method='POST')
def chat():
    user_message = request.POST.get('msg')
    the_message = user_message.split(" ")

    for word in the_message:
        for letter in word:
            if letter[0].isupper():
                return json.dumps({"animation": "excited", "msg": "Hello "+user_message})
    if any(word in love for word in the_message):
        return love_func(the_message)
    if any(word in animals for word in the_message):
        return animals_func(the_message)
    elif any(word in money for word in the_message):
        return json.dumps({"animation": "money", "msg": "MONEY"})
    elif any(word in jokes_in for word in the_message):
        return json.dumps({"animation": "laughing", "msg": choice(jokes)})
    elif any(word in curses for word in the_message):
        return curses_func(the_message)
    elif user_message[-1] == "?":
        return json.dumps({"animation": "confused", "msg": choice(question_answer)})
    else:
        return json.dumps({"animation": choice(reactions), "msg": "I don't know a lot about "+user_message+", tomorrow we can talk about"})

def animals_func(the_message):
    if animals[0] in the_message or animals[1] in the_message:
        return json.dumps({"animation": "dog", "msg": "Dogs are my favorite animals, that's Snoop Bot my best friend"})
    if animals[2] in the_message or animals[3] in the_message:
        return json.dumps({"animation": "no", "msg": "I hate cats"})
    else:
        return json.dumps({"animation": choice(reactions), "msg": "animals"})


def love_func(the_message):
    if any(word in animals for word in the_message):
        return json.dumps({"animation": "dog", "msg": "I love animals"})
    else:
        return json.dumps({"animation": "love", "msg": "Love love"})

def curses_func(the_message):
    if "go" in the_message:
        return json.dumps({"animation": "no", "msg": "NO! GO YOU!"})
    else:
        return json.dumps({"animation": choice(reactions), "msg": choice(curses_answer)})


@route("/test", method='POST')
def chat():
    user_message = request.POST.get('msg')
    return json.dumps({"animation": "inlove", "msg": user_message})


@route('/js/<filename:re:.*\.js>', method='GET')
def javascripts(filename):
    return static_file(filename, root='js')


@route('/css/<filename:re:.*\.css>', method='GET')
def stylesheets(filename):
    return static_file(filename, root='css')


@route('/images/<filename:re:.*\.(jpg|png|gif|ico)>', method='GET')
def images(filename):
    return static_file(filename, root='images')


def main():
    run(host='localhost', port=7000)

if __name__ == '__main__':
    main()
