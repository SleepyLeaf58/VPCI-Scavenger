from flask import *
import random
import google.generativeai as genai
import os
from dotenv import load_dotenv
import time

from Object import *

app = Flask(__name__)

load_dotenv()

genai.configure(api_key=os.environ['API_KEY'])
model = genai.GenerativeModel("gemini-1.5-flash")

hunts = {}  # store hunts and items
players = {}  # store players and their progress

# Route for Home Page
@app.route("/")
def home():
    return render_template("index.html")

# Route for organizers to start a hunt
@app.route("/start-hunt", methods=['POST'])
def start_hunt():
    hunt_name = request.form['roomName']
    organizer = request.form['org']
    riddle1 = request.form['riddle1']
    riddle2 = request.form['riddle2']
    riddle3 = request.form['riddle3']
    room1 = request.form['room1']
    room2 = request.form['room2']
    room3 = request.form['room3']
    code1 = request.form['code1']
    code2 = request.form['code2']
    code3 = request.form['code3']

    object1 = Object(request.form['riddle1'], request.form['room1'], request.form['code1'])
    object2 = Object(request.form['riddle2'], request.form['room2'], request.form['code2'])
    object3 = Object(request.form['riddle3'], request.form['room3'], request.form['code3'])

    hunt_id = random.randint(1000, 9999)

    def generate_riddle(object):
        response = model.generate_content(f"You are an AI assistant helping a game organizer create riddles to hide objects within a room. Given a description of the object and its location, generate a concise and specific riddle (around 20-25 words). Emphasize the object's distinctive features and its exact location, ensuring the riddle clearly directs players to the item. Make sure the clues are specific and unambiguous. Absolutely do not say the object in question. The object description given is {object.getRiddle()}")
        return response.text        

    object1.setRiddle(generate_riddle(object1))
    object2.setRiddle(generate_riddle(object2))
    object3.setRiddle(generate_riddle(object3))

    hunts[hunt_id] = {
        'hunt_name': hunt_name,
        'organizer': organizer,
        'objects': [
            object1, object2, object3
        ],
        'players': []
    }
    return render_template("hunt-reveal.html", hunt_name=hunt_name, hunt_id=hunt_id)

# Route for players to join a hunt
@app.route("/join-hunt", methods=["POST"])
def join_hunt():
    hunt_id = int(request.form["idd"])
    name = request.form["name"]
    if hunt_id in hunts:
        player_id = random.randint(1000, 9999)
        player = {'name': name, 'current_object': 0, 'start_time': time.time(), 'current_time': time.time(), 'finished': False}
        hunts[hunt_id]['players'].append(player_id)
        players[player_id] = player
        return render_template("save-local.html", player_id=player_id, hunt_id=hunt_id)
    else:
        return render_template("error.html", error="This hunt does not exist.")

@app.route("/current-riddle", methods=["POST"])
def current_riddle():
    player_id = request.form["player_id"]
    hunt_id = int(request.form["hunt_id"])
    player = players.get(int(player_id))
    if player:
        next_hint = hunts[hunt_id]['objects'][player['current_object']].getRiddle()
        next_room = hunts[hunt_id]['objects'][player['current_object']].getRoom()
        return render_template("player-dashboard.html", riddle=next_hint, room=next_room, obj=player['current_object'], player_id=player_id, hunt_id=hunt_id)
    else:
        return render_template("error.html", error="Player not found.")

@app.route("/join-game")
def join_game_page():
    return render_template("join-game.html")

@app.route("/create-game")
def create_game_page():
    return render_template("create-game.html")

@app.route("/current-riddle/<player>/<hunt>", methods=["GET"])
def current_riddle_get(player, hunt):
    player_id = int(player)
    hunt_id = int(hunt)
    player = players.get(player_id)
    if player:
        next_hint = hunts[hunt_id]['objects'][player['current_object']].getRiddle()
        next_room = hunts[hunt_id]['objects'][player['current_object']].getRoom()
        return render_template("player-dashboard.html", riddle=next_hint, room=next_room, obj=player['current_object'], player_id=player_id, hunt_id=hunt_id)
    else:
        return render_template("error.html", error="Player not found or invalid hunt ID.")

# Route for players to submit found item codes
@app.route("/submit-item", methods=['POST'])
def submit_item():
    player_id = int(request.form["player-id"])
    hunt_id = int(request.form["hunt-id"])
    code = str(request.form["code"])

    player = players.get(player_id)
    if not player:
        return render_template("error.html", error="Invalid player.")

    if hunt_id not in hunts:
        return render_template("error.html", error="Invalid hunt ID.")

    current_object_idx = player['current_object']
    correct_code = str(hunts[hunt_id]['objects'][current_object_idx].getCode())

    if player['finished']:
        return render_template("error.html", error="You have already finished the hunt!")

    if code == correct_code:
        player['current_object'] += 1
        player['current_time'] = time.time()
        if player['current_object'] < len(hunts[hunt_id]['objects']):
            return redirect(f"/current-riddle/{player_id}/{hunt_id}")
        else:
            player['finished'] = True
            return redirect(f"/finish/{player_id}/{hunt_id}")
    else:
        return render_template("error.html", error="Incorrect code.")

# Route to check leaderboard or see who finished first
@app.route("/leaderboard/<int:hunt_id>", methods=['GET'])
def leaderboard(hunt_id):
    if hunt_id in hunts:
        names, scores = [], []
        for player_id in hunts[hunt_id]['players']:
            pl = players.get(player_id)
            if pl:
                name = pl["name"]
                score = pl["current_object"]
                names.append(name)
                scores.append(score)

        sorted_pairs = sorted(zip(scores, names), reverse=True)
        sorted_scores, sorted_names = zip(*sorted_pairs) if sorted_pairs else ([], [])
        sorted_scores = list(sorted_scores)
        sorted_names = list(sorted_names)

        return render_template("leaderboard.html", names=sorted_names, scores=sorted_scores)
    else:
        return render_template("error.html", error="Hunt not found.")

# Route for finishing
@app.route("/finish/<player>/<hunt>", methods=["GET"])
def finish_game(player, hunt):
    player_id = int(player)
    hunt_id = int(hunt)
    player = players.get(player_id)

    if player and player['finished']:
        player_time = player['current_time']
        rank = 1
        for participant in hunts[hunt_id]['players']:
            pl = players.get(participant)
            if pl and pl['finished'] and pl['current_time'] < player_time:
                rank += 1

        total_seconds = round(player['current_time'] - player['start_time'])
        hours = total_seconds // 3600
        total_seconds %= 3600
        minutes = total_seconds // 60
        total_seconds %= 60
        seconds = total_seconds
        return render_template("finish.html", name=player['name'], rk=rank, hrs=hours, mins=minutes, secs=seconds)
    else:
        return render_template("error.html", error="Unfinished hunt or player not found.")

if __name__ == '__main__':
    app.run(debug=True)
