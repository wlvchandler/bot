import json
import hmac
import hashlib
import time
import datetime
import uuid

import os
from dotenv import load_dotenv
load_dotenv()

## LOGGING SETUP
import logging
logging.basicConfig(format='%(asctime)s %(message)s', filename='log/chatthew.log', encoding='utf-8', level=logging.DEBUG)

## DB SETUP
import mariadb
ENV=os.environ
conn = mariadb.connect(user=ENV["DBUSER"], password=ENV["DBPW"], host="127.0.0.1", port=3306, database=ENV["DB"], autocommit=True)
dbcur = conn.cursor()

## FLASK SETUP
import flask
from flask import Flask, request, Response
from flask_sock import Sock
app = Flask(__name__)
app.config['SOCK_SERVER_OPTIONS'] = {'ping_interval': 25}
sock = Sock(app)


################################################################

def GetTimestamp(fmt='%Y-%m-%d %H:%M:%S'):
    return datetime.datetime.fromtimestamp(time.time()).strftime(fmt)    




###################
##### EVENTSUB HANDLERS
###################

def handle_channel_follow(event):
    eUserId     = event["user_id"]
    eUserLogin  = event["user_login"]
    eUserName   = event["user_name"]
    eBId        = event["broadcaster_user_id"]
    eBUserLogin = event["broadcaster_user_login"]
    eBUserName  = event["broadcaster_user_name"]
    eFollowTime = event["followed_at"]
    with open('/home/will/chatthew/followed', 'a') as f:
        f.write(f'{event["user_name"]} has followed\n')

def handle_channel_update(event):
    eBId          = event["broadcaster_user_id"]
    eBUserLogin   = event["broadcaster_user_login"]
    eBUserName    = event["broadcaster_user_name"]
    eTitle        = event["title"]
    eLanguage     = event["language"]
    eCategoryId   = event["category_id"]
    eCategoryName = event["category_name"]
    eMature       = event["is_mature"]
    timestamp = GetTimestamp()
    user = 'jaahska' 
    query=f"insert into alerts (alert_type, timestamp, user) values ('channel_update','{timestamp}','{user}')"
    dbcur.execute(query)

point_redeems = {
    uuid.UUID('278846c3-d03b-4a2d-8956-1eae210b4326'): "Sound Alert: mr magoo",
    uuid.UUID('188d0260-c5eb-4bcb-8a9c-822b5199a8d4'): "Curse The Run",
    uuid.UUID('4dc8e700-e1c2-4a6c-bafd-71481a4d29be'): "Sound Alert: Dark Souls - Hello",
    uuid.UUID('600d05c6-c9ca-452b-b78a-c23dce0c1358'): "Sound Alert: Dark Souls - Very Good",
    uuid.UUID('185a5cf0-295d-474f-a514-732795b086d9'): "Say Something",
    uuid.UUID('47a3b68f-dffe-41d6-bed1-03d9bc8e01fb'): "Curse the Run (Audio)",
    uuid.UUID('60fa0174-6c07-425e-a68b-d66b5bdcc974'): "Bless The Run",
    uuid.UUID('9d20f66c-f6f4-4390-80b9-2fb6f1de97c3'): "Bless the Run (Audio)",
    uuid.UUID('bab9e1de-7330-4cc3-8295-31b2ba20319f'): "IRL word ban",
    uuid.UUID('52e75172-c31b-4e56-8a33-acb5f88ac212'): "No cursing",
    uuid.UUID('36e904c8-9e40-4f54-b7a3-656d5316e607'): "name the next character",
    uuid.UUID('5ab4b396-c848-4b66-a103-5e19ff1e963d'): "Song request",
    uuid.UUID('83fd2cce-fe17-44b2-af92-42121371514a'): "rename a split",
    uuid.UUID('54f8ab39-5eeb-48db-89a1-4c46e18317cd'): "Ban an in-game action (1 minute)"
}
def handle_channel_point_redeem(event):
    eId         = event["id"]
    eUserId     = event["user_id"]
    eUserLogin  = event["user_login"]
    eUserName   = event["user_name"]
    eUserInput  = event["user_input"]
    eBUserId    = event["broadcaster_user_id"]
    eBUserLogin = event["broadcaster_user_login"]
    eBUserName  = event["broadcaster_user_name"]
    eStatus     = event["status"]
    eRedeemedAt = event["redeemed_at"]
    eRwdId      = uuid.UUID(event["reward"]["id"])
    eRwdTitle   = event["reward"]["title"]
    eRwdCost    = event["reward"]["cost"]
    eRwdPrompt  = event["reward"]["prompt"]

    #TODO: insert redeem into tables for future
    
    with open('/home/will/chatthew/point_redeem', 'a') as f:
        #f.write(f'{eUserName} redeemed {eRwdTitle} ({eRwdId}{type(eRwdId)}): "{eUserInput}"\n')
        f.write(f'uuid.UUID(\'{eRwdId}\'): "{eRwdTitle}"\n')
        
    query = ''
    if eRwdTitle.split()[0].lower() in ['curse', 'bless']:
        t = eRwdTitle.split()[0]
        query = f"insert into blurse (type, user) values ('{t}', '{eUserName}')"
        
    if query != '':
        print(f"executing '{query}'")
        dbcur.execute(query)

