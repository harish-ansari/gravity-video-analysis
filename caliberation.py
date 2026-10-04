import cv2

video = cv2.VideoCapture("videos/trial_1.mp4")

ret, frame = video.read()
video.release()

if not ret:
    print("Video read nahi ho rahi")
    exit()

# Original dimensions
original_height, original_width = frame.shape[:2]

print("Original size:", original_width, "x", original_height)

# ------------------------------------------
# DISPLAY SIZE
# ------------------------------------------

screen_height = 800

# Maintain EXACT 9:16 aspect ratio
scale = screen_height / original_height

display_width = int(original_width * scale)
display_height = int(original_height * scale)

display_frame = cv2.resize(
    frame,
    (display_width, display_height),
    interpolation=cv2.INTER_AREA
)

print(
    "Display size:",
    display_width,
    "x",
    display_height
)

# ------------------------------------------
# CLICK FUNCTION
# ------------------------------------------

def click_event(event, x, y, flags, param):

    if event == cv2.EVENT_LBUTTONDOWN:

        # Convert display coordinates
        # back to original coordinates
        original_x = int(x / scale)
        original_y = int(y / scale)

        print(
            f"Clicked original: "
            f"{original_x} {original_y}"
        )

        # Mark click on display
        cv2.circle(
            display_frame,
            (x, y),
            5,
            (0, 0, 255),
            -1
        )

        cv2.imshow(
            "Calibration",
            display_frame
        )


# ------------------------------------------
# SHOW
# ------------------------------------------

cv2.namedWindow(
    "Calibration",
    cv2.WINDOW_AUTOSIZE
)

cv2.setMouseCallback(
    "Calibration",
    click_event
)

cv2.imshow(
    "Calibration",
    display_frame
)

cv2.waitKey(0)

cv2.destroyAllWindows()