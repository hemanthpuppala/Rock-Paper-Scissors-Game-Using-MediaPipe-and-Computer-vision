import cv2
import mediapipe as mp
import random
import math
import time
import numpy as np

class RockPaperScissorsMediaPipe:
    def __init__(self):
        self.choices = ['rock', 'paper', 'scissors']
        self.win_map = {'rock': 'scissors', 'paper': 'rock', 'scissors': 'paper'}
        self.lose_map = {'rock': 'paper', 'paper': 'scissors', 'scissors': 'rock'}
        
        # Pattern recognition storage
        self.player_history = []
        self.pattern_length = 3  # Look for patterns of this length
        self.player_score = 0
        self.ai_score = 0
        
        # MediaPipe setup
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.mp_drawing = mp.solutions.drawing_utils
        
        # Game state
        self.countdown = 0
        self.last_gesture = None
        self.ai_choice = None
        self.round_result = None
        self.waiting_for_gesture = False
        
    def detect_gesture(self, hand_landmarks):
        # Get fingertip and finger base landmarks
        thumb_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_TIP]
        index_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
        middle_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
        ring_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.RING_FINGER_TIP]
        pinky_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.PINKY_TIP]
        
        wrist = hand_landmarks.landmark[self.mp_hands.HandLandmark.WRIST]
        
        # Check if fingers are extended
        fingers_extended = [
            self._is_finger_extended(thumb_tip, wrist),
            self._is_finger_extended(index_tip, wrist),
            self._is_finger_extended(middle_tip, wrist),
            self._is_finger_extended(ring_tip, wrist),
            self._is_finger_extended(pinky_tip, wrist)
        ]
        
        # Determine gesture based on extended fingers
        if sum(fingers_extended) <= 1:  # Only thumb may be extended
            return "rock"
        elif all(fingers_extended[1:]) and not fingers_extended[0]:  # All fingers except thumb
            return "paper"
        elif fingers_extended[1] and fingers_extended[2] and not fingers_extended[3] and not fingers_extended[4]:
            return "scissors"
        else:
            return None
            
    def _is_finger_extended(self, fingertip, wrist, threshold=0.1):
        # Simple heuristic: if the y-coordinate of the fingertip is smaller than
        # the y-coordinate of the wrist (remembering that y increases downward in images)
        return fingertip.y < wrist.y - threshold
    
    def predict_next_move(self):
        if len(self.player_history) < self.pattern_length + 1:
            return random.choice(self.choices)
        
        # Look for the most recent pattern in history
        current_pattern = self.player_history[-self.pattern_length:]
        
        # Find all occurrences of this pattern in history
        matches = []
        for i in range(len(self.player_history) - self.pattern_length):
            if self.player_history[i:i+self.pattern_length] == current_pattern:
                # What did they play after this pattern?
                matches.append(self.player_history[i + self.pattern_length])
        
        if matches:
            # Predict the most common move after this pattern
            prediction = max(set(matches), key=matches.count)
            # Choose the move that beats their predicted move
            return self.lose_map[prediction]
        else:
            return random.choice(self.choices)
    
    def determine_winner(self, player_choice, ai_choice):
        if player_choice == ai_choice:
            return "Tie!"
        elif self.win_map[player_choice] == ai_choice:
            self.player_score += 1
            return "You win!"
        else:
            self.ai_score += 1
            return "AI wins!"
    
    def play_game(self):
        cap = cv2.VideoCapture(0)
        
        start_time = time.time()
        game_state = "waiting"  # waiting, countdown, show_result
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("Failed to grab frame")
                break
                
            # Flip the frame horizontally for a later selfie-view display
            frame = cv2.flip(frame, 1)
            
            # Convert the BGR image to RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Process the frame and detect hands
            results = self.hands.process(rgb_frame)
            
            # Draw hand landmarks
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    self.mp_drawing.draw_landmarks(
                        frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                    
                    # Detect gesture
                    current_gesture = self.detect_gesture(hand_landmarks)
                    
                    # Update the display to show the detected gesture
                    if current_gesture:
                        cv2.putText(frame, f"Detected: {current_gesture}", (10, 70), 
                                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                        
                        # Store the last detected gesture
                        self.last_gesture = current_gesture
            
            # Game state machine
            current_time = time.time()
            
            # Display scores
            cv2.putText(frame, f"You: {self.player_score}  AI: {self.ai_score}", 
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            
            if game_state == "waiting":
                cv2.putText(frame, "Press SPACE to start a round", (10, frame.shape[0] - 30), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
                
                # Check for space key
                key = cv2.waitKey(1) & 0xFF
                if key == 32:  # Space key
                    game_state = "countdown"
                    start_time = current_time
                    self.countdown = 3
                elif key == 27:  # ESC key
                    break
            
            elif game_state == "countdown":
                elapsed = current_time - start_time
                
                if elapsed > 1 and self.countdown > 0:
                    self.countdown -= 1
                    start_time = current_time
                
                if self.countdown > 0:
                    # Display countdown
                    cv2.putText(frame, str(self.countdown), 
                               (frame.shape[1]//2 - 20, frame.shape[0]//2 + 20), 
                               cv2.FONT_HERSHEY_SIMPLEX, 4, (255, 255, 255), 4)
                else:
                    # Countdown finished, get player's gesture
                    if self.last_gesture:
                        player_choice = self.last_gesture
                        self.player_history.append(player_choice)
                        
                        # AI makes its choice
                        self.ai_choice = self.predict_next_move()
                        
                        # Determine the winner
                        self.round_result = self.determine_winner(player_choice, self.ai_choice)
                        
                        game_state = "show_result"
                        start_time = current_time
                    else:
                        cv2.putText(frame, "No gesture detected! Try again.", 
                                   (frame.shape[1]//4, frame.shape[0]//2), 
                                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                        game_state = "waiting"
            
            elif game_state == "show_result":
                # Display results for 3 seconds
                cv2.putText(frame, f"You chose: {self.last_gesture}", 
                           (10, frame.shape[0] - 90), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
                cv2.putText(frame, f"AI chose: {self.ai_choice}", 
                           (10, frame.shape[0] - 60), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
                cv2.putText(frame, self.round_result, 
                           (10, frame.shape[0] - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                
                if current_time - start_time > 3:
                    game_state = "waiting"
            
            # Display the frame
            cv2.imshow('Rock Paper Scissors with MediaPipe', frame)
            
            # Break the loop on 'q' key press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        # Release resources
        cap.release()
        cv2.destroyAllWindows()
        self.hands.close()
        
        print("\n==== Game Over ====")
        print(f"Final Score - You: {self.player_score}, AI: {self.ai_score}")
        
        if self.player_score > self.ai_score:
            print("You win overall! But the AI is learning...")
        elif self.player_score < self.ai_score:
            print("The AI wins overall! It learned your patterns.")
        else:
            print("It's a tie overall! The AI has matched your strategy.")

if __name__ == "__main__":
    game = RockPaperScissorsMediaPipe()
    game.play_game()