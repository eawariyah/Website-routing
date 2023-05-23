from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

# set directory for json files
json_dir = os.getcwd()

# create a dictionary to store voter and election data
voters = {}
elections = {}

# route to register a new voter
@app.route('/voters', methods=['POST'])
def register_voter():
    voter_data = request.get_json()
    voter_id = len(voters) + 1
    voter_data["id"] = voter_id
    voters[voter_id] = voter_data
    # save voter data to json file
    voter_file = os.path.join(json_dir, f"voter_{voter_id}.txt")
    with open(voter_file, "w") as f:
        json.dump(voter_data, f)
    return jsonify({'message': 'New voter registered successfully', 'voter_id': voter_id})

# route to deregister a voter
@app.route('/voters/<int:voter_id>', methods=['DELETE'])
def deregister_voter(voter_id):
    if voter_id in voters:
        del voters[voter_id]
        # delete voter data json file
        voter_file = os.path.join(json_dir, f"voter_{voter_id}.txt")
        os.remove(voter_file)
        return jsonify({'message': 'Voter deregistered successfully'})
    else:
        return jsonify({'error': 'Voter not found'})

# route to update voter information
@app.route('/voters/<int:voter_id>', methods=['PUT'])
def update_voter(voter_id):
    if voter_id in voters:
        voter_data = request.get_json()
        voters[voter_id].update(voter_data)
        # save updated voter data to json file
        voter_file = os.path.join(json_dir, f"voter_{voter_id}.txt")
        with open(voter_file, "w") as f:
            json.dump(voters[voter_id], f)
        return jsonify({'message': 'Voter information updated successfully'})
    else:
        return jsonify({'error': 'Voter not found'})

# route to get voter information
@app.route('/voters/<int:voter_id>', methods=['GET'])
def get_voter(voter_id):
    if voter_id in voters:
        return jsonify(voters[voter_id])
    else:
        return jsonify({'error': 'Voter not found'})

# route to create a new election
@app.route('/elections', methods=['POST'])
def create_election():
    election_data = request.get_json()
    election_id = len(elections) + 1
    election_data["id"] = election_id
    elections[election_id] = election_data
    # save election data to json file
    election_file = os.path.join(json_dir, f"election_{election_id}.txt")
    with open(election_file, "w") as f:
        json.dump(election_data, f)
    return jsonify({'message': 'New election created successfully', 'election_id': election_id})

# route to get election information
@app.route('/elections/<int:election_id>', methods=['GET'])
def get_election(election_id):
    if election_id in elections:
        return jsonify(elections[election_id])
    else:
        return jsonify({'error': 'Election not found'})

# route to delete an election
@app.route('/elections/<int:election_id>', methods=['DELETE'])
def delete_election(election_id):
    if election_id in elections:
        del elections[election_id]
        # delete election data json file
        election_file = os.path.join(json_dir, f"election_{election_id}.txt")
        os.remove(election_file)
        return jsonify({'message': 'Election deleted successfully'})
    else:
        return jsonify({'error': 'Election not found'})

# route to cast a vote in an election
@app.route('/elections/<int:election_id>/vote', methods=['POST'])
def cast_vote(election_id):
    if election_id in elections:
        vote_data = request.get_json()
        voter_id = vote_data["voter_id"]
        candidate_id = vote_data["candidate_id"]
        # add the vote to the election data
        if "votes" not in elections[election_id]:
            elections[election_id]["votes"] = {}
        if candidate_id not in elections[election_id]["votes"]:
            elections[election_id]["votes"][candidate_id] = 0
        elections[election_id]["votes"][candidate_id] += 1
        # save updated election data to json file
        election_file = os.path.join(json_dir, f"election_{election_id}.txt")
        with open(election_file, "w") as f:
            json.dump(elections[election_id], f)
        return jsonify({'message': 'Vote cast successfully'})
    else:
        return jsonify({'error': 'Election not found'})

if __name__ == '__main__':
    app.run(debug=True)