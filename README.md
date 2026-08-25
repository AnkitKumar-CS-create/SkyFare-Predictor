cat << 'EOF' > README.md

# ✈️ SkyFare Predictor: Flight Price ML Model

Predicts Indian domestic flight fares from trip details, served as an interactive Streamlit app on top of a tuned Random Forest model.

## Overview

Airline ticket prices move around a lot — they depend on the carrier, the route, the number of stops, the time of year, and how far ahead you book. This project takes a historical flight-fare dataset (the MachineHack-style Indian domestic flights data), works through the usual end-to-end machine learning pipeline, and lands on a regression model that estimates a fair price for a given trip.

The whole thing is wrapped in a Streamlit web app so you don't have to touch the notebook to use it. You pick an airline, source, destination, a booking date, ticket type, passenger counts and stop preference, hit Predict, and it returns an estimated fare with a bit of pricing logic layered on top. The notebook (`Price_Detection.ipynb`) does the heavy lifting: EDA, feature engineering, comparing four model families, and hyperparameter tuning. The tuned Random Forest Regressor came out best at roughly R² 0.85 on the test split and is the model that ships in the app.

This was built as an end-to-end ML learning/portfolio project, and it ships with the trained model, the app, and a full folder of design documents plus a demo video.

## Key Features

- **End-to-end regression pipeline** — raw CSV data through cleaning, feature engineering, model comparison, tuning, and a saved model artifact.
- **Four model families compared** — Linear Regression, Random Forest Regressor, Support Vector Regressor, and Polynomial Regression (degree 2 and 3), evaluated on the same 80/20 split.
- **Hyperparameter tuning** — GridSearchCV over the Random Forest, with the best parameters fixed and the fitted model persisted to `model/best_model.pkl`.
- **Interactive Streamlit app** — dropdowns for airline / origin / destination, a date picker, ticket-type select, adult and child counts, and a max-stops input, all styled with custom CSS (teal #00ADB5 theme).
- **Pricing logic on top of the model** — the raw model output is adjusted with real booking rules, not just returned as-is.
  - _Per-passenger fare_ — the predicted base fare is multiplied across the number of adults and children.
  - _Business-class surcharge_ — a 25% markup is applied when "Business" is selected instead of "Economy".
  - _Last-minute surge_ — if the booking date is less than a day out, the fare is doubled.
- **Airline price comparison chart** — a bar chart of price by airline rendered straight from the training data so you can see how carriers stack up.
- **Codespaces-ready** — a `.devcontainer/devcontainer.json` that installs requirements and auto-launches the Streamlit app on port 8501.

## How It Works

### Data and preprocessing

The dataset lives in `train/Data_Train.csv` and `test/Test_set.csv`. Each row is a flight with an airline, source, destination, route, departure/arrival times, duration, number of stops, additional info, and the target Price.
Preprocessing in the notebook:

- Missing values are filled with the most frequent value in each column.
- Date features — the date of journey is split into separate Day, Month, and Year columns so the model can pick up seasonal effects.
- Categorical encoding — Airline, Source, Destination, and Additional_Info are label-mapped to integers (the exact same maps are hard-coded in the app so user input is encoded identically to training).
- Duration is converted into a single numeric total (hours).
- Dropped columns — Route, Dep_Time, and Arrival_Time are removed to keep the feature set simple.

### Model training and selection

Everything is trained on an 80/20 train-test split and scored mainly with R². Random Forest was the clear winner (~0.85 R²), so it got a GridSearchCV pass. The fitted estimator is pickled to `model/best_model.pkl` (~15 MB) and that's the file the app loads at startup.

### The Streamlit app

`app.py` is the deployment layer. On load it unpickles `best_model.pkl`, applies a custom CSS block for the teal theme, and renders a two-column input form. When you click Predict it:

1. Maps your selections to the same integer codes used in training.
2. Builds a single-row DataFrame with the encoded inputs.
3. Calls `best_model.predict(...)` to get a base fare.
4. Applies the pricing rules (passenger count, business class markup, last-minute surge).
5. Shows the final fare and renders the airline-vs-price comparison bar chart underneath.

## Results / Highlights

- **Tuned Random Forest Regressor** — R² ≈ 0.85 on the test split, the best of four model families tried.
- Comfortably beat the linear baseline (R² ≈ 0.38) and polynomial (≈ 0.57).
- GridSearchCV-tuned hyperparameters fixed and the trained model shipped as a ~15 MB pickle for instant serving.
- Shipped as a working interactive app, not just a notebook.

## Tech Stack

- **Language:** Python 3.x
- **Data / ML:** scikit-learn, pandas, NumPy, xgboost
- **Visualization:** matplotlib, seaborn, Streamlit
- **App / UI:** Streamlit (custom CSS)
- **Tooling:** Jupyter Notebook, VS Code Dev Container

## Getting Started

### Prerequisites

- Python 3.x
- pip

### Usage

- Run streamlit run app.py.

- Pick your airline, origin, and destination from the dropdowns.

- Choose a booking date (must be today or later), set ticket type, enter adult and child counts, and set your max number of stops.

- Hit Predict — you'll get the estimated total fare (per-passenger, with surcharges applied) and a comparison chart.

### Project Structure

SkyFare-Predictor/
├── app.py # Streamlit app: form, encoding, prediction, pricing logic, chart
├── Price_Detection.ipynb # EDA, feature engineering, model comparison, GridSearchCV tuning
├── requirements.txt # dependencies
├── model/
│ └── best_model.pkl # Tuned Random Forest, persisted (~15 MB)
├── train/
│ ├── Data_Train.csv # Training data
│ └── Data_Train.xlsx
├── test/
│ ├── Test_set.csv # Test data
│ └── Test_set.xlsx
├── Sample_submission.csv # Expected output format
├── Sample_submission.xlsx
├── documents/
│ ├── Flight_Arch.docx # Architecture document
│ ├── Flight_HLD.docx # High-level design
│ ├── Flight_LLD.docx # Low-level design
│ ├── Flight_WF.docx # Workflow document
│ ├── Flight_Pro_Rep.pptx # Project report deck
│ └── Flight Prediction.mp4 # Demo video
├── .devcontainer/
│ └── devcontainer.json # Codespaces config
└── README.md

### Contact

Ankit Kumar | B.Tech CSE (Bioinformatics), Vellore Institute of Technology | GitHub: AnkitKumar-CS-create | Email: kumarankit9431780451@gmail.com

Made by Ankit Kumar
EOF

### Installation

```bash
git clone [https://github.com/AnkitKumar-CS-create/SkyFare-Predictor.git](https://github.com/AnkitKumar-CS-create/SkyFare-Predictor.git)
cd SkyFare-Predictor
pip install -r requirements.txt
```
