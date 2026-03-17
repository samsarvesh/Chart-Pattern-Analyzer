import cv2
import numpy as np
import time
from mss import mss
from ultralytics import YOLO

# --- CONFIGURATION ---
# Define the screen region to capture (x, y, width, height)
# You can use a tool like 'ScreenToGif' or similar to find these coordinates
MONITOR_REGION = {'top': 100, 'left': 100, 'width': 800, 'height': 600}
CAPTURE_INTERVAL = 5  # Seconds between scans
MODEL_PATH = 'yolov8n_trading.pt'  # Path to your trained model

def preprocess_image(img):
    """
    Converts image to grayscale and resizes to 224x224 to save RAM (4GB limit).
    """
    gray = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)
    resized = cv2.resize(gray, (224, 224))
    # YOLOv8 usually expects 3-channel images, so we convert back to BGR
    # but the information content is reduced, saving processing overhead
    processed = cv2.cvtColor(resized, cv2.COLOR_GRAY2BGR)
    return processed

def detect_patterns(model, frame):
    """
    Placeholder for YOLOv8-nano pattern detection.
    """
    # In a real scenario, model.predict() would be used
    # results = model.predict(frame, conf=0.5)
    
    # MOCK LOGIC FOR DEMONSTRATION
    # Replace this with actual model inference:
    # for r in results:
    #     for box in r.boxes:
    #         cls = int(box.cls[0])
    #         conf = float(box.conf[0])
    #         ...
    
    return None, 0.0  # (Pattern Name, Confidence)

def main():
    print("--- Chart Pattern Risk Analyzer Started ---")
    print(f"Scanning region: {MONITOR_REGION}")
    print("Press 'q' in the preview window to stop.")

    # Initialize YOLOv8-nano (will download if not found)
    # Note: Use a custom trained model for trading patterns
    try:
        model = YOLO('yolov8n.pt') 
    except Exception as e:
        print(f"Warning: Could not load model. Error: {e}")
        model = None

    with mss() as sct:
        while True:
            start_time = time.time()

            # 1. Screen Capture
            screenshot = sct.grab(MONITOR_REGION)
            frame = np.array(screenshot)

            # 2. Image Processing
            processed_frame = preprocess_image(frame)

            # 3. Pattern Detection (Placeholder)
            # This is where your custom-trained YOLO model would run
            pattern, confidence = detect_patterns(model, processed_frame)

            # 4. Decision Logic & Console Output
            if pattern:
                print(f"[{time.strftime('%H:%M:%S')}] DETECTED: {pattern} | Confidence: {confidence:.2f}")
                if pattern == "Double Bottom":
                    print(">>> SUGGESTION: BUY")
                elif pattern == "Head and Shoulders":
                    print(">>> SUGGESTION: SELL")
            else:
                print(f"[{time.strftime('%H:%M:%S')}] No significant patterns detected.")

            # 5. Optimization & UI
            # Show a small preview window (optional, can be commented out to save more RAM)
            cv2.imshow('Analyzer Preview (224x224)', processed_frame)

            # Wait for 'q' key to exit or wait for the interval
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            # Prevent CPU overheating on i5-4200U
            elapsed = time.time() - start_time
            sleep_time = max(0, CAPTURE_INTERVAL - elapsed)
            time.sleep(sleep_time)

    cv2.destroyAllWindows()
    print("Analyzer stopped.")

if __name__ == "__main__":
    main()
