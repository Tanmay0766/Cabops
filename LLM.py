import os
import json
import time

from dotenv import load_dotenv
from google import genai
from google.genai import types

def get_api_key():

    api_key = os.getenv("GEMINI_API_KEY")

    if api_key:
        return api_key

    try:
        import streamlit as st

        return st.secrets.get("GEMINI_API_KEY")

    except Exception:
        return None

def analyze(incident, metrics, system_prompt):

    load_dotenv(override=True)

    api_key = get_api_key()

    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is missing. Add it to your .env file locally or Streamlit secrets online."
        )

    client = genai.Client(api_key=api_key)

    prompt = f"""
{system_prompt}

=============================
INCIDENT DATA
=============================

{json.dumps(incident, indent=2)}

=============================
PRE-CALCULATED METRICS
=============================

{json.dumps(metrics, indent=2)}

IMPORTANT:

Use the metrics provided.

Do NOT recalculate them.

Only make operational decisions.

Return ONLY JSON.
"""

    retries = 3
    last_error = None

    for _ in range(retries):

        try:

            response = client.models.generate_content(
        
                model="gemini-2.5-flash",

                contents=prompt,

                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    temperature=0.3
                )

            )

            return response.text

        except Exception as exc:

            last_error = exc
            time.sleep(2)

    raise RuntimeError(f"Gemini API unavailable: {last_error}") from last_error
