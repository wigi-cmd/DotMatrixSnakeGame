# DotMatrix Snake Game 

A retro-style Snake game built using **Raspberry Pi Pico W**, a **joystick**, and a **4-in-1 MAX7219 dot matrix display**, written entirely in MicroPython.

This project combines low-level hardware control with classic game logic to create a fun and responsive embedded game experience.

---

##  Components Used

- **Raspberry Pi Pico W**
- **Joystick** (2-axis analog)
- **MAX7219 Dot Matrix Display** (4 x 8x8 modules)
- **MicroPython**
- Optional: LED for "apple" indicator

---

##  How It Works

- The snake is represented as a list of `(x, y)` coordinate tuples.
- The direction is tracked as a 2D vector, e.g., right → `(1, 0)`, up → `(0, -1)`, etc.
- On each tick:
  - A new head is created by adding the current direction to the current head.
  - If the new head overlaps with the apple:
    - The snake **grows** (tail is not removed).
    - A new apple is randomly placed.
    - The score is increased.
  - Otherwise:
    - The tail is removed (snake moves forward).
- If the snake hits itself or the wall, the game ends.

---

## 🕹 Controls

- Use the analog joystick to change the snake’s direction.
- The game continuously polls the joystick to detect changes.
- Directions are constrained (e.g., cannot immediately reverse direction).

---

##  Score System

- Each apple consumed increases the score.
- Score is tracked internally and optionally can be displayed or output.

---

##  Run It

To run the game:

1. Flash MicroPython to your Raspberry Pi Pico W.
2. Upload `SnakeGame_fullversion.py` and supporting display/joystick modules to the Pico.
3. Connect joystick and MAX7219 display to correct GPIO pins.
4. Run the game via Thonny or another MicroPython IDE.

---

##  Possible Improvements

- Add game over screen or animation.
- Display score on a second display or via serial output.
- Implement difficulty levels (increase speed over time).
- Save high scores in non-volatile memory.

---

##  Author

Developed with love and a little rage by [@wigi-cmd](https://github.com/wigi-cmd)  
Built by the resistance.  


---
