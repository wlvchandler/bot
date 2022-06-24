import json
import hmac
import hashlib
import flask
from flask import Flask, request, Response
from flask_sock import Sock
app = Flask(__name__)
app.config['SOCK_SERVER_OPTIONS'] = {'ping_interval': 25}
sock = Sock(app)


@sock.route('/echo')
def echo(ws):
    while True:
        data = ws.receive()
        if data == 'close':
            break
        ws.send(data)

def handle_channel_follow(event):
    with open('/home/will/chatthew/followed', 'a') as f:
        f.write(f'{event["user_name"]} has followed\n')

def handle_channel_update(event):
    with open('/home/will/chatthew/channel_update', 'a') as f:
        f.write(f'category now {event["category_name"]}\n')

def handle_channel_point_redeem(event):
    with open('/home/will/chatthew/point_redeem', 'a') as f:
        f.write(f'{event["user_name"]} redeemed {event["reward"]["title"]} ({event["user_input"]})\n')

def handle_sub(event):
    pass

def handle_gifted_sub(event):
    pass

def handle_sub_message(event):
    pass

def handle_cheer(event):
    with open('/home/will/chatthew/cheers', 'a') as f:
        name = event["user_name"]
        if event["is_anonymous"] == True:
            name = "anonymous"
        f.write(f'{name} cheered {event["bits"]} bits: \'{event["message"]}\'\n')

def handle_hype_train_begin(event):
    pass

def handle_hype_train_progress(event):
    pass

def handle_hype_train_end(event):
    pass


event_handler = {
    "channel.follow": handle_channel_follow,
    "channel.update": handle_channel_update,
    "channel.channel_points_custom_reward_redemption.add" : handle_channel_point_redeem,
    "channel.subscribe" : handle_sub,
    "channel.subscription.gift" : handle_gifted_sub,
    "channel.subscription.message" : handle_sub_message,
    "channel.cheer" : handle_cheer,
    "channel.hype_train.begin" : handle_hype_train_begin,
    "channel.hype_train.progress" : handle_hype_train_progress,
    "channel.hype_train.end" : handle_hype_train_end
}
    
def handle_notification(rjson):
    event_handler[rjson["subscription"]["type"]](rjson["event"])

def debug_out(request):
    with open('/home/will/chatthew/callback-out', 'a') as f:
        f.write("received callback\n")
        f.write("DATA:\n===================\n")
        f.write(json.dumps(request.json))
        f.write("\nHEADERS:\n===================\n")
        f.write(f'{request.headers}\n')
        f.write("===================\n")

@app.route("/webhooks/twitch-callback", methods=['POST','GET'])
def twitchCallback():
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


@app.route("/blessed")
def blessed():
    return "camyo - 1\nalba - 1"
    #return "<p>camyo - 1</p><p>alba - 1</p>"

@app.route("/test")
def testshit():
    id = flask.request.args.get('button_id')
    return f'<p>{id}</p>'
    #return '<h1 style="color:white">hi hi hi hi hi hi hi hi hi hi hi hi hi</h1>', 200

@app.route("/", methods=['GET','POST'])
def hello():
    return flask.render_template('blurse.html')
    #return "<h1 style='color:blue'>Hello world >:)</h1>"


if __name__ == "__main__":
    app.run(host='0.0.0.0')
