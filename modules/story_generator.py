import openai
import os
from typing import Dict, Any

def generate_story(report: Dict[str, Any], df_desc: str) -> str:
    """Turns data analysis into human-readable story"""
    
    prompt = f"""
    Analyze this data quality report and generate a 3-paragraph executive summary:
    
    Dataset: {df_desc}
    Rows: {report.get('rows', 0):,}
    Columns: {report.get('columns', 0)}
    Missing: {report.get('missing_%', 0):.1f}%
    
    Key Issues:
    {report.get('missing_cols', {})}
    
    Turn this into a professional business story. Focus on:
    1. Data health overview
    2. Critical issues found  
    3. Recommended next steps
    
    Keep it concise (200 words max).
    """
    
    try:
        if not os.getenv("OPENAI_API_KEY"):
            return f"""
**DataMind AI Insights** 🧠

**Overview:** {df_desc} contains {report.get('rows', 0):,} rows across {report.get('columns', 0)} columns.

**Data Health:** {report.get('missing_%', 0):.1f}% missing values detected. {report.get('duplicates', 0)} duplicates found.

**Action Items:**
• Clean missing data in key columns
• Remove duplicates
• Ready for advanced analysis!

**Status:** Premium GPT-4 stories unlocked with API key.
            """
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except:
        return "OpenAI API setup required for live generation"

def test():
    report = {'rows': 1000, 'columns': 12, 'missing_%': 15.2, 
              'missing_cols': {'email': 120, 'phone': 80}}
    return generate_story(report, "Customer database")

print("Story generator ready!")