# Rock-Paper-Scissors Game Using MediaPipe and Computer Vision

A fully interactive Rock-Paper-Scissors game that uses your webcam and MediaPipe's hand tracking to detect gestures in real-time, combined with random-based computer moves and a visually engaging interface.

---

## Project Overview

This project leverages computer vision—specifically, MediaPipe's robust hand landmark detection framework—to recognize your hand signs for rock, paper, or scissors. The computer opponent makes its move randomly, providing a classic, fair gameplay experience. The interface gives live feedback on gesture recognition, manages game rounds with a countdown, displays round and total scores, and allows keyboard controls for an enjoyable, tech-driven twist on a favorite childhood game.

---

## Features

- Real-time hand gesture detection using MediaPipe (rock, paper, scissors)
- Video feed, result overlay, countdown, and running score display
- Keyboard controls:
  - SPACE: Start a round
  - Q or ESC: Quit
- Engaging and easy-to-use webcam interface
- **No machine learning or AI; computer's choice is random**
- Modular code - easy to adapt or extend for more gesture-based mini-games

---

## Requirements

- Python 3.7+
- OpenCV
- MediaPipe
- NumPy

Install dependencies:
```
pip install opencv-python mediapipe numpy

```
---

## Usage

1. Save the main script (e.g., `rps_game.py`) in your project directory.
2. Run the script:
```
python rps_game.py
```
3. Your webcam window will appear. Use your hand to play:
   - Rock: Make a fist (only thumb extended or none).
   - Paper: Extend all four fingers except thumb.
   - Scissors: Extend index and middle fingers only.
4. Press SPACE to start each countdown and round.
5. Press 'q' or ESC to exit.

---

## How It Works

- The webcam frame is processed by MediaPipe to extract hand landmarks.
- Code classifies your gesture (rock, paper, or scissors) using landmark positions.
- Computer randomly selects rock, paper, or scissors.
- Scores update, feedback is shown, and the process can be repeated.

---

## Customization & Extensions

- Change timer length or interface styling for custom experience.
- Expand gesture set or add difficulty levels.
- Connect to other hardware (e.g., buzzer, lights) for fun classroom demos.

### Future Extensions (AI or Advanced Features)

- Integrate pattern recognition to predict user’s moves over time.
- Add an AI model for adaptive gameplay that learns common user strategies and counteracts them.
- Transmit game states to a remote server for multiplayer or stats tracking.

---

## License

Free to use for personal and educational purposes under the MIT License.

---

## Acknowledgements

- MediaPipe by Google for robust, easy-to-use hand detection.
- OpenCV for webcam handling and rendering.
- Inspired by classic Rock-Paper-Scissors—now with computer vision flair!

---

_Enjoy hands-on play and explore computer vision in action!_

