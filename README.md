# CabOps AI

CabOps AI is a Streamlit app for handling cab operations incidents such as driver absence, vehicle breakdowns, bad weather, and backup capacity shortages. It calculates operational metrics, sends the incident context to Gemini, and returns a structured incident response with priority, dispatch strategy, impact, ready-to-send messages, and manual decision points.

# Demo:





## Features

- Incident input form for route, client, driver absence, weather, breakdown details, and employee counts
- Pre-calculated operational metrics before the AI step
- Risk score and priority classification
- Gemini-powered response generation
- Recommended actions for dispatch and operations teams
- Ready messages for HR, employees, and backup drivers
- Streamlit interface for quick demo usage

## Project Structure

```text
.
|-- app.py              # Streamlit app UI and response display
|-- business_logic.py   # Metric, risk score, delay, and priority calculations
|-- LLM.py              # Gemini API integration
|-- models.py           # Data models
|-- prompt.py           # System prompt and response rules
|-- requirements.txt    # Python dependencies
`-- .gitignore          # Local files excluded from Git
```

## Risk Score

The risk score is calculated before calling Gemini. It gives the app a consistent operational severity signal.

```text
Risk score =
+ 35 if a driver is marked absent
+ 30 if a vehicle breakdown is entered
+ 10 for Rain, or 20 for Heavy Rain
+ 5 for each waiting employee
+ 10 for each employee beyond backup vehicle capacity
```

Priority is then assigned from the score:

```text
80 or more: Critical
60 to 79: High
35 to 59: Medium
Below 35: Low
```

## Requirements

- Python 3.10 or newer
- Gemini API key
- Git

## Local Setup

Clone the repository:

```bash
git clone https://github.com/Tanmay0766/Cabops.git
cd Cabops
```

Create and activate a virtual environment:

```bash
python -m venv .venv
```

On Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

Run the app:

```bash
streamlit run app.py
```

## Usage

1. Enter the incident details in the form.
2. Add the number of employees already picked and still waiting.
3. Enter backup vehicle capacity.
4. Select the weather condition.
5. Add breakdown and client HR message details if available.
6. Click `Analyze Incident`.
7. Review the priority, dispatch strategy, impact, recommended actions, and ready messages.

## Deployment

The easiest demo deployment path is Streamlit Community Cloud.

1. Push this repository to GitHub.
2. Go to `https://share.streamlit.io`.
3. Create a new app from the GitHub repository.
4. Set the main file path to `app.py`.
5. Add `GEMINI_API_KEY` in the app secrets or environment settings.
6. Deploy the app.

## Security Notes

Do not commit your `.env` file or API keys. This project already ignores `.env`, `.venv`, `__pycache__`, and Python bytecode files through `.gitignore`.

## Tech Stack

- Streamlit
- Python
- Google Gemini API
- python-dotenv
