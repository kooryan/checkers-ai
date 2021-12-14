'''
This module is created to enable simulation of games between bots MCTS vs Baseline AI
'''
import argparse
from copy import deepcopy
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib.ticker import PercentFormatter
from board import Board
import math
from bot import Node
from bot import Bot, puct
from math import inf
from player import Player


def check_num_of_games(val):
    try:
        val = int(val)
        if (val < 0):
            return 100
        return val
    except:
        return 100


# evaluate board_config argument passed from command line
def accept_board_config(val):
    try:
        val = int(val)
        if (val == 8 or val == 10 or val == 6):
            return val
        return 8
    except:
        return 8


def main():
    parser = argparse.ArgumentParser(description="Enter the size of board and number of games you want to simulate")
    parser.add_argument('board_config', default=8, type=accept_board_config)
    parser.add_argument('num_of_games', default=100, type=check_num_of_games)
    args = parser.parse_args()
    board_config = args.board_config
    num_of_games = args.num_of_games
    num_of_pawns = 0
    print(f"Board config selected:{board_config}\nNumber of games to be played: {num_of_games}")
    while True:
        if (board_config == 8):
            print("Select Number of Pawns for the board")
            numOfPawns = int(input("12,\t9,\t6\n"))
            if numOfPawns == 6 or numOfPawns == 9 or numOfPawns == 12:
                print("num_of_pawns")
                num_of_pawns = numOfPawns
                break
        else:
            if board_config == 6:
                num_of_pawns = 6
            elif board_config == 10:
                num_of_pawns = 20
            break
    state = Board(board_config, num_of_pawns)
    node = Node(state, depth=0)
    moves = -1
    nodes_processed = 0
    games = 0
    moves_list = []
    scores = []
    nodes_processed_list_NNMCTS = []
    nodes_processed_list_AB = []
    NN_MCTS_AI_WON = 0
    AB_WON = 0
    while games < num_of_games:
        state = Board(board_config, num_of_pawns)
        obstacles = state.set_obstacles(0)
        print(f"Obstacles added at {obstacles}")
        node = Node(state, depth=0)
        games += 1
        moves = -1
        bot = Bot()
        bot2 = Bot()
        player_1 = Player(True)
        while not state.check_game_status():
            moves += 1
            print(f"Game #: {games}/{num_of_games}\nMove #: {moves}")
            prev_move = state.total_moves
            if moves % 2 == 0:
                print(state)
                print(f"Moves since last capture: {state.moves_since_last_capture}")
                print("NN + MCTS's turn")
                node = player_1.player_NN_MCTS_AI(bot, state)
                print(f"Nodes processed this turn {bot.tree_node_processed}")
                if node is None:
                    break
            else:
                print(node.state)
                print(f"Moves since last capture: {node.state.moves_since_last_capture}")
                print("Alpha-Beta AI turn")
                nodes_processed = bot2.tree_node_processed

                node = bot2.alpha_beta(node, 4, -inf, inf, True)[1]

                nodes_processed_this_turn = bot2.tree_node_processed - nodes_processed
                print(f"nodes_processed_this_turn {nodes_processed_this_turn}")
                if node is None:
                    break
            state = node.state
            if state.total_moves == prev_move:
                num_passes += 1
            else:
                num_passes = 0
            if num_passes == 5:
                break
        print(f"Total moves: {moves}")
        score = state.compute_score()
        if (len(state.p1_pawns) > len(state.p2_pawns)):
            NN_MCTS_AI_WON += 1
            print("NN + MCTS AI Won")
            print(f"Score = {score}")
        elif len(state.p1_pawns) < len(state.p2_pawns):
            print("AB AI Won")
            print(f"Score = {score * -1}")
            AB_WON += 1
        else:
            print("It's a draw")
            print(f"Score = {score}")
        print(f"total nodes processed = {bot.tree_node_processed + bot2.tree_node_processed}")
        moves_list.append(moves)
        scores.append(score)
        nodes_processed_list_NNMCTS.append(bot.tree_node_processed)
        nodes_processed_list_AB.append(bot2.tree_node_processed)
    from pathlib import Path
    # TODO: `~` not working in Mac, Analyse and fix
    path = Path('~/../plots/')
    with open(path / f"Simulated_{board_config}x{board_config}_{num_of_games}_{num_of_pawns}.txt", 'w') as f:
        f.write(
            f"Moves List: {moves_list}\nScores List: {scores}\nNodes Processed List NN + MCTS: {nodes_processed_list_NNMCTS}\nNodes Processed List AB: {nodes_processed_list_AB}"
            f"\nNN + MCTS_AI_WON: {NN_MCTS_AI_WON}\nAB AI WON: {AB_WON}")
    print(moves_list)
    print(scores)
    print(nodes_processed_list_NNMCTS)
    print(nodes_processed_list_AB)
    generatePlots(nodes_processed_list_NNMCTS, "Range of Nodes processed", "Number of games", "Nodes processed for NN + MCTS",
                  path / f"NodesprocessedMCTS_{board_config}_{num_of_games}_{num_of_pawns}")
    generatePlots(nodes_processed_list_AB, "Range of Nodes processed", "Number of games", "Nodes processed for AB",
                  path / f"NodesprocessedAB_{board_config}_{num_of_games}_{num_of_pawns}")


def generatePlots(nodes_processed, x_label, y_label, title, file_name):
    n_bins = 10
    # Creating histogram
    fig, axs = plt.subplots(1, 1,
                            figsize=(10, 7),
                            tight_layout=True)

    # Remove axes splines
    for s in ['top', 'bottom', 'left', 'right']:
        axs.spines[s].set_visible(False)

    # Remove x, y ticks
    axs.xaxis.set_ticks_position('none')
    axs.yaxis.set_ticks_position('none')

    # Add padding between axes and labels
    axs.xaxis.set_tick_params(pad=5)
    axs.yaxis.set_tick_params(pad=10)

    # Add x, y gridlines
    axs.grid(b=True, color='grey',
             linestyle='-.', linewidth=0.5,
             alpha=0.6)

    # Creating histogram
    N, bins, patches = axs.hist(nodes_processed, bins=n_bins)

    # Setting color
    fracs = ((N ** (1 / 5)) / N.max())
    norm = colors.Normalize(fracs.min(), fracs.max())

    for thisfrac, thispatch in zip(fracs, patches):
        color = plt.cm.viridis(norm(thisfrac))
        thispatch.set_facecolor(color)

    # Adding extra features

    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)

    # Show plot
    plt.savefig(file_name)


if __name__ == "__main__":
    main()
