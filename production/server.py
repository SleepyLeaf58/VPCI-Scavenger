from flask import *
import random
from groq import Groq
import time

app = Flask(__name__)

client = Groq(
    api_key="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",
)

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
    hunt_id = random.randint(1000, 9999)
    riddle_1 = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content":
"You are an AI assistant helping a game organizer create riddles to hide objects within a room. Given a description of the object and its location, generate a concise and specific riddle (around 20-25 words). Emphasize the object's distinctive features and its exact location, ensuring the riddle clearly directs players to the item. Make sure the clues are specific and unambiguous. Absolutely do not say the object in question."
        },

        {
            "role": "user",
            "content": riddle1,
        }
    ],
    model="llama3-groq-70b-8192-tool-use-preview",
    ).choices[0].message.content
    riddle_2 = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content":
"You are an AI assistant helping a game organizer create riddles to hide objects within a room. Given a description of the object and its location, generate a concise and specific riddle (around 20-25 words). Emphasize the object's distinctive features and its exact location, ensuring the riddle clearly directs players to the item. Make sure the clues are specific and unambiguous. Absolutely do not say the object in question."
        },

        {
            "role": "user",
            "content": riddle2,
        }
    ],
    model="llama3-groq-70b-8192-tool-use-preview",
    ).choices[0].message.content
    riddle_3 = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content":
"You are an AI assistant helping a game organizer create riddles to hide objects within a room. Given a description of the object and its location, generate a concise and specific riddle (around 20-25 words). Emphasize the object's distinctive features and its exact location, ensuring the riddle clearly directs players to the item. Make sure the clues are specific and unambiguous. Absolutely do not say the object in question."
        },

        {
            "role": "user",
            "content": riddle3,
        }
    ],
    model="llama3-groq-70b-8192-tool-use-preview",
    ).choices[0].message.content
    hunts[hunt_id] = {
        'hunt_name': hunt_name,
        'organizer': organizer,
        'objects': [{"riddle":riddle_1, "room":room1, "code": code1}, {"riddle":riddle_2, "room":room2, "code": code2}, {"riddle":riddle_3, "room":room3, "code": code3}],  # list of items with room, riddle,code
        'players': []
    }
    return f"Hunt with name {hunt_name} created! The id for this hunt is {hunt_id}"

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
        first_hint = hunts[hunt_id]['objects'][0]['riddle']
        first_room = hunts[hunt_id]['objects'][0]['room']
        return render_template("save-local.html", player_id=player_id, hunt_id=hunt_id)
    else:
        return jsonify({"error": "This hunt is over."}), 404

@app.route("/current-riddle", methods=["POST"])
def current_riddle():
    player_id = request.form["player_id"]
    hunt_id = int(request.form["hunt_id"])
    player = players[int(player_id)]
    next_hint = hunts[hunt_id]['objects'][player['current_object']]['riddle']
    next_room = hunts[hunt_id]['objects'][player['current_object']]['room']
    return render_template("player-dashboard.html", riddle=next_hint, room=next_room, obj=player['current_object'], player_id=player_id, hunt_id=hunt_id)
    
@app.route("/join-game")
def join_game_page():
    return render_template("join-game.html")

@app.route("/create-game")
def create_game_page():
    return render_template("create_game.html")
    
@app.route("/current-riddle/<player>/<hunt>", methods=["GET"])
def current_riddle_get(player, hunt):
    player_id = player
    hunt_id = int(hunt)
    player = players[int(player_id)]
    next_hint = hunts[hunt_id]['objects'][player['current_object']]['riddle']
    next_room = hunts[hunt_id]['objects'][player['current_object']]['room']
    return render_template("player-dashboard.html", riddle=next_hint, room=next_room, obj=player['current_object'], player_id=player_id, hunt_id=hunt_id)

# Route for players to submit found item codes
@app.route("/submit-item", methods=['POST'])
def submit_item():
    player_id = int(request.form["player-id"])
    hunt_id = int(request.form["hunt-id"])
    code = str(request.form["code"])
    
    if player_id in players and hunt_id in hunts:
        player = players[int(player_id)]
        current_object_idx = player['current_object']
        if player['finished']:
            return jsonify({"message": "You have already finished the hunt!"})
        
        correct_code = str(hunts[hunt_id]['objects'][current_object_idx]['code'])
        
        if code == correct_code:
            player['current_object'] += 1
            player['current_time'] = time.time()
            if player['current_object'] < len(hunts[hunt_id]['objects']):
                next_hint = hunts[hunt_id]['objects'][player['current_object']]['riddle']
                next_room = hunts[hunt_id]['objects'][player['current_object']]['room']
                return redirect(f"/current-riddle/{player_id}/{hunt_id}")
            else:
                player['finished'] = True
                total_seconds = round(player['current_time']-player['start_time'])
                return redirect(f"/finish/{player_id}/{hunt_id}")
                # hours = total_seconds // 3600
                # total_seconds %= 3600
                # minutes = total_seconds // 60
                # total_seconds %= 60
                # seconds = total_seconds
                # return jsonify({"message": f"Congratulations {player['name']}! You've found all the items and completed the hunt in {hours} hours, {minutes} minutes, and {seconds} seconds!"})
        else:
            return jsonify({"error": "Incorrect code"}), 400
    else:
        return jsonify({"error": "Invalid player or hunt"}), 404
# Route to check leaderboard or see who finished first
@app.route("/leaderboard/<int:hunt_id>", methods=['GET'])
def leaderboard(hunt_id):
    if hunt_id in hunts:
        names, scores = [], []
        for player in hunts[hunt_id]['players']:
            # player is an id here
            pl = players[int(player)]
            name = pl["name"]
            score = pl["current_object"]
            names.append(name)
            scores.append(score)
        
        sorted_pairs = sorted(zip(scores, names), reverse=True)
        sorted_scores, sorted_names = zip(*sorted_pairs)
        sorted_scores = list(sorted_scores)
        sorted_names = list(sorted_names)

        # Pass the data to the HTML template
        return render_template("leaderboard.html", names=sorted_names, scores=sorted_scores)
    else:
        return jsonify({"error": "Hunt not found"}), 404

# Route for finishing
# Route for players to submit found item codes
@app.route("/finish/<player>/<hunt>", methods=["GET"])
def finish_game(player, hunt):
    player_id = player
    hunt_id = int(hunt)
    player = players[int(player_id)]

    player_time = player['current_time']
    print(player)

    rank = 1
    for participant in hunts[hunt_id]['players']:
        # player is an id here
        pl = players[int(participant)]
        if (pl['finished'] and pl['current_time'] < player_time): 
            rank += 1
    
    if player['finished']:
        total_seconds = round(player['current_time']-player['start_time'])
        hours = total_seconds // 3600
        total_seconds %= 3600
        minutes = total_seconds // 60
        total_seconds %= 60
        seconds = total_seconds
        return render_template("finish.html", name=player['name'], rk=rank,  hrs=hours, mins=minutes, secs=seconds)
    else:
        return jsonify({"error": "Unfinished hunt"}), 400

if __name__ == '__main__':
    app.run(debug=True)