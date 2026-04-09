import json
import sys

# Read diff
with open('/tmp/code_diff.txt') as f:
    diff = f.read(4000)


prompt = f"""Act as a senior DevSecOps engineer.

Analyze this code diff for:
- Bugs
- Security issues (OWASP Top 10)
- Hardcoded secrets
- Performance issues

Return STRICT JSON like:
[
  {{
    "issue": "...",
    "severity": "Low/Medium/High/Critical",
    "fix": "..."
  }}
]

Code:
{diff}
"""

payload = {
    "model": "qwen2.5-coder:latest",
    "prompt": prompt,
    "stream": False
}

# Save payload
with open('/tmp/ai_payload.json', 'w') as f:
    json.dump(payload, f)