def handle_sub(event):
    eUserId     = event["user_id"]
    eUserLogin  = event["user_login"]
    eUserName   = event["user_name"]
    eBUserId    = event["broadcaster_user_id"]
    eBUserLogin = event["broadcaster_user_login"]
    eBUserName  = event["broadcaster_user_name"]
    eTier       = event["tier"]
    eGift       = event["is_gift"]

def handle_gifted_sub(event):
    eUserId     = event["user_id"]
    eUserLogin  = event["user_login"]
    eUserName   = event["user_name"]
    eBUserId    = event["broadcaster_user_id"]
    eBUserLogin = event["broadcaster_user_login"]
    eBUserName  = event["broadcaster_user_name"]
    eTier       = event["tier"]
    eTotal      = event["total"]
    eCumulative = event["cumulative_total"]
    eAnon       = event["is_anonymous"]
    
def handle_sub_message(event):
    eUserId     = event["user_id"]
    eUserLogin  = event["user_login"]
    eUserName   = event["user_name"]
    eBUserId    = event["broadcaster_user_id"]
    eBUserLogin = event["broadcaster_user_login"]
    eBUserName  = event["broadcaster_user_name"]
    eTier       = event["tier"]
    eCumulative = event["cumulative_months"]
    eStreak     = event["streak_months"]
    eDuration   = event["duration_months"]
    eMessage    = event["message"]
    eMsgText    = eMessage["text"]
    eEmotes     = eMessage["emotes"] # [{begin, end, id},..]

def handle_cheer(event):
    eAnon       = event["is_anonymous"]
    eUserId     = 0 if eAnon else event["user_id"]
    eUserLogin  = 'Anonymous' if eAnon else event["user_login"]
    eUserName   = 'Anonymous' if eAnon else event["user_name"]
    eBUserId    = event["broadcaster_user_id"]
    eBUserLogin = event["broadcaster_user_login"]
    eBUserName  = event["broadcaster_user_name"]
    eMessage    = event["message"]
    eBits       = event["bits"]

    event_id = 0 #TODO generate unique id -- or autoinc
    query = f"insert into cheers (id, amount, user, channel) values ('{event_id}', '{eBits}', '{eUserName}', '{eBUserName}')"
    dbcur.execute(query)
    
def handle_hype_train_begin(event):
    pass

def handle_hype_train_progress(event):
    pass

def handle_hype_train_end(event):
    pass

def handle_stream_online(event):
    #session_id = uuid.uuid1()
    eId = event["id"]
    eBUserId = event["broadcaster_user_id"]
    eBUserLogin = event["broadcaster_user_login"]
    eBUserName = event["broadcaster_user_name"]
    eType = event["type"] # live, playlist, watch_party, premiere, rerun
    eTime = event["started_at"]
    eTimeConv = datetime.datetime.strptime(eTime, "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y-%m-%d %H:%M:%S.%f")
    query = f"insert into stream (start_time, end_time, messages) values ({eTimeConv}, NULL, 0)"
    dbcur.execute(query)
    
def handle_stream_offline(event):
    eUserId = event["broadcaster_user_id"]
    eUserLogin = event["broadcaster_user_login"]
    eUserName = event["broadcaster_user_name"]

