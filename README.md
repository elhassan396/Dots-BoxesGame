# 🎮 Dots & Boxes

> The classic Dots & Boxes game — built with Python and pygame. Nothing fancy, took me about four days to complete.

---

## 📖 About

Dots & Boxes is a classic pencil-and-paper game for two players. Starting from an empty grid of dots, players take turns drawing a single horizontal or vertical line between two adjacent dots. The player who completes the fourth side of a box claims it and earns another turn. The player with the most boxes when the grid is full wins.

This is my Python/pygame implementation of that game, built from scratch as a personal project.

---

## ✨ Features

- 2-player local gameplay
- Clean grid-based UI rendered with pygame
- Sound effects on line placement and box completion
- Score tracking displayed in real time
- Grid size selection
- ...

---

## 🚀 Getting Started

### Prerequisites

- Python 3.x
- pygame

Install pygame with:

```bash
pip install pygame
```

### Run the game

```bash
git clone https://github.com/elhassan396/Dots-BoxesGame.git
cd Dots-BoxesGame/Dots\&Boxes
python main.py
```

---

## 🎮 How to Play

1. Two players take turns clicking between two adjacent dots to draw a line.
2. If your line completes the fourth side of a box, you score a point and get another turn.
3. The game ends when all boxes are filled.
4. The player with the most boxes wins!

---

## 🛠️ Built With

- [Python 3](https://www.python.org/)
- [pygame](https://www.pygame.org/)

---

## 🎨 Credits

This project uses sound assets sourced from the [lichess.org (lila)](https://github.com/lichess-org/lila) open-source project:

| Asset                      | Author                                                       | License                                                      |
| -------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| `public/sounds/futuristic` | [Enigmahack](https://github.com/Enigmahack)                  | AGPLv3+                                                      |
| `public/sounds/nes`        | [Enigmahack](https://github.com/Enigmahack)                  | AGPLv3+                                                      |
| `public/sounds/piano`      | [Enigmahack](https://github.com/Enigmahack)                  | AGPLv3+                                                      |
| `public/sounds/sfx`        | [Enigmahack](https://github.com/Enigmahack)                  | AGPLv3+                                                      |
| `public/sounds/lisp`       | [EdinburghCollective](https://lichess.org/@/EdinburghCollective) | [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) |

---

## 📄 License

This project is licensed under the **GNU Affero General Public License v3.0 or later (AGPLv3+)** — see the [LICENSE](LICENSE) file for the full text.

In short: you're free to use, modify, and redistribute this code, including running it as a network service, as long as any modified version (including ones run as a web service) is also made available under the AGPLv3+ and the source code is shared.
