# Games with Python Data Structures

This repository contains five different games implemented using Python data structures. Each game offers a unique challenge and allows players to test their skills in various problem-solving scenarios.

## Tower of Hanoi

The Tower of Hanoi game is a mathematical puzzle that involves transferring a stack of disks from one rod to another while following specific rules. The objective is to move the entire stack to a different rod, adhering to the following guidelines:

- Only one disk can be moved at a time.
- A disk can only be moved if it is the highest disk on a stack.
- A smaller disk cannot be placed on top of a larger disk.

To play the game, enter the number of discs and then provide the number of moves and the sequence of moves to solve the puzzle. The game will save the player's name and correct response in the database.

## Sixteen Queens Puzzle

In this game, you need to place sixteen chess queens on a 16x16 chessboard in such a way that no two queens threaten each other. The game provides two approaches to finding the maximum number of solutions:

1. Sequential Program: This program sequentially searches for all possible solutions and saves them in the system.
2. Threaded Application: This threaded application identifies the maximum number of solutions and compares the time taken with the sequential program.

Players can provide answers using a user interface. If a player provides the same correct response, the system will indicate that the solution has already been recognized and ask them to try again until the maximum number of solutions is achieved. The game will record the player's name, correct response, and the time taken for each algorithm in the database.

## Minimum Cost Assignment

In this game, a company has N tasks to be completed by N employees. The goal is to use the Hungarian algorithm to determine the optimal assignment of tasks to employees that minimizes the total cost. Each game round, the cost of assigning each task to each employee randomly changes between $20 and $200. The game will record the time taken for each algorithm in each game round in the database.

## Identify Shortest Path

In this game, the distance between cities is assigned randomly between 5 and 50 kilometers. Players need to find the shortest path and distance for other cities from the system's randomly selected city. The game utilizes the Bellman-Ford and Dijkstra algorithms to determine whether the user response is correct or incorrect. The time taken for each algorithm in each game round is recorded in the database.

## Predict the Value Index

In this game, 5000 random numbers between 1 and 1000000 are generated in each game round. The game implements various search algorithms, including Binary Search, Jump Search, Exponential Search, Fibonacci Search, and Interpolation Search. Players are asked to predict the index of a randomly selected number from 1 to 1000000. If the player correctly identifies the answer, their name and the correct response are saved in the database. The game also records the time taken for each search method and the index values returned from each search algorithm.

Please refer to the individual game branches for more details on each game and the code used for unit testing.

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
To run this game, follow these instructions:

1. Download the repository as a zip file or clone the branch using the command:
    ```
    git clone https://github.com/kusalkrp/5-Games-with-Python-Data-Structures/tree/main
    ```

2. Navigate to the "game" folder in the downloaded or cloned repository.

3. Install the required dependencies by running the following command:
    ```
    pip install -r requirements.txt
    ```

4. Once the dependencies are installed, you can run the game by executing the `main.py` file:
    ```
    python main.py
    ```

Please make sure you have Python installed on your system before running the game.

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
