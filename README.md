# Flight Price Prediction

**Predicts Indian domestic flight fares from trip details, served as an interactive Streamlit app on top of a tuned Random Forest model.**

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white) ![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=flat&logo=scikit-learn&logoColor=white) ![pandas](https://img.shields.io/badge/pandas-150458?style=flat&logo=pandas&logoColor=white) ![NumPy](https://img.shields.io/badge/NumPy-013243?style=flat&logo=numpy&logoColor=white) ![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white) ![Jupyter](https://img.shields.io/badge/Jupyter-F37626?style=flat&logo=jupyter&logoColor=white)

## Overview

Airline ticket prices move around a lot — they depend on the carrier, the route, the number of stops, the time of year, and how far ahead you book. This project takes a historical flight-fare dataset (the MachineHack-style Indian domestic flights data), works through the usual end-to-end machine learning pipeline, and lands on a regression model that estimates a fair price for a given trip.

The whole thing is wrapped in a Streamlit web app so you don't have to touch the notebook to use it. You pick an airline, source, destination, a booking date, ticket type, passenger counts and stop preference, hit **Predict**, and it returns an estimated fare with a bit of pricing logic layered on top. The notebook (`Price_Detection.ipynb`) does the heavy lifting: EDA, feature engineering, comparing four model families, and hyperparameter tuning. The tuned **Random Forest Regressor** came out best at roughly **R² 0.85** on the test split and is the model that ships in the app.

This was built as an end-to-end ML learning/portfolio project (it maps to an iNeuron.ai ML internship), and it's one of the more complete builds in the set — it ships with the trained model, the app, and a full folder of design documents plus a demo video.

## Key Features

- **End-to-end regression pipeline** — raw CSV data through cleaning, feature engineering, model comparison, tuning, and a saved model artifact.
- **Four model families compared** — Linear Regression, Random Forest Regressor, Support Vector Regressor, and Polynomial Regression (degree 2 and 3), evaluated on the same 80/20 split.
- **Hyperparameter tuning** — `GridSearchCV` over the Random Forest, with the best parameters fixed and the fitted model persisted to `model/best_model.pkl`.
- **Interactive Streamlit app** — dropdowns for airline / origin / destination, a date picker, ticket-type select, adult and child counts, and a max-stops input, all styled with custom CSS (teal `#00ADB5` theme).
- **Pricing logic on top of the model** — the raw model output is adjusted with real booking rules (see below), not just returned as-is.
- **Per-passenger fare** — the predicted base fare is multiplied across the number of adults and children.
- **Business-class surcharge** — a 25% markup is applied when "Business" is selected instead of "Economy".
- **Last-minute surge** — if the booking date is less than a day out, the fare is doubled.
- **Airline price comparison chart** — a bar chart of price by airline rendered straight from the training data so you can see how carriers stack up.
- **Design documentation** — a `documents/` folder with architecture, HLD, LLD, and workflow docs, a project report slide deck, and a recorded demo video.
- **Codespaces-ready** — a `.devcontainer/devcontainer.json` that installs requirements and auto-launches the Streamlit app on port 8501.

## How It Works

### Data and preprocessing

The dataset lives in `train/Data_Train.csv` and `test/Test_set.csv` (both also provided as `.xlsx`), plus a `Sample_submission` file. Each row is a flight with an airline, source, destination, route, departure/arrival times, duration, number of stops, additional info, and the target `Price`.

Preprocessing in the notebook:

- **Missing values** are filled with the most frequent value in each column.
- **Date features** — the date of journey is split into separate **Day**, **Month**, and **Year** columns so the model can pick up seasonal effects.
- **Categorical encoding** — Airline, Source, Destination, and Additional_Info are label-mapped to integers (the exact same maps are hard-coded in the app so user input is encoded identically to training).
- **Duration** is converted into a single numeric total (hours).
- **Dropped columns** — Route, Dep_Time, and Arrival_Time are removed to keep the feature set simple, since their signal is largely captured by stops, duration, and the date features.

### Model training and selection

Everything is trained on an 80/20 train-test split and scored mainly with R². The notebook compares:

| Model | Test R² (approx.) |
|---|---|
| Linear Regression | 0.383 |
| Polynomial Regression (deg 2/3) | 0.565 |
| Support Vector Regressor | negative (~-0.03) |
| **Random Forest Regressor (tuned)** | **~0.85** |

Random Forest was the clear winner, so it got a `GridSearchCV` pass. The best parameters found:

```
{
  'n_estimators': 200,
  'min_samples_split': 5,
  'min_samples_leaf': 1,
  'max_features': 'log2',
  'max_depth': 20
}
```

The fitted estimator is pickled to `model/best_model.pkl` (~15 MB) and that's the file the app loads at startup — no retraining needed to serve predictions.

### The Streamlit app

`app.py` is the deployment layer. On load it unpickles `best_model.pkl`, applies a custom CSS block for the teal theme, and renders a two-column input form. When you click **Predict** it:

1. Maps your selections to the same integer codes used in training (airline / source / destination / additional-info dictionaries live in the app).
2. Builds a single-row `DataFrame` with the encoded inputs plus the split-out Day / Month / Year.
3. Calls `best_model.predict(...)` to get a base fare.
4. Applies the pricing rules — multiply by passenger count, add 25% for business class, and double the total if the trip is booked less than a day out.
5. Shows the final fare (with a `st.balloons()` celebration on success) and renders the airline-vs-price comparison bar chart underneath.

### Pricing logic, concretely

The model predicts a single base fare; the app turns that into a usable total:

```
base = model.predict(inputs)
if Business:  base *= 1.25            # business-class surcharge
fare = base * (adults + children)     # per-passenger
if days_until_travel < 1: fare *= 2   # last-minute surge
```

This is the part that takes it from "a regression score" to something that behaves a little more like a real fare quote.

## Results / Highlights

- **Tuned Random Forest Regressor — R² ≈ 0.85** on the test split, the best of four model families tried.
- Comfortably beat the linear baseline (R² ≈ 0.38) and polynomial (≈ 0.57); SVR didn't work for this data (negative R²).
- `GridSearchCV`-tuned hyperparameters fixed and the trained model shipped as a ~15 MB pickle for instant serving.
- Trained on the full Indian domestic flights dataset (~10k+ rows across 12 airlines and several routes).
- Shipped as a working interactive app, not just a notebook — plus a complete set of SDLC design docs and a recorded demo.

## Tech Stack

- **Language:** Python 3.x
- **Data / ML:** scikit-learn (Random Forest, SVR, Linear/Polynomial regression, GridSearchCV), pandas, NumPy
- **Visualization:** matplotlib, seaborn, Streamlit's built-in charts
- **App / UI:** Streamlit (custom CSS)
- **Tooling:** Jupyter Notebook, VS Code Dev Container / GitHub Codespaces

## Getting Started

### Prerequisites
- Python 3.x (3.11 is what the dev container uses)
- pip

### Installation
```bash
git clone https://github.com/DCode-v05/Flight-Price-Prediction.git
cd Flight-Price-Prediction
pip install -r requirements.txt
```

`requirements.txt` covers pandas, numpy, scikit-learn, xgboost, matplotlib, seaborn, and streamlit.

### Running
```bash
# launch the web app (loads the pre-trained model)
streamlit run app.py
```

The app opens on `http://localhost:8501`. To explore or retrain the models instead:

```bash
jupyter notebook Price_Detection.ipynb
```

If you open the repo in a GitHub Codespace, the dev container installs the requirements and starts the Streamlit server for you automatically.

## Usage

1. Run `streamlit run app.py`.
2. Pick your **airline**, **origin**, and **destination** from the dropdowns.
3. Choose a **booking date** (must be today or later), set **ticket type** (Economy / Business), enter **adult** and **child** counts, and set your **max number of stops**.
4. Optionally pick an **additional info** tag (meal, baggage, layover, etc.).
5. Hit **Predict** — you'll get the estimated total fare (per-passenger, with the business surcharge and last-minute surge applied where relevant) and a chart comparing average price across airlines.

The notebook is the place to go if you want to see the EDA, the model comparison, the correlation heatmap, the prediction-accuracy plots, or to retrain and re-export the model.

## Project Structure

```
Flight-Price-Prediction/
├── app.py                    # Streamlit app: form, encoding, prediction, pricing logic, chart
├── Price_Detection.ipynb     # EDA, feature engineering, model comparison, GridSearchCV tuning
├── requirements.txt          # pandas, numpy, scikit-learn, xgboost, matplotlib, seaborn, streamlit
├── model/
│   └── best_model.pkl        # Tuned Random Forest, persisted (~15 MB)
├── train/
│   ├── Data_Train.csv        # Training data
│   └── Data_Train.xlsx
├── test/
│   ├── Test_set.csv          # Test data
│   └── Test_set.xlsx
├── Sample_submission.csv     # Expected output format
├── Sample_submission.xlsx
├── documents/
│   ├── Flight_Arch.docx      # Architecture document
│   ├── Flight_HLD.docx       # High-level design
│   ├── Flight_LLD.docx       # Low-level design
│   ├── Flight_WF.docx        # Workflow document
│   ├── Flight_Pro_Rep.pptx   # Project report deck
│   └── Flight Prediction.mp4 # Demo video
├── .devcontainer/
│   └── devcontainer.json     # Codespaces config (auto-runs Streamlit on :8501)
└── README.md
```

---

## Contact

<table>
  <tr><td><b>Portfolio:</b> <a href="https://www.denistan.me">Denistan</a></td><td><b>LinkedIn:</b> <a href="https://www.linkedin.com/in/denistanb">denistanb</a></td></tr>
  <tr><td><b>GitHub:</b> <a href="https://github.com/DCode-v05">DCode-v05</a></td><td><b>LeetCode:</b> <a href="https://leetcode.com/u/Denistan_B">Denistan_B</a></td></tr>
  <tr><td colspan="2" align="center"><b>Email:</b> <a href="mailto:denistanb05@gmail.com">denistanb05@gmail.com</a></td></tr>
</table>

Made with ❤️ by **Denistan B**
