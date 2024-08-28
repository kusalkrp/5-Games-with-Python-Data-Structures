# Tower of Hanoi Game

This is a Python implementation of the classic Tower of Hanoi game using the Tkinter library for the graphical user interface.

## Description

The Tower of Hanoi is a mathematical puzzle where the objective is to move a stack of disks from one rod to another, following specific rules. This implementation provides a graphical interface to play the game.

## How to Play

1. **Objective**: Move all the disks from the source rod (leftmost) to the destination rod (rightmost) using the auxiliary rod (middle).
2. **Rules**:
   - Only one disk can be moved at a time.
   - A disk can only be placed on top of a larger disk or an empty rod.
   - All disks start on the source rod, arranged in ascending order of size from top to bottom.

## Setup and Installation

### Prerequisites

- Python 3.x
- Tkinter (usually included with Python)

### Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/tower-of-hanoi.git
   cd tower-of-hanoi

### (Optional) Create and activate a virtual environment:
python -m venv venv
venv\Scripts\activate  # On Windows
source venv/bin/activate  # On macOS/Linux

### Run the game:
python TowerofHanoi.py

### Game Controls
Drag and Drop: Click and hold a disk to drag it to another rod. Release the mouse button to place the disk.
Reset: The game will automatically reset if an invalid move is attempted.
Testing
To run the unit tests, use the following command:

### Testing
To run the unit tests, use the following command:
python -m unittest discover