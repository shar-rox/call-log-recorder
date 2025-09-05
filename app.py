from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime
import re

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('call_logs.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS calls (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    company TEXT,
                    contact TEXT,
                    summary TEXT,
                    date TEXT,
                    followup TEXT
                )''')
    conn.commit()
    conn.close()

init_db()

def smart_parse(summary):
    contact = None
    company = None
    followup = None

    contact_match = re.search(r"spoke to ([A-Za-z]+)", summary, re.IGNORECASE)
    if contact_match:
        contact = contact_match.group(1)

    # Try multiple patterns for company detection
    company_patterns = [
        r"at ([A-Za-z]+)",  # "at Company"
        r"from ([A-Za-z]+)",  # "from Company"
        r"called ([A-Za-z]+)",  # "called Company"
        r"with ([A-Za-z]+)",  # "with Company"
        r"\b([A-Z][A-Za-z]{2,})\b"  # Single capitalized word (company name)
    ]
    
    for pattern in company_patterns:
        company_match = re.search(pattern, summary)
        if company_match:
            potential_company = company_match.group(1).strip()
            # Filter out common words that aren't companies
            if potential_company.lower() not in ['the', 'and', 'with', 'about', 'regarding', 'spoke', 'called', 'talked', 'john', 'jane', 'mike', 'sarah']:
                company = potential_company
                break

    followup_match = re.search(r"(follow[- ]?up|deadline|due|reminder).*?(on|by|next)? ([A-Za-z0-9]{1,15})", summary, re.IGNORECASE)
    if followup_match:
        followup = followup_match.group(3).strip()

    return company, contact, followup

@app.route('/')
def index():
    company_search = request.args.get('company_search', '')
    followup_search = request.args.get('followup_search', '')
    filter_type = request.args.get('filter_type', 'all')
    
    conn = sqlite3.connect('call_logs.db')
    c = conn.cursor()
    
    # Build the query based on search parameters
    query = "SELECT * FROM calls WHERE 1=1"
    params = []
    
    if company_search:
        query += " AND company LIKE ?"
        params.append(f"%{company_search}%")
    
    if followup_search:
        query += " AND followup LIKE ?"
        params.append(f"%{followup_search}%")
    
    if filter_type == 'upcoming':
        query += " AND followup IS NOT NULL AND followup != ''"
    
    query += " ORDER BY id DESC"
    
    c.execute(query, params)
    logs = c.fetchall()
    conn.close()
    return render_template('index.html', logs=logs)

@app.route('/submit', methods=['POST'])
def submit():
    summary = request.form['summary']
    company, contact, followup = smart_parse(summary)
    date = datetime.now().strftime("%Y-%m-%d %H:%M")

    conn = sqlite3.connect('call_logs.db')
    c = conn.cursor()
    c.execute("INSERT INTO calls (company, contact, summary, date, followup) VALUES (?, ?, ?, ?, ?)",
              (company or '', contact or '', summary, date, followup or ''))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
