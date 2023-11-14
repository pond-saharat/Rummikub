Rummikub

- main.py: 
This is the entry point of your game. It will initialize Pygame user interface and game engine via class GameEngine and class GameUI. The user should be able to open the game via python main.py
- config.py: 
This file holds various configuration settings for your game, such as screen dimensions, color constants, font settings, and any other configurable parameters. Keeping these separate from your main game logic makes it easier to adjust settings without digging through your main code.

- game_engine.py: This module contains the GameEngine class. The GameEngine class manages the game state, including starting a new game, handling player turns, checking for win conditions, and transitioning between different states of the game (like game start, in-play, game over).

- game_ui.py: This module contains the GameUI class. The GameUI class will handle the event provided by the HumanPlayer and pass them to GameEngine.

- player.py: Here, you define a Player class. Each instance of this class represents a player in the game. It should store information specific to each player, such as their hand (the tiles they currently hold), their name or ID, and possibly their score.
    class Player should track how many cards they are holding
    class HumanPlayer(Player) is a typical player
    class BotPlayer(Player) should have a method that can think and return a move

- card.py: should contain the card
    class Card should have following attributes
        rect = Rectangle respect to the picture of the card
        number: int
        colour: str
        Joker: bool
- deck.py: should initialize the card pool and contain the remaining cards after distributing.
- board.py: should track which groups are currently on the board