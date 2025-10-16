# Running the Development Server

Not much work is needed to run the backend server for the app:

### Prerequisites

- Python 3.7+
- Pip

From the `backend/` directory:

1. Create Virtual Environment
```
python3 -m venv .venv
```

2. Initialize Virtual Environment

```
. ./.venv/bin/activate
```

3. Install Python Dependencies

```
pip install -r requirements.txt
```

4. Run Server

This is a pretty basic Flask server so you can run:

```
flask --app server run
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



<!-- 
  # TODO question analytics, most frequent, least frequent question, entity asked about

  # TODO logical operators of civs that get X but not Y, AND Y, OR Y
  # TODO This vs. that only if they are not techs
  # TODO what is the name of civ UT/UU
  # TODO These questions:
    #   Specific info questions:
    # HP, Base attack, Bonus damage, movement speed, frame delay, regeneration rate?
    # Armor, hidden armor, range
  
  # What is the pikemen’s attack bonus versus camels?

  # How much anti cavalry damage do Byzantine cataphracts resist?

  # What is the movement speed of a capped ram with drill?

  # What’s the hitpoints of a Viking man-at-arms in Castle Age?

  # Do hand cannoneers benefit from ballistics?

  # How many petards does it take to destroy a castle?

  # How many +2 crossbows does it take to kill a +2 knight with bloodlines in one shot?

  # Did Spirit of the Law make a video on [x topic]?

  # Has T-West done a pacifist run on [x scenario] yet?

  # Can 25 knights beat 25 Teutonic knights?

  # Does 40 archers trade well against 20 skirmishers?

  # Do X entity get bonus vs Y entity? -->