def handle_raid(event):
    eRaiderId    = event["from_broadcaster_user_id"]
    eRaiderLogin = event["from_broadcaster_user_login"]
    eRaiderName  = event["from_broadcaster_user_name"]
    eBUserId     = event["to_broadcaster_user_id"]
    eBUserLogin  = event["to_broadcaster_user_login"]
    eBUserName   = event["to_broadcaster_user_name"]
    eViewers     = event["viewers"]

def handle_ban(event):
    eUserId     = event["user_id"]
    eUserLogin  = event["user_login"]
    eUserName   = event["user_name"]
    eBUserId    = event["broadcaster_user_id"]
    eBUserLogin = event["broadcaster_user_login"]
    eBUserName  = event["broadcaster_user_name"]
    eModId      = event["moderator_user_id"]
    eModLogin   = event["moderator_user_login"]
    eModName    = event["moderator_user_name"]
    eReason     = event["reason"]
    eBannedAt   = event["banned_at"]
    eEndsAt     = event["ends_at"]
    ePermanent  = event["is_permanent"]
    
event_handler = {
    "channel.follow": handle_channel_follow,
    "channel.update": handle_channel_update,
    "channel.channel_points_custom_reward_redemption.add" : handle_channel_point_redeem,
    "channel.subscribe" : handle_sub,
    "channel.subscription.gift" : handle_gifted_sub,
    "channel.subscription.message" : handle_sub_message,
    "channel.cheer" : handle_cheer,
    "channel.raid" : handle_raid,
    "channel.ban" : handle_ban,
    "channel.hype_train.begin" : handle_hype_train_begin,
    "channel.hype_train.progress" : handle_hype_train_progress,
    "channel.hype_train.end" : handle_hype_train_end,
    "stream.online": handle_stream_online,
    "stream.offline": handle_stream_offline
}
    

##################
#### EXTERNAL EVENT HANDLER
##################

def handle_notification(rjson):
    logging.info(f'chatthew_event {rjson["subscription"]["type"]}')
    event_handler[rjson["subscription"]["type"]](rjson["event"])

    
@app.route("/webhooks/twitch-callback", methods=['POST','GET'])
def twitchCallback():
    def debug_out(request):
        with open('/home/will/chatthew/callback-out', 'a') as f:
            f.write("received callback\n")
            f.write("DATA:\n===================\n")
            f.write(json.dumps(request.json))
            f.write("\nHEADERS:\n===================\n")
            f.write(f'{request.headers}\n')
            f.write("===================\n")

    # debug_out(request)
    ret = 'Bad', 403
    secret = "blahblahblahblah"
    message = f'{request.headers["Twitch-Eventsub-Message-Id"]}{request.headers["Twitch-Eventsub-Message-Timestamp"]}{request.data.decode("utf-8")}'
    calculated_sig = 'sha256='+hmac.new(str.encode(secret,'utf-8'),msg=str.encode(message,'utf-8'),digestmod=hashlib.sha256).hexdigest()
    sig = request.headers["Twitch-Eventsub-Message-Signature"]
    if calculated_sig == sig or request.headers["Debug"] == "True":
        ret = 'Ok', 200
        if "challenge" in request.json.keys():
            ret = f'{request.json["challenge"]}'
    if request.headers["Twitch-Eventsub-Message-Type"] == "notification":
        handle_notification(request.json)
    return ret



##############
#### STATIC PAGES
##############

def sort_blurse(blurse):
    D = {}
    dbcur.execute(f'select * from blurse where type ="{blurse}"')
    for r in dbcur:
        if r[1] not in D.keys():
            D[r[1]] = 1
        else:
            D[r[1]] += 1
    return [f'{y[1]} - {y[0]}' for y in sorted(D.items(), key=lambda x: x[1], reverse=True)]
   
    
@app.route("/blessed")
def blessed():
    return flask.render_template('blurses.html', blursers="Blessers", blurses=sort_blurse('bless'))

@app.route("/cursed")
def cursed():
    return flask.render_template('blurses.html', blursers="Cursers", blurses=sort_blurse('curse'))
    #return flask.render_template('cursed.html', curses=sort_blurse('curse'))

@app.route("/canvas" ''', methods=['GET', 'POST']''')
def canvas():
    return flask.render_template("canvas.html")



if __name__ == "__main__":
    app.run(host='0.0.0.0')
