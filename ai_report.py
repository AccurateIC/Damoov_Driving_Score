import subprocess, json, urllib.request, sys os
from datetime imporrt dateti

OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://192.168.10.41:11434")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "qwen2.5-coder:latest")
BUILD_NUM = os.environ.get("BUILD_NUMBER", "0")
BUILD_STATUS = sys.argv[1] if len(sys.argv) > 1 else "SUCCESS

def ask_ai(prompt):
    payload = json.dumps({"model": OLLAMA_MODEL, "prompt": prompt, "stream": False}).encode()
    req = urllib.request.Request(f"{OLLAMA_URL}/api/generate",
        data=payload, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read())["response"]
def get_diff():
    try:
        return subprocess.check_output(
            ["git", "diff", "HEAD~1", "HEAD", "--", "."],
            stderr=subprocess.DEVNULL).decode()[:3000]
    except:
        return "No diff available"
diff = get_diff()
review = ask_ai(f"Review this git diff. List bugs, security issues, suggestions. Be concise:\n\n{diff}")
summary = ask_ai("Write a 2-sentence deployment summary for a Node.js frontend + Python backend app deployed to production.")

status_color = "#639922" if BUILD_STATUS == "SUCCESS" else "#E24B4A"
status_label = "Passed" if BUILD_STATUS == "SUCCESS" else "Failed"

html = f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8">
<title>Build #{BUILD_NUM} Report</title>
<style>
  body{{font-family:Arial,sans-serif;max-width:860px;margin:40px auto;padding:0 20px;color:#222;background:#fff}}
  .header{{background:#f5f5f5;border-radius:8px;padding:20px;margin-bottom:20px;display:flex;justify-content:space-between;align-items:center}}
  .badge{{padding:4px 14px;border-radius:6px;font-size:13px;font-weight:600;background:{"#EAF3DE" if BUILD_STATUS=="SUCCESS" else "#FCEBEB"};color:{status_color}}}
  .card{{border:1px solid #e5e5e5;border-radius:8px;padding:20px;margin-bottom:16px}}
  .card h3{{font-size:13px;text-transform:uppercase;letter-spacing:0.05em;color:#888;margin:0 0 12px}}
  .ai-box{{background:#f0f7ff;border-left:3px solid #378ADD;border-radius:0 6px 6px 0;padding:14px 16px;font-size:14px;line-height:1.7;white-space:pre-wrap}}
  .meta{{font-size:13px;color:#888;margin-top:6px}}
</style></head><body>
<div class="header">
  <div>
    <div style="font-size:20px;font-weight:600">Damoov — Build #{BUILD_NUM}</div>
    <div class="meta">Production · {datetime.now().strftime("%b %d %Y %H:%M")}</div>
  </div>
  <span class="badge">{status_label}</span>
</div>
<div class="card">
  <h3>AI code reviewer</h3>
  <div class="ai-box">{review}</div>
</div>
<div class="card">
  <h3>Deployment summary</h3>
  <div class="ai-box">{summary}</div>
</div>
</body></html>"""
os.makedirs("reports", exist_ok=True)
path = f"reports/build_{BUILD_NUM}.html"
with open(path, "w") as f:
    f.write(html)
print(f"Report saved: {path}")
