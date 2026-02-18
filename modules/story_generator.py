import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv() # Load variables from .env file

def generate_story(report, df_desc):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    prompt = f"""
    Analyze this data quality report and generate a 3-paragraph executive summary:
    Dataset: {df_desc}
    Rows: {report.get('rows', 0):,}
    Columns: {report.get('columns', 0)}
    Missing: {report.get('missing_%', 0):.1f}%
    Key Issues: {report.get('missing_cols', {})}
    
    1. Data health overview | 2. Critical issues | 3. Next steps
    """

    if not os.getenv("OPENAI_API_KEY"):
        return "⚠️ API Key missing. Please add it to your .env file."

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo", # Or "gpt-4" as planned
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ Error: {str(e)}"