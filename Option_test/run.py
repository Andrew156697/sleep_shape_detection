from flask import Flask, Response
import cv2
import time
import mediapipe as mp

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

# Initialize Flask app
app = Flask(__name__)

# Initialize the camera
camera = cv2.VideoCapture(0)

def generate_frames():
    frame_count = 0
    start_time = time.time()

    while True:
        # Read a frame from the camera
        success, frame = camera.read()
        if not success:
            break
        else:
            # Convert the frame to RGB for MediaPipe processing
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Process the frame to detect poses
            results = pose.process(rgb_frame)

            # Draw the pose landmarks on the frame and extract coordinates
            if results.pose_landmarks:
                mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

                # Extract and print coordinates of 32 landmarks
                for idx, landmark in enumerate(results.pose_landmarks.landmark):
                    x = landmark.x  # Normalized x-coordinate
                    y = landmark.y  # Normalized y-coordinate
                    z = landmark.z  # Depth
                    visibility = landmark.visibility  # Visibility score
                    print(f"Landmark {idx}: x={x:.2f}, y={y:.2f}, z={z:.2f}, visibility={visibility:.2f}")

            # Increment frame count
            frame_count += 1

            # Calculate FPS
            elapsed_time = time.time() - start_time
            if elapsed_time > 1:  # Update FPS every second
                fps = int(frame_count / elapsed_time)
                frame_count = 0
                start_time = time.time()

                # Put FPS text on the frame
                cv2.putText(frame, f'FPS: {fps}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

            # Encode the frame in JPEG format
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            # Yield the frame in the correct format for streaming
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return '''
    <h1>BlazePose with Flask</h1>
    <p>Visit <a href="/video_feed">/video_feed</a> to see the camera stream with pose detection.</p>
    <img src="/video_feed" width="1720" height="880">
    '''

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)
