import json
from datetime import datetime

with open("reports/ai_review.json") as f:
    issues = json.load(f)

html = f"""
<html>
<head>
<title>AI Code Review</title>
<style>
body {{ font-family: Arial; }}
.critical {{ color: red; }}
.high {{ color: orange; }}
.medium {{ color: blue; }}
.low {{ color: green; }}
</style>
</head>
<body>

<h1>AI Code Review Report</h1>
<p>Generated: {datetime.now()}</p>

<table border="1" cellpadding="10">
<tr><th>Issue</th><th>Severity</th><th>Fix</th></tr>
"""

for issue in issues:
    severity = issue['severity'].lower()
    html += f"<tr class='{severity}'>"
    html += f"<td>{issue['issue']}</td>"
    html += f"<td>{issue['severity']}</td>"
    html += f"<td>{issue['fix']}</td>"
    html += "</tr>"

html += "</table></body></html>"

with open("reports/ai_report.html", "w") as f:
    f.write(html)
