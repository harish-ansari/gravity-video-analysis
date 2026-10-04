import os

from video_tracker import track_video
from gravity_calculation import calculate_gravity


VIDEO_FOLDER = "videos"
DATA_FOLDER = "data"

os.makedirs(
    DATA_FOLDER,
    exist_ok=True
)

results = []


# ==========================================
# 5 TRIALS
# ==========================================

for trial in range(1, 4):

    video_file = (
        f"{VIDEO_FOLDER}/trial_{trial}.mp4"
    )

    csv_file = (
        f"{DATA_FOLDER}/trial_{trial}.csv"
    )

    print("\n")
    print("=" * 50)
    print(f"TRIAL {trial}")
    print("=" * 50)

    # ======================================
    # CHECK VIDEO
    # ======================================

    if not os.path.exists(video_file):

        print(
            f"Trial {trial}: video not found"
        )

        continue

    # ======================================
    # TRACK VIDEO
    # ======================================

    print(
        "Starting video tracking..."
    )

    success = track_video(
        video_file,
        csv_file
    )

    if not success:

        print(
            f"Trial {trial}: tracking failed"
        )

        continue

    # ======================================
    # CALCULATE GRAVITY
    # ======================================

    print(
        "Calculating gravity..."
    )

    result = calculate_gravity(
        csv_file
    )

    if result is None:

        print(
            f"Trial {trial}: calculation failed"
        )

        continue

    # ======================================
    # RESULTS
    # ======================================

    g = result["g"]
    error = result["percentage_error"]
    r2 = result["r_squared"]

    results.append({
        "Trial": trial,
        "g": g,
        "Error": error,
        "R2": r2
    })

    print("\nTrial Result")
    print("-" * 30)

    print(
        f"g = {g:.4f} m/s²"
    )

    print(
        f"Error = {error:.2f}%"
    )

    print(
        f"R² = {r2:.5f}"
    )


# ==========================================
# FINAL RESULTS
# ==========================================

print("\n")
print("=" * 60)
print("FINAL EXPERIMENT RESULTS")
print("=" * 60)

if len(results) == 0:

    print("No successful trials.")

else:

    for result in results:

        print(
            f"Trial {result['Trial']}: "
            f"g = {result['g']:.4f} m/s² | "
            f"Error = {result['Error']:.2f}% | "
            f"R² = {result['R2']:.5f}"
        )