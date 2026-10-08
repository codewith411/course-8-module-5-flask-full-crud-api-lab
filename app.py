from flask import Flask, jsonify, request

app = Flask(__name__)


# Simulated data
class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        return {"id": self.id, "title": self.title}


# In-memory "database"
events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop")
]


# Welcome route
@app.route("/")
def home():
    return jsonify({"message": "Welcome to the Event API"})


# GET /events - Return all events
@app.route("/events", methods=["GET"])
def get_events():
    return jsonify([event.to_dict() for event in events])


# POST /events - Create a new event
@app.route("/events", methods=["POST"])
def create_event():
    data = request.get_json()

    # Make sure JSON data was provided
    if not data:
        return jsonify({"error": "Request body is required"}), 400

    # Make sure title was provided
    title = data.get("title")

    if not title:
        return jsonify({"error": "Title is required"}), 400

    # Generate a new ID
    new_id = max((event.id for event in events), default=0) + 1

    # Create the new event
    new_event = Event(new_id, title)

    # Add it to the in-memory database
    events.append(new_event)

    return jsonify(new_event.to_dict()), 201


# PATCH /events/<id> - Update an event title
@app.route("/events/<int:event_id>", methods=["PATCH"])
def update_event(event_id):
    # Find the event by ID
    event = next(
        (event for event in events if event.id == event_id),
        None
    )

    # Return 404 if the event does not exist
    if event is None:
        return jsonify({"error": "Event not found"}), 404

    data = request.get_json()

    # Make sure JSON data was provided
    if not data:
        return jsonify({"error": "Request body is required"}), 400

    # Make sure title was provided
    title = data.get("title")

    if not title:
        return jsonify({"error": "Title is required"}), 400

    # Update the event
    event.title = title

    return jsonify(event.to_dict()), 200


# DELETE /events/<id> - Remove an event
@app.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    # Find the event by ID
    event = next(
        (event for event in events if event.id == event_id),
        None
    )

    # Return 404 if the event does not exist
    if event is None:
        return jsonify({"error": "Event not found"}), 404

    # Remove the event from the in-memory database
    events.remove(event)

    return "", 204


if __name__ == "__main__":
    app.run(debug=True)
