from flask import *
import random

app = Flask(__name__)

hunts = {}  # store hunts and items
players = {}  # store players and their progress

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
    hunts[hunt_id] = {
        'hunt_name': hunt_name,
        'organizer': organizer,
        'objects': [{"riddle":riddle1, "room":room1, "code": code1}, {"riddle":riddle2, "room":room2, "code": code2}, {"riddle":riddle3, "room":room3, "code": code3}],  # list of items with room, riddle,code
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
        player = {'name': name, 'current_object': 0, 'finished': False}
        hunts[hunt_id]['players'].append(player_id)
        players[player_id] = player
        first_hint = hunts[hunt_id]['objects'][0]['riddle']
        first_room = hunts[hunt_id]['objects'][0]['room']
        return render_template("save-local.html", player_id=player_id)
    else:
        return jsonify({"error": "This hunt is over."}), 404

@app.route("/current-riddle", methods=["POST"])
def current_riddle():
    player_id = request.form["player_id"]
    player = players[player_id]
    next_hint = hunts[hunt_id]['objects'][player['current_object']]['riddle']
    next_room = hunts[hunt_id]['objects'][player['current_object']]['room']
    return render_template("player-dashboard.html", riddle=next_hint, room=next_room, obj=player['current_object'])

# Route for players to submit found item codes
@app.route("/submit-item", methods=['POST'])
def submit_item():
    data = request.json
    player_id = data['player_id']
    hunt_id = data['hunt_id']
    code = data['code']
    
    if player_id in players and hunt_id in hunts:
        player = players[player_id]
        current_object_idx = player['current_object']
        if player['finished']:
            return jsonify({"message": "You have already finished the hunt!"})
        
        correct_code = hunts[hunt_id]['objects'][current_object_idx]['code']
        
        if code == correct_code:
            player['current_object'] += 1
            if player['current_object'] < len(hunts[hunt_id]['objects']):
                next_hint = hunts[hunt_id]['objects'][player['current_object']]['riddle']
                next_room = hunts[hunt_id]['objects'][player['current_object']]['room']
                return jsonify({"message": "Correct! Move to the next item", "next_hint": next_hint, "next_room": next_room})
            else:
                player['finished'] = True
                return jsonify({"message": f"Congratulations {player['name']}! You've found all the items and completed the hunt!"})
        else:
            return jsonify({"error": "Incorrect code"}), 400
    else:
        return jsonify({"error": "Invalid player or hunt"}), 404

# Route to check leaderboard or see who finished first
@app.route("/leaderboard/<int:hunt_id>", methods=['GET'])
def leaderboard(hunt_id):
    if hunt_id in hunts:
        finished_players = [player_id for player_id in hunts[hunt_id]['players'] if players[player_id]['finished']]
        if finished_players:
            winner = players[finished_players[0]]['name']  # The first player to finish
            return jsonify({"message": f"{winner} has won the hunt!"})
        else:
            return jsonify({"message": "No one has completed the hunt yet."})
    else:
        return jsonify({"error": "Hunt not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
