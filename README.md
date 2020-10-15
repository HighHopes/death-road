# death-road

This is a game engine developed in Python, using Flask library and SQLAlchemy. This is a basic concept for the engine, and new features will also be added soon. 

The game can be accessed at the following website https://highhopes.pythonanywhere.com

===   !!! Please DO NOT use any sensitive or personal data when registering a new account !!!   ===

Features of the game: 
- A Responsive Website for the game, designed with Bootstrap 
- Subscription System - Register your email in database to get new updates about the game
- Registration Page and Login Page
    - register a new account, no verification is needed - just for developing purpose 
    - log in to your personal account where you have your account details
- Account Page
    - Change information about the current account, Change Password
- Message System 
    - Full message system to send messages to other accouns. Check if the account exists otherwise will not send are return error.
    - Messages have the following fields: Sender, Subject and Message Body
    - Reveive messages. Unread messages are marked with a bold text.
    - Replay to a message you have received.
    - Delete or Mark as Read one or multiple messages 
    - Get a Notificiation if a new message is received, or not read.
- HERO Pages
    - If an account have no hero, you can create one. Currently only Name and Gendre can be choosen
    - STATISTICS Page will show all heroes created with their current level. The Sorting is based on the experience points of every hero 
        - Multiple updates will be added at this page soon.
        - Can select a hero and send a message to that account from Statistics Page
    - Fighting is Turn Base (Every involved character can hit once)
    - Hero can train with different "creatures" and gain experience 
    - Every "creature" have a different level, HP, Hit Points etc
    - Everytime a Hero levels up, it gains Stat Points that can be used to upgrade his Strength, Hit Points, Attack Points, Dodge Points, Critical Hit POints
        - Every Hit Points increases Hero's current HP
        - HP is regenerated with 1 unit every second 
        - When hero is Dead, a time to revive is necessary and the hero is unable in that period of time
    - When hero is fighting, a different time, based on "Animal" level is required for the hero. During that time, the hero is unavailable
    
    
CURRENTLY WORKING ON:
  - Improve the hero attack points and different fighting styles
  - BUILDING SYSTEM (75% done) 
      - Different production buildings (example: Woodcutter - provides wood every x seconds. Wood is needed to construt other buildings)
          - Currently used production buildings are: Wood, Iron, Gold
      - Support Buildings (Example: Hospital - Increases the hero Hit Point Regeneration Rate) 
      - Resourcess are generated based on building level at different rates.
  - SPECIAL RESOURCES - are gained from fighting stronger creatures and are used to craft items or other stuff 
      - Rare drops from creatures
  - ITEM SYSTEM
      - INVENTORY 
      - Hero can equipt different items to get bonuses 
      - Items will be dropped from fighting with creatures
      - Later on the items can be crafted from different resources 
