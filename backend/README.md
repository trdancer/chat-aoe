# Running the Development Server

Not much work is needed to run the backend server for the app:

### Prerequisites

- Python 3.7+
- Pip

1. Initialize Virtual Environment

```
chat-aoe/backend$ . ./.venv/bin/activate
```

2. Install Python Dependencies

```
chat-aoe/backend$ pip install -r requirements.txt
```

3. Run Server

This is a pretty basic Flask server so you can run:

```
chat-aoe/backend$ flask --app server run
```

This will run the app on port 5000.

Optionally add the `--debug` flag to enable hot reloading.

# Endpoints
The primary API endpoint is:

```
GET /api/v1/chat?q=<question>
```

Response:

```json
{
  "response": "plain text string answer here",
  "entity_names": ["recognized", "AOE", "entity", "from question", "here"],
  "civilization_access": ["Aztecs", "Mayans", "Incas"],
  "intent": 1,
  "related_entities": ["entities", "in", "response"]
}
```
## Entities
An Entity is simply any "thing" in Age of Empires:

- A technology or unit upgrade
- A unit
- A building
- A civilization

## Question Intent
The intent of a question is as follows:

**-1:**

Unknown

**0:**

How much something costs

**1:**

Does a civ get an entity

**2:**

Information about an entity

**3:**

Information about a civilization's unique tech

**4:**

Information about a civilization's unique unit from the castle

**5:**

What civilizations get an entity
