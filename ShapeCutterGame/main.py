import cv2
import mediapipe as mp
import numpy as np
import random
import time

# Constants
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
SHAPES = ["circle", "square", "triangle"]
SHAPE_COLOR = (0, 255, 0)
TRACE_COLOR = (255, 0, 0)
SHAPE_THICKNESS = 3
TRACE_THICKNESS = 4
TRACE_TOLERANCE = 25
GAME_DURATION = 10  # Time limit in seconds

# Mediapipe Hand Detection
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils


# Generate a random shape
def generate_shape():
    shape = random.choice(SHAPES)
    center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
    size = 150
    return shape, center, size


# Draw the shape
def draw_shape(image, shape, center, size):
    if shape == "circle":
        cv2.circle(image, center, size, SHAPE_COLOR, SHAPE_THICKNESS)
    elif shape == "square":
        top_left = (center[0] - size, center[1] - size)
        bottom_right = (center[0] + size, center[1] + size)
        cv2.rectangle(image, top_left, bottom_right, SHAPE_COLOR, SHAPE_THICKNESS)
    elif shape == "triangle":
        pts = np.array(
            [
                (center[0], center[1] - size),
                (center[0] - size, center[1] + size),
                (center[0] + size, center[1] + size),
            ],
            np.int32,
        )
        cv2.polylines(
            image, [pts], isClosed=True, color=SHAPE_COLOR, thickness=SHAPE_THICKNESS
        )


# Check if a point is near a shape's contour
def is_point_near_shape(shape, center, size, point):
    px, py = point
    if shape == "circle":
        distance = np.sqrt((px - center[0]) ** 2 + (py - center[1]) ** 2)
        return abs(distance - size) < TRACE_TOLERANCE
    elif shape == "square":
        x_min, x_max = center[0] - size, center[0] + size
        y_min, y_max = center[1] - size, center[1] + size
        return (
            abs(px - x_min) < TRACE_TOLERANCE
            or abs(px - x_max) < TRACE_TOLERANCE
            or abs(py - y_min) < TRACE_TOLERANCE
            or abs(py - y_max) < TRACE_TOLERANCE
        )
    elif shape == "triangle":
        pts = [
            (center[0], center[1] - size),
            (center[0] - size, center[1] + size),
            (center[0] + size, center[1] + size),
        ]
        for i in range(3):
            p1, p2 = pts[i], pts[(i + 1) % 3]
            d = abs(
                (p2[1] - p1[1]) * px
                - (p2[0] - p1[0]) * py
                + p2[0] * p1[1]
                - p2[1] * p1[0]
            ) / np.sqrt((p2[1] - p1[1]) ** 2 + (p2[0] - p1[0]) ** 2)
            if d < TRACE_TOLERANCE:
                return True
    return False


# Main function
def main():
    shape, center, size = generate_shape()
    traced_points = []
    points_near_shape = 0
    total_points = 0
    game_over = False
    game_started = False
    start_time = None

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, WINDOW_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, WINDOW_HEIGHT)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Hand detection
        result = hands.process(rgb_frame)
        if result.multi_hand_landmarks and not game_over:
            for hand_landmarks in result.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    frame, hand_landmarks, mp_hands.HAND_CONNECTIONS
                )

                # Get index finger tip
                x, y = int(hand_landmarks.landmark[8].x * WINDOW_WIDTH), int(
                    hand_landmarks.landmark[8].y * WINDOW_HEIGHT
                )

                # Start the game timer when the first point is traced
                if not game_started and is_point_near_shape(
                    shape, center, size, (x, y)
                ):
                    game_started = True
                    start_time = time.time()

                if game_started:
                    traced_points.append((x, y))
                    cv2.circle(frame, (x, y), TRACE_THICKNESS, TRACE_COLOR, -1)

                    # Check if the point is near the shape
                    if is_point_near_shape(shape, center, size, (x, y)):
                        points_near_shape += 1
                    total_points += 1

        # Draw shape and traced path
        draw_shape(frame, shape, center, size)
        for point in traced_points:
            cv2.circle(frame, point, TRACE_THICKNESS, TRACE_COLOR, -1)

        # Display game status
        if not game_started:
            cv2.putText(
                frame,
                "Start tracing the shape!",
                (WINDOW_WIDTH // 4, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 255, 255),
                2,
            )
        elif not game_over:
            # Display remaining time
            elapsed_time = time.time() - start_time
            remaining_time = max(0, GAME_DURATION - elapsed_time)
            cv2.putText(
                frame,
                f"Time: {int(remaining_time)}s",
                (WINDOW_WIDTH - 150, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 255, 255),
                2,
            )

            # Check if time is up
            if remaining_time <= 0:
                game_over = True

        # Display instructions
        cv2.putText(
            frame,
            "Press 'R' to Restart, 'Q' to Quit",
            (10, WINDOW_HEIGHT - 20),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2,
        )

        # Display score when game is over
        if game_over:
            score = (
                int((points_near_shape / total_points) * 100) if total_points > 0 else 0
            )
            cv2.putText(
                frame,
                f"Your Score: {score}%",
                (WINDOW_WIDTH // 3, WINDOW_HEIGHT // 2),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                3,
            )

        # Show frame
        cv2.imshow("Squid Game Cookie Cutter Challenge", frame)

        # Handle keypresses
        key = cv2.waitKey(1) & 0xFF
        if key == ord("r"):
            shape, center, size = generate_shape()
            traced_points = []
            points_near_shape = 0
            total_points = 0
            game_over = False
            game_started = False
            start_time = None
        elif key == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
