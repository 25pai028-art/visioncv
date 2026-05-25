import cv2
import mediapipe as mp
import numpy as np
import math
import time

# Initialize MediaPipe
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5
)

# Initialize video capture
cap = cv2.VideoCapture(0)

def get_gesture(landmarks, handedness):
    """
    Detect gesture from hand landmarks
    Returns: "No Hand", "Open Hand", "Pointing", "Thumbs Up", "Peace", "OK"
    """
    
    if landmarks is None:
        return "No Hand"
    
    h, w, c = landmarks.shape
    lm = landmarks[0]
    
    # Extract key points
    thumb_tip = np.array([lm[4][0], lm[4][1]])
    thumb_ip = np.array([lm[3][0], lm[3][1]])
    index_tip = np.array([lm[8][0], lm[8][1]])
    index_pip = np.array([lm[6][0], lm[6][1]])
    middle_tip = np.array([lm[12][0], lm[12][1]])
    middle_pip = np.array([lm[10][0], lm[10][1]])
    ring_tip = np.array([lm[16][0], lm[16][1]])
    ring_pip = np.array([lm[14][0], lm[14][1]])
    pinky_tip = np.array([lm[20][0], lm[20][1]])
    pinky_pip = np.array([lm[18][0], lm[18][1]])
    palm_center = np.array([lm[9][0], lm[9][1]])
    
    # Calculate distances
    def distance(p1, p2):
        return np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)
    
    # Check if fingers are extended
    def is_finger_extended(tip, pip):
        return tip[1] < pip[1]  # tip is higher than pip (y-axis inverted in image)
    
    thumb_extended = is_finger_extended(thumb_tip, thumb_ip)
    index_extended = is_finger_extended(index_tip, index_pip)
    middle_extended = is_finger_extended(middle_tip, middle_pip)
    ring_extended = is_finger_extended(ring_tip, ring_pip)
    pinky_extended = is_finger_extended(pinky_tip, pinky_pip)
    
    extended_fingers = sum([thumb_extended, index_extended, middle_extended, ring_extended, pinky_extended])
    
    # Gesture detection logic
    
    # Thumbs Up: Only thumb extended, pointing up
    if thumb_extended and not index_extended and not middle_extended and not ring_extended and not pinky_extended:
        if thumb_tip[1] < palm_center[1]:
            return "Thumbs Up"
    
    # Pointing: Only index extended
    if index_extended and not middle_extended and not ring_extended and not pinky_extended:
        return "Pointing"
    
    # Peace/Victory: Index and middle extended, others closed
    if index_extended and middle_extended and not ring_extended and not pinky_extended:
        # Check if fingers are separated
        if distance(index_tip, middle_tip) > distance(index_pip, middle_pip) * 0.5:
            return "Peace"
    
    # Open Hand: All fingers extended
    if extended_fingers >= 4:
        return "Open Hand"
    
    # OK: Thumb and index touching, other fingers extended
    if distance(thumb_tip, index_tip) < 30 and middle_extended and ring_extended and pinky_extended:
        return "OK"
    
    return "No Hand"

print("Starting gesture detection...")
print("Press 'q' to exit")

frame_count = 0
last_gesture = "No Hand"

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        frame_count += 1
        
        # Flip and process frame
        frame = cv2.flip(frame, 1)
        h, w, c = frame.shape
        
        # Convert to RGB for MediaPipe
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)
        
        gesture = "No Hand"
        
        if results.multi_hand_landmarks and results.multi_handedness:
            # Process each detected hand
            for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
                # Convert landmarks to numpy array
                h_landmarks = []
                for lm in hand_landmarks.landmark:
                    h_landmarks.append([lm.x * w, lm.y * h, lm.z])
                landmarks_array = np.array([h_landmarks])
                
                # Get gesture
                gesture = get_gesture(landmarks_array, handedness.classification[0].label)
                
                # Draw hand on frame
                mp_drawing.draw_landmarks(
                    frame,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=1),
                    mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2)
                )
        
        # Write gesture to file
        if gesture != last_gesture:
            try:
                with open("gesture.txt", "w") as f:
                    f.write(gesture)
                last_gesture = gesture
                print(f"Gesture detected: {gesture}")
            except Exception as e:
                print(f"Error writing gesture: {e}")
        
        # Display gesture on frame
        cv2.putText(frame, f"Gesture: {gesture}", (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        # Show frame
        cv2.imshow("VisionCV - Gesture Detection", frame)
        
        # Press 'q' to exit
        if cv2.waitKey(5) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    print("\nGesture detection stopped")
finally:
    cap.release()
    cv2.destroyAllWindows()
    hands.close()
    print("Camera closed")
