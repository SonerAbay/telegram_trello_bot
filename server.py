from bot import telegram_chatbot
import sunny
from threading import Timer
import json

bot = telegram_chatbot("config.cfg")


def make_reply(msg, item):
    reply = None
    if msg is not None:
        reply = sunny.text(msg, item)
    return reply

def welcome_user(item):

    # creating different messages for responser type
    group_id = str(item["message"]["chat"]["id"])
    if "username" in item["message"]["new_chat_members"][0]:
        new_user = item["message"]["new_chat_members"][0]["username"]
        message = "<b>WAIT!</b> @{}\nhttps://i.pinimg.com/474x/1b/ba/4b/1bba4b617111f57095911b2317542c35--philadelphia.jpg".format(new_user)
    else:
        message = "<b>WAIT!</b>\nhttps://i.pinimg.com/474x/1b/ba/4b/1bba4b617111f57095911b2317542c35--philadelphia.jpg"

    bot.send_message(message, group_id)
    t1 = Timer(7, bot.send_message, ("Okay you are clear. Welcome to the group!", group_id))
    t2 = Timer(3, bot.send_message, (".........", group_id))
    t1.start()
    t2.start()

def speed_user(item):

    # it will send it both to the group and the user
    user_id = str(item["message"]["left_chat_participant"]["id"])
    group_id = str(item["message"]["chat"]["id"])
    message = "https://media.giphy.com/media/BLvZWddnwvcwE/giphy.gif"
    bot.send_message(message, group_id)
    bot.send_message(message, user_id)


def user_update(item):

    if "text" in item["message"].keys():
        message = str(item["message"]["text"].encode('utf-8'))
        from_ = item["message"]["from"]["id"]
        print(from_)
        reply = make_reply(message, item)
        bot.send_message(reply, from_)

        if 'new_chat_members' in item["message"]:
            welcome_user(item)

def group_update(item):

    if "text" in item["message"].keys():
        message = str(item["message"]["text"].encode('utf-8'))
        group_id = str(item["message"]["chat"]["id"])
        reply = make_reply(message, item)
        bot.send_message(reply, group_id)

    elif 'new_chat_participant' in item["message"].keys():
        welcome_user(item) 
    elif 'left_chat_participant' in item["message"].keys():
        speed_user(item)


def channel_update(item):
    if "text" in item["channel_post"].keys():
        message = str(item["channel_post"]["text"].encode('utf-8'))
        reply = make_reply(message, item)
        channel_id = '@' + str(item["channel_post"]["chat"]["username"])
        bot.send_message(reply, channel_id)

update_id = None
while True:
    updates = bot.get_updates(offset=update_id)
    updates = updates["result"]
    if updates:
        for item in updates:
            update_id = item["update_id"]
            if "message" in item.keys() and item["message"]["chat"]["type"] == "private":
                    user_update(item)
            elif 'channel_post' in item.keys():
                channel_update(item)
            elif "message" in item.keys() and item["message"]["chat"]["type"] == "group":
                group_update(item)

            else:
                print("Non-message")
