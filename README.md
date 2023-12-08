## Rummikub
### Team members
- Zihe GAO (psxzg11)
- Saharat PRANGPITAK (psxsp16)
- Jinxu SHEN (psxjs26)
- Yuheng Yang (psxyy22)
### Runnning a game
This game was developed on Pygame 2.5.2 and Python version 3.12.0.
A user can run a game by typing `python main.py` or `python3 main.py`.

### Files

- **main.py**: This file is the entry point of your game. It will initialise Pygame interface and game engine by initialising an instance of `GameEngine` and `GameUI` classes. The user should be able to open the game by typing `python main.py` or `python3 main.py` in the command line interface.
- **config.py**: This file contains all constants and parameters which can be set before running a game. It holds various configuration settings for your game, such as screen dimensions, color constants, font settings, and any other configurable parameters. Keeping these separate from main game logic makes it easier to adjust settings without digging through the main code.
- **game_engine.py**: This module contains the `GameEngine` class. The `GameEngine` class manages the game state, including starting a new game, handling player turns, checking for win conditions, and transitioning between different states of the game (like game start, in-play, game over).
- **game_ui.py**: This module contains the `GameUI` class. The `GameUI` class will handle the event provided by the `HumanPlayer` and pass the information to the `GameEngine` object.
- **player.py**: Here, you define a `Player` class. Each instance of this class represents a player in the game. It should store information specific to each player, such as their hand (the cards they currently hold), their name or ID, and possibly their score.
  - Class `Player` is a parent class of any players. Most part of the game will handle any types of players the same.
  - Class `HumanPlayer(Player)` is a typical human player.
  - Class `AIPlayer(Player)` is a non-human player that relies on play-for-me features.
- **card.py**: This file contains the definitions of class `Card`, class `ColourCard(Card)`, and class `JokerCard(Card)`.
  - Class `Card` has atrributes of colour, value, and parameters used in a drawing process of Pygame.
  - Class `ColourCard(Card)` is a class which represents a colour card.
  - Class `JokerCard(Card)` is a class which represents a joker card.
- **deck.py**: This file contains a logic of initialisation of the card pool and contain the remaining cards after distributing.

- **board.py**: should track which groups/runs are currently on the board.

- **cardset.py**: should define a collections of cards.
    class `Group(CardSet)` is a collection with the same number, but their colours are different.
    class `Run(CardSet)` is a collection with consecutive numbers.
- **bot.py**: This file contains a logic of retrieving the information of cards and put them into a Tensor. Then, the tensor is processed to calculate the longest groups or runs that the bot can play in that specific turn. Finally, the tensor is transformed and points to an associated Card object.

#### References
The font used in the main menu's game logo. <br> 
[Pattaya by Cadson Demak](https://fonts.google.com/specimen/Pattaya?query=Cadson+Demak)
<br><br>The pictures used in a tile. <br> 
[The University of Nottingham Image Bank](https://www.nottingham.ac.uk/imagebank/index.php)

