# American Checkers - AI (WIP)

This is an American Checkers AI game built using Python.

  ![Checkers Board](https://github.com/nikeshsraj10/checkers-ai/blob/main/images/board.PNG)
## Rules:
Open [rules.md](./rules.md) to view the rules of the game


## Python Version 

3.8.6

## Setup
  Python version: 3.0+
  ### Libraries
  - Numpy
  - Matplotlib

  ### Install numpy
  Run: `pip install numpy` <br/>
  Run: `pip install matplotlib`

## How to play?

Clone the repository by using the URL: `https://github.com/nikeshsraj10/checkers-ai.git`

CD into the game directory: `cd checkers-ai`

### To play against our AI:
Run: `python main.py`

### Simulate MCTS AI vs Baseline AI
Run: `python bot_simulate.py` <br/>
Running the above command would simulate 100 games using a 8x8 board <br/><br/>
To Configure the board and number of games use the below command <br/>
Run: `python bot_simulate.py {board_config} {number_of_games}` <br/>
Valid values for board_config is 8 or 10 <br/> <br/>
The following command will run 8x8 board for 50 games <br/>
Run: `python bot_simulate.py 8 50` <br/>
Refer to `plots` folder for the data on the simulated games

