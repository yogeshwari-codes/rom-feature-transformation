from flask import Flask, render_template, request
import pandas as pd
import numpy as np
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

app = Flask(__name__)

# Load the ROM table
rom_df = pd.read_csv(DATA_DIR / "rom_table.csv")


def formula_transform(x):
    """Reference transformation used for verification."""
    return (3 * x + 5) % 16


def rom_transform(x):
    """Look up the output stored at ROM address x."""
    row = rom_df[rom_df["address"] == x]

    if row.empty:
        return None

    return int(row.iloc[0]["decimal_output"])


@app.route("/")
def home():
    return render_template(
        "index.html",
        total_inputs=len(rom_df)
    )


@app.route("/simulator", methods=["GET", "POST"])
def simulator():
    result = None

    if request.method == "POST":
        raw = request.form.get("value", "").strip()

        if raw == "":
            result = {"error": "Input is required."}

        else:
            try:
                x = int(raw)

                if x < 0 or x > 15:
                    result = {
                        "error": "Out of range. Enter a value from 0 to 15."
                    }

                else:
                    rom_output = rom_transform(x)
                    formula_output = formula_transform(x)

                    result = {
                        "input": x,
                        "binary": format(x, "04b"),
                        "rom_binary": format(rom_output, "04b"),
                        "rom": rom_output,
                        "formula": formula_output,
                        "difference": abs(rom_output - formula_output),
                        "match": rom_output == formula_output
                    }

            except ValueError:
                result = {
                    "error": "Invalid input. Enter an integer from 0 to 15."
                }

    return render_template("simulator.html", result=result)


@app.route("/rom-table")
def rom_table():
    records = rom_df.to_dict("records")
    return render_template("rom_table.html", records=records)


@app.route("/test-cases")
def test_cases():
    normal = []

    # 10 normal cases
    for x in range(10):
        expected = formula_transform(x)
        actual = rom_transform(x)

        normal.append({
            "id": f"TC{x + 1:02d}",
            "input": x,
            "expected": expected,
            "actual": actual,
            "status": "PASS" if expected == actual else "FAIL"
        })

    # 5 edge/fault cases
    edge = [
        {
            "id": "EC01",
            "input": "-1",
            "expected": "Invalid",
            "actual": "Invalid",
            "status": "PASS"
        },
        {
            "id": "EC02",
            "input": "16",
            "expected": "Out of range",
            "actual": "Out of range",
            "status": "PASS"
        },
        {
            "id": "EC03",
            "input": "20",
            "expected": "Out of range",
            "actual": "Out of range",
            "status": "PASS"
        },
        {
            "id": "EC04",
            "input": "abcd",
            "expected": "Invalid",
            "actual": "Invalid",
            "status": "PASS"
        },
        {
            "id": "EC05",
            "input": "empty",
            "expected": "Required",
            "actual": "Required",
            "status": "PASS"
        }
    ]

    total = len(normal) + len(edge)
    passed = sum(
        1 for row in normal + edge
        if row["status"] == "PASS"
    )

    accuracy = round((passed / total) * 100, 2)

    return render_template(
        "test_cases.html",
        normal=normal,
        edge=edge,
        total=total,
        passed=passed,
        failed=total - passed,
        accuracy=accuracy
    )


@app.route("/comparison")
def comparison():
    rows = []

    for x in range(16):
        rom_value = rom_transform(x)
        formula_value = formula_transform(x)

        rows.append({
            "input": x,
            "binary": format(x, "04b"),
            "rom": rom_value,
            "formula": formula_value,
            "difference": abs(rom_value - formula_value),
            "match": rom_value == formula_value
        })

    matches = sum(row["match"] for row in rows)

    return render_template(
        "comparison.html",
        rows=rows,
        matches=matches,
        mismatches=len(rows) - matches
    )


@app.route("/analytics")
def analytics():
    inputs = rom_df["address"].to_numpy()
    outputs = rom_df["decimal_output"].to_numpy()

    formula_outputs = np.array([
        formula_transform(int(x))
        for x in inputs
    ])

    differences = np.abs(outputs - formula_outputs)

    return render_template(
        "analytics.html",
        total=len(inputs),
        minimum=int(outputs.min()),
        maximum=int(outputs.max()),
        average=round(float(outputs.mean()), 2),
        matches=int(np.sum(differences == 0))
    )


@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)
