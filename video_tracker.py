import cv2
import pandas as pd
import os
import math


def track_video(video_file, output_csv):

    video = cv2.VideoCapture(video_file)

    if not video.isOpened():
        print("ERROR: Video could not be opened.")
        return False

    # Read actual FPS from video
    fps = video.get(cv2.CAP_PROP_FPS)

    print("Video FPS:", fps)

    if fps <= 0:
        print("ERROR: Invalid FPS.")
        video.release()
        return False

    # Store tracking data
    data = []

    frame_number = 0

    # Previous ball position
    previous_center = None

    # Maximum allowed movement between consecutive frames
    max_movement = 250

    # Display size
    max_display_height = 800
    max_display_width = 450

    while True:

        ret, frame = video.read()

        if not ret:
            break

        # ======================================
        # BGR → HSV
        # ======================================

        hsv = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2HSV
        )

        # ======================================
        # RED COLOR
        # ======================================

        lower_red1 = (0, 100, 100)
        upper_red1 = (10, 255, 255)

        lower_red2 = (170, 100, 100)
        upper_red2 = (179, 255, 255)

        mask1 = cv2.inRange(
            hsv,
            lower_red1,
            upper_red1
        )

        mask2 = cv2.inRange(
            hsv,
            lower_red2,
            upper_red2
        )

        mask = mask1 | mask2

        # ======================================
        # CLEAN MASK
        # ======================================

        kernel = cv2.getStructuringElement(
            cv2.MORPH_ELLIPSE,
            (5, 5)
        )

        mask = cv2.morphologyEx(
            mask,
            cv2.MORPH_OPEN,
            kernel
        )

        mask = cv2.morphologyEx(
            mask,
            cv2.MORPH_CLOSE,
            kernel
        )

        # ======================================
        # FIND CONTOURS
        # ======================================

        contours, _ = cv2.findContours(
            mask,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        candidates = []

        for contour in contours:

            area = cv2.contourArea(contour)

            if area < 100:
                continue

            x, y, w, h = cv2.boundingRect(
                contour
            )

            center_x = x + w // 2
            center_y = y + h // 2

            candidates.append({
                "x": center_x,
                "y": center_y,
                "area": area,
                "bbox": (x, y, w, h)
            })

        # ======================================
        # SELECT BALL
        # ======================================

        selected = None

        if candidates:

            # First detection
            if previous_center is None:

                selected = max(
                    candidates,
                    key=lambda c: c["area"]
                )

            else:

                px, py = previous_center

                valid_candidates = []

                for candidate in candidates:

                    cx = candidate["x"]
                    cy = candidate["y"]

                    distance = math.sqrt(
                        (cx - px) ** 2
                        + (cy - py) ** 2
                    )

                    candidate["distance"] = distance

                    if distance <= max_movement:

                        valid_candidates.append(
                            candidate
                        )

                if valid_candidates:

                    selected = min(
                        valid_candidates,
                        key=lambda c: c["distance"]
                    )

        # ======================================
        # SAVE DETECTION
        # ======================================

        if selected is not None:

            center_x = selected["x"]
            center_y = selected["y"]

            x, y, w, h = selected["bbox"]

            time = frame_number / fps

            data.append([
                frame_number,
                time,
                center_x,
                center_y
            ])

            previous_center = (
                center_x,
                center_y
            )

            # Draw bounding box
            cv2.rectangle(
                frame,
                (x, y),
                (x + w, y + h),
                (0, 255, 0),
                3
            )

            # Draw center
            cv2.circle(
                frame,
                (center_x, center_y),
                7,
                (255, 0, 0),
                -1
            )

            # Show coordinates
            cv2.putText(
                frame,
                f"X={center_x}, Y={center_y}",
                (20, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 255, 255),
                2
            )

        # ======================================
        # RESIZE ONLY FOR DISPLAY
        # ======================================

        height, width = frame.shape[:2]

        scale = min(
            max_display_width / width,
            max_display_height / height
        )

        display_width = int(
            width * scale
        )

        display_height = int(
            height * scale
        )

        display_frame = cv2.resize(
            frame,
            (
                display_width,
                display_height
            )
        )

        cv2.imshow(
            "Ball Tracking",
            display_frame
        )

        # Press Q to stop
        if cv2.waitKey(30) & 0xFF == ord("q"):
            break

        frame_number += 1

    # ==========================================
    # RELEASE
    # ==========================================

    video.release()
    cv2.destroyAllWindows()

    # ==========================================
    # CREATE DATAFRAME
    # ==========================================

    df = pd.DataFrame(
        data,
        columns=[
            "Frame",
            "Time",
            "X_pixel",
            "Y_pixel"
        ]
    )

    # ==========================================
    # SAVE CSV
    # ==========================================

    output_folder = os.path.dirname(
        output_csv
    )

    if output_folder:
        os.makedirs(
            output_folder,
            exist_ok=True
        )

    df.to_csv(
        output_csv,
        index=False
    )

    print(
        f"Tracking completed: {output_csv}"
    )

    print(
        f"Detected points: {len(df)}"
    )

    return True