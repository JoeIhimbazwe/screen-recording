import cv2
import numpy as np
import pyautogui
import time
import argparse
import os

def main(output_path: str, fps: int):
    # Get screen size
    screen_width, screen_height = pyautogui.size()
    screen_size = (screen_width, screen_height)

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

    # Define the codec and create VideoWriter object
    # 'mp4v' works well for .mp4 files on most systems
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(output_path, fourcc, fps, screen_size)

    print(f"[INFO] Recording started.")
    print(f"[INFO] Resolution: {screen_width}x{screen_height}, FPS: {fps}")
    print(f"[INFO] Output file: {os.path.abspath(output_path)}")
    print("[INFO] Press 'q' in the preview window or Ctrl+C in the terminal to stop.\n")

    prev_time = time.time()

    try:
        while True:
            # Capture the screen
            img = pyautogui.screenshot()

            # Convert PIL Image to NumPy array
            frame = np.array(img)

            # Convert RGB (PyAutoGUI) to BGR (OpenCV)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

            # Write the frame
            out.write(frame)

            # Show preview (optional – can be commented out for slightly better performance)
            cv2.imshow("Screen Recorder - Press 'q' to stop", frame)

            # Handle quit key
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("\n[INFO] 'q' pressed, stopping recording...")
                break

            # Simple FPS control (best-effort)
            elapsed = time.time() - prev_time
            sleep_time = max(0, (1.0 / fps) - elapsed)
            if sleep_time > 0:
                time.sleep(sleep_time)
            prev_time = time.time()

    except KeyboardInterrupt:
        print("\n[INFO] KeyboardInterrupt detected, stopping recording...")

    finally:
        out.release()
        cv2.destroyAllWindows()
        print("[INFO] Recording saved and resources released.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Simple screen recorder using PyAutoGUI, OpenCV, and NumPy."
    )
    parser.add_argument(
        "-o", "--output",
        type=str,
        default="screen_recording.mp4",
        help="Output video file path (default: screen_recording.mp4)"
    )
    parser.add_argument(
        "-f", "--fps",
        type=int,
        default=20,
        help="Frames per second (default: 20)"
    )

    args = parser.parse_args()
    main(args.output, args.fps)
