# AI-Based Crop Planning and Yield Recommendation Platform

A beginner-friendly Streamlit prototype that demonstrates prompt engineering and agriculture decision support.

## Features
- Farmer input form: location, season, soil, pH, NPK, irrigation, area, budget, price
- Rule-based crop suitability ranking
- Smart cultivation schedule template
- Low/typical/high yield scenarios
- Budget, revenue, and profit calculator
- Agriculture chatbot using a small offline knowledge base
- Prompt templates and side-by-side prompt comparison
- Dashboard with crop/yield comparison chart

## Requirements
- Python 3.10 or newer (Python 3.11 recommended)
- Internet is only needed to install packages; the app itself does not require an AI API.

## Setup on Windows
1. Extract the ZIP.
2. Open the `crop_planning_project` folder in VS Code.
3. Open Terminal and create a virtual environment:

   ```bash
   py -3.11 -m venv venv
   ```

4. Activate it:

   ```bash
   .\\venv\\Scripts\\activate
   ```

5. Install dependencies:

   ```bash
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

6. Run the app:

   ```bash
   streamlit run app.py
   ```

7. Streamlit will open the application in your browser. If it does not, open the local URL shown in the terminal.

## Project structure
```text
crop_planning_project/
├── app.py
├── requirements.txt
├── README.md
├── modules/
│   ├── __init__.py
│   ├── crop_recommendation.py
│   ├── input_validation.py
│   └── prompt_generator.py
├── data/
│   └── crop_data.json
└── utils/
    └── __init__.py
```

## How the recommendation works
The current version uses a transparent, hand-built scoring heuristic based on season, soil, pH range, and water availability. It is not a trained machine-learning model. The crop data and economics are illustrative placeholders for a classroom demonstration.

For a real deployment:
- Replace sample requirements with region-specific, verified agricultural data.
- Use soil test reports and local agricultural university / extension guidance.
- Validate yield estimates against historical district-level data.
- Use current market prices and locally verified input costs.
- Add an LLM API only after storing keys in environment variables or Streamlit secrets.
- Do not use chatbot output as the sole basis for pesticide, fertilizer, or other high-impact farming decisions.

## Suggested project presentation
1. Problem statement
2. Target users and objectives
3. Architecture and module flow
4. Prompt engineering approach
5. Demonstration of each feature
6. Limitations and future scope
