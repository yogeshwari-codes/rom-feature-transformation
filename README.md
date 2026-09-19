# ROM-Based Feature Transformation Simulator

## Project
Interactive Flask website for the project:
**ROM-Based Lookup Table for Feature Transformation**

## Core concept
A 4-bit input selects one of 16 ROM addresses.
The stored ROM value is returned as the transformed feature.

## Included synthetic mapping
The sample ROM table follows:

`Y = (3X + 5) mod 16`

If your college/faculty gives a different mapping or formula, replace:
- `data/rom_table.csv`
- `formula_transform()` in `app.py`

## Features
- Home/dashboard
- Interactive simulator
- Complete ROM table
- 10 normal test cases
- 5 edge/fault cases
- ROM vs formula comparison
- Analytics
- Responsive design
- NumPy/Pandas support

## Windows installation

### 1. Install Python
Install Python 3.10 or newer.

During installation, enable:
**Add Python to PATH**

### 2. Open terminal
Open the project folder in VS Code.

### 3. Create virtual environment

`python -m venv venv`

### 4. Activate

`venv\Scripts\activate`

### 5. Install packages

`pip install -r requirements.txt`

### 6. Run

`python app.py`

### 7. Open browser

`http://127.0.0.1:5000`

### 8. Stop server

Press `Ctrl + C`.

## Main pages

- `/` — Home
- `/simulator` — Interactive ROM simulator
- `/rom-table` — ROM lookup table
- `/test-cases` — 10 normal + 5 edge cases
- `/comparison` — ROM/formula verification
- `/analytics` — dashboard
- `/about` — project information
