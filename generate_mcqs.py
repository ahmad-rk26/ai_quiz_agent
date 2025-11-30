import google.generativeai as genai
import json
import os
import re

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def extract_json(text):
    try:
        match = re.search(r"\[.*\]", text, re.DOTALL)
        if match:
            return json.loads(match.group())
    except:
        pass
    return None

def generate_mcqs(text, num_questions=5):
    if not text:
        return [{"error": "No text provided for MCQ generation."}]

    prompt = f"""
Generate EXACTLY {num_questions} MCQs from the text below.

STRICT RULES:
- Return ONLY a JSON array.
- NO markdown, no backticks.
- Each MCQ must include:
  "question": "",
  "options": ["A", "B", "C", "D"],
  "correct": "A",
  "explanation": ""

TEXT:
{text[:3000]}
"""

    try:
        model = genai.GenerativeModel("gemini-flash-latest")
        response = model.generate_content(prompt)

        output_text = response.text or ""
        mcqs = extract_json(output_text)

        if mcqs is None:
            return [{"error": "Model did not return valid JSON", "raw_output": output_text}]

        return mcqs

    except Exception as e:
        return [{"error": f"MCQ generation failed: {str(e)}"}]
