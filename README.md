# 🗼 Tower of Hanoi


**A classic Data Structures and Algorithms problem brought to life with Python.**

Tower of Hanoi is a small interactive project built around the famous mathematical puzzle used to demonstrate recursion and algorithmic problem-solving.

The objective is to move a stack of disks from one tower to another while following a simple set of rules. This project turns that classic **DSA** problem into a fun, playable experience.

## 🎮 About the Game

The Tower of Hanoi puzzle consists of three towers and a collection of disks of different sizes.

The goal is to transfer all disks from the starting tower to the destination tower while following these rules:

## Move only one disk at a time.
## Only the top disk of a tower can be moved.
## A larger disk cannot be placed on top of a smaller disk.

The puzzle is a classic example of how recursion can solve a problem by breaking it into smaller subproblems.

## ✨ Features

- 🗼 Classic Tower of Hanoi puzzle.
- 🧠 Recursive problem-solving logic.
- 🎮 Interactive gameplay implemented in Python.
- 🔊 Sound effects using `move.wav` and `win.wav`.
- 🏆 High-score or score-tracking file using `highscore.txt`, depending on the implemented logic.
- 🐍 A lightweight project built around a fundamental **DSA** concept.

## 🧠 The Algorithm

For \(n\) disks, the recursive solution follows three steps:

## Move the top \(n-1\) disks from the source tower to the auxiliary tower.
## Move the largest remaining disk to the destination tower.
## Move the \(n-1\) disks from the auxiliary tower to the destination tower.

The minimum number of moves required to solve the puzzle is:

\[
T(n)=2^n-1
\]

For example:

| Number of disks | Minimum moves |
|---:|---:|
| 1 | 1 |
| 2 | 3 |
| 3 | 7 |
| 4 | 15 |
| 5 | 31 |
| 10 | 1,023 |

This demonstrates why the puzzle becomes increasingly challenging as the number of disks grows.

## 🛠️ Built With

- **Python** — Application logic and gameplay
- **Audio assets** — Sound effects for moves and completion

The exact graphics library and other dependencies should be confirmed from the source code.

## 📁 Project Structure

```text
Tower-of-Hanoi/
│
├── main.py          # Main application and game logic
├── highscore.txt    # High-score data
├── move.wav         # Move sound effect
├── win.wav          # Victory sound effect
└── .gitattributes
```

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone [https://github.com/**YASHRAWAT**-**1611**/Tower-of-Hanoi.git](https://github.com/**YASHRAWAT**-**1611**/Tower-of-Hanoi.git)
```

### 2. Navigate to the project directory

```bash
cd Tower-of-Hanoi
```

### 3. Install dependencies

Install Python and any additional packages required by `main.py`.

If the project uses only Python's standard library, no additional package installation may be necessary.

### 4. Run the program

```bash
python main.py
```

## 🎓 What I Learned

This project helped me explore:

- Recursion and recursive problem decomposition
- Algorithmic thinking
- The mathematical structure of the Tower of Hanoi puzzle
- Translating a **DSA** problem into an interactive application
- Basic audio integration and game-state handling

## 👨‍💻 Developer

**Yash Rawat**

- GitHub: [@**YASHRAWAT**-**1611**](https://github.com/**YASHRAWAT**-**1611**)
- LinkedIn: [Yash Rawat](https://[www.linkedin.com/in/yash-rawat-2a426a265](https://www.linkedin.com/in/yash-rawat-2a426a265))

---

**Three towers. A stack of disks. One recursive solution.** 🗼

