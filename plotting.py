import pandas as pd
import numpy as np
import os


DATA_FOLDER = "data"

theoretical_g = 9.81

results = []


# =====================================
# READ ALL 3 TRIALS
# =====================================

for trial in range(1, 4):

    file = f"{DATA_FOLDER}/trial_{trial}_processed.csv"

    df = pd.read_csv(file)

    time = df["Time"].values
    displacement = df["Displacement_m"].values

    time_squared = time ** 2

    # s = a(t²) + b(t)
    A = np.column_stack((time_squared, time))

    coefficients, _, _, _ = np.linalg.lstsq(
        A,
        displacement,
        rcond=None
    )

    a = coefficients[0]
    b = coefficients[1]

    # g = 2a
    g = 2 * a

    # Predicted displacement
    predicted = a * time_squared + b * time

    # R²
    ss_res = np.sum((displacement - predicted) ** 2)
    ss_tot = np.sum(
        (displacement - np.mean(displacement)) ** 2
    )

    r_squared = 1 - ss_res / ss_tot

    # Percentage error
    error = abs(g - theoretical_g) / theoretical_g * 100

    results.append({
        "Trial": trial,
        "g": g,
        "Error": error,
        "R2": r_squared
    })


# =====================================
# STATISTICS
# =====================================

g_values = np.array([result["g"] for result in results])

mean_g = np.mean(g_values)

standard_deviation = np.std(
    g_values,
    ddof=1
)

minimum_g = np.min(g_values)

maximum_g = np.max(g_values)

range_g = maximum_g - minimum_g

mean_error = abs(
    mean_g - theoretical_g
) / theoretical_g * 100


# =====================================
# FINAL REPORT
# =====================================

print("\n")
print("=" * 70)
print("FINAL EXPERIMENTAL RESULT")
print("=" * 70)

print(
    f"{'Trial':<10}"
    f"{'g (m/s²)':<15}"
    f"{'Error (%)':<15}"
    f"{'R²':<15}"
)

print("-" * 70)

for result in results:

    print(
        f"{result['Trial']:<10}"
        f"{result['g']:<15.4f}"
        f"{result['Error']:<15.2f}"
        f"{result['R2']:<15.5f}"
    )

print("-" * 70)

print(f"Mean g              = {mean_g:.4f} m/s²")

print(
    f"Standard Deviation  = "
    f"{standard_deviation:.4f} m/s²"
)

print(f"Minimum g           = {minimum_g:.4f} m/s²")

print(f"Maximum g           = {maximum_g:.4f} m/s²")

print(f"Range               = {range_g:.4f} m/s²")

print(f"Theoretical g       = {theoretical_g:.2f} m/s²")

print(f"Mean Percentage Error = {mean_error:.2f}%")

print("=" * 70)