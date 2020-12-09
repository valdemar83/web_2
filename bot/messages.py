import telebot
import redis

handle = open("token.txt", "r")
token = handle.readline()
r = redis.Redis(host='127.0.0.1', port=6379)
bot = telebot.TeleBot(token)


#for getting from redis
#r.get('IP').decode("utf-8")   

#for sending messages
#bot.send_message(IP, 'message')




