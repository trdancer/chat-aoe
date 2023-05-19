# Chat AOE

## About 

This goal of this project is to provide a chat bot -style API/interface to users to easily get information about game information for the popular game "Age of Empires 2 Definitive Edition". More information about the game can be found here: [https://www.ageofempires.com/games/aoeiide/](https://www.ageofempires.com/games/aoeiide/).

The game has a loads of information for players to memorize, with dozens of units, technologies, and bonuses. Each of the 49 civilizations in the game have a unique combination of access to these things in the game, so even the most skilled and seasoned players don't always know all the ins and outs of the game. This tool allows you to ask the bot common questions about the game and it will respond to you with the answer! No need to look up the information manually in-game, or in a tech tree explorer, or ask others in an online forum. I have observed that many people playing/watching this game have questions about game information, and this would allow that to be more easily accessible.

Here are some of the things you can do with Chat AOE

- Ask if a civilization has a technology or unit: 
  - *"Do the Britons get Bloodlines?"*
  - *"Does Hindustanis have Ring Archer Armor?"*
- Ask how much a tech costs:
  - *"How much does Hoardings cost?"*
- General Information about something:
  - *"Tell me about Yasama"*

### Use Cases
I imagine this tool being used in 2 ways:

- Native Website/UI
  - I eventually want to publish this app to the web for everyone to access with an easy to use interface. This will allows AOE2 gamers to go this website whenever they need a quick answer to a game question.
- Discord/Twitch Bot
  - Once the API and UI are complete and have adequate reliability, question repsonses, etc. I would create a bot for Twitch. This would allow streamers to integrate a bot command into their chat. Then their viewers would be able to ask this bot questions and instantly get information back. This removes the burden of the streamer or other viewers to know absolute game knowledge, or go to the tech tree themselves.

## Usage
Here is a full list of things you can ask Chat AOE:

### Questions

- Ask if a civilization has a technology or unit: 
  - *"Do the Britons get Bloodlines?"*
  - *"Does Hindustanis have Ring Archer Armor?"*
- Ask how much a tech costs:
  - *"How much does Hoardings cost?"*
  - *"What is the cost of Crossbow?"*
- General Information about something:
  - *"Tell me about Yasama"*
  - *"Paladin"*
  - *"Explain elite teutonic knight"*
  - *"Tell me about Byzantines"*
- Unique Units:
  - Currently only works for units from the Castle
  - *"What is Dravidians unique unit?"*
- Unique Technologies:
  - *"What is Aztecs castle age unique tech?"*
  - *"What is Malians UTs?"*
- What civilizations get access to something:
  - Does not work for unique units from the Castle
  - *"Which civilizations get heavy camel?"*
  - *"What are the civilizations that get eagles?"*

### Responses
The bot will respond to you with the information requested in plain text.

Additionally, it will include any "related" entities. Right now those are just names of units, techs, civs, or buildings that are in the description of the thing you asked about. For example, if you ask about monks, then it will also tell you that the scout cavalry, and monastary are related.

## FAQ

***Isn't this tool obesolete now that we apps like ChatGPT?***

No, while apps like ChatGPT provide general purpose intellegence, and allows users to have natural language conversations, they have a few disadvatages;

- They do not have the specialized intelligence needed for a tool like this. We cannnot get accurate answers from ChatGPT for nuanced game info. We can embed the game data directly into this tool and enable it to respond to complex questions.
- They are prone to hallucanating/making up information. If we want information about a civilization, we always need it to be correct. LLMs have no concept of what is the ultimate source of truth or even really have any idea "what" they are saying. Take for example this question given to ChatGPT:

    *Do bohemians get paladin?*
  
        No, the Bohemians civilization in Age of Empires 2 Definitive Edition does not have access to the Paladin unit. Paladins are one of the most powerful and expensive cavalry units in the game and are only available to civilizations with access to the Stable and the necessary technology upgrades.

        While the Bohemians do have access to cavalry units, such as Knights and Hussars, their strengths lie primarily in their unique unit, the Hussite Wagon, which is a ranged siege unit that can convert enemy units to their side. The Bohemians also receive other bonuses related to their siege units and monks, making them a unique and versatile civilization to play with.

    And if you know about the "Hussit Wagon" unit, you know it cannot convert units.

- They're functionality is overkill for our purposes. We do not need a full conversation with the bot, we just want to get our information and be done.

Some of the functionality of this app is inspired by what ChatGPT can do, but the idea for this tool was conceived well before ChatGPT was launched!

----------

Project created by Troy Kelley (Your Average Duck/uraverageduck) 2022-2023.
