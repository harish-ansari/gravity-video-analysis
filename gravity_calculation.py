import pandas as pd
import numpy as np


def calculate_gravity(csv_file):

    # ==========================================
    # LOAD DATA
    # ==========================================

    df = pd.read_csv(csv_file)

    if len(df) < 3:

        print("ERROR: Not enough tracking points.")

        return None

    # ==========================================
    # EXPERIMENT SETTINGS
    # ==========================================

    FPS = 30.0

    # Latest calibration
    # 130 cm = 1795 pixels

    KNOWN_DISTANCE_M = 1.30
    KNOWN_PIXELS = 1795

    meters_per_pixel = (
        KNOWN_DISTANCE_M
        / KNOWN_PIXELS
    )

    # ==========================================
    # STARTING POSITION
    # ==========================================

    y0 = df.iloc[0]["Y_pixel"]

    # ==========================================
    # TIME
    # ==========================================

    df["Time"] = (
        df["Frame"]
        - df["Frame"].iloc[0]
    ) / FPS

    # ==========================================
    # PIXEL DISPLACEMENT
    # ==========================================

    df["Displacement_pixel"] = (
        df["Y_pixel"] - y0
    )

    # ==========================================
    # PIXEL → METRE
    # ==========================================

    df["Displacement_m"] = (
        df["Displacement_pixel"]
        * meters_per_pixel
    )

    # ==========================================
    # TIME²
    # ==========================================

    df["Time_squared"] = (
        df["Time"] ** 2
    )

    # ==========================================
    # REGRESSION
    # ==========================================

    time = df["Time"].values

    time_squared = df[
        "Time_squared"
    ].values

    displacement = df[
        "Displacement_m"
    ].values

    # s = a*t² + b*t

    A = np.column_stack(
        (
            time_squared,
            time
        )
    )

    coefficients, _, _, _ = np.linalg.lstsq(
        A,
        displacement,
        rcond=None
    )

    a = coefficients[0]
    b = coefficients[1]

    # a = g/2

    g = 2 * a

    # ==========================================
    # PREDICTED VALUES
    # ==========================================

    predicted = (
        a * time_squared
        + b * time
    )

    # ==========================================
    # R²
    # ==========================================

    ss_res = np.sum(
        (displacement - predicted) ** 2
    )

    ss_tot = np.sum(
        (displacement - np.mean(displacement)) ** 2
    )

    if ss_tot == 0:

        r_squared = np.nan

    else:

        r_squared = (
            1
            - ss_res / ss_tot
        )

    # ==========================================
    # PERCENTAGE ERROR
    # ==========================================

    theoretical_g = 9.81

    percentage_error = (
        abs(g - theoretical_g)
        / theoretical_g
        * 100
    )

    # ==========================================
    # SAVE PROCESSED DATA
    # ==========================================

    output_file = csv_file.replace(
        ".csv",
        "_processed.csv"
    )

    df.to_csv(
        output_file,
        index=False
    )

    # ==========================================
    # RETURN
    # ==========================================

    return {
        "g": g,
        "initial_velocity": b,
        "r_squared": r_squared,
        "percentage_error": percentage_error,
        "data": df
    }