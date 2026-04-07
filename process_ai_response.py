import json
import sys

try:
    with open('/tmp/ai_response.json') as f:
        data = json.load(f)

    raw = data.get("response", "").strip()

    # Try parsing JSON response
    issues = json.loads(raw)

    critical_found = False

    print("\n=== AI CODE REVIEW ===")

    for i, issue in enumerate(issues, 1):
        print(f"{i}. {issue['issue']}")
        print(f"   Severity: {issue['severity']}")
        print(f"   Fix: {issue['fix']}\n")

        if issue['severity'].lower() == "critical":
            critical_found = True

    print("======================\n")

    # Save structured report
    with open("reports/ai_review.json", "w") as f:
        json.dump(issues, f, indent=2)

    if critical_found:
        print("❌ Critical issues found!")
        sys.exit(1)

except Exception as e:
    print("❌ Error processing AI response:", str(e))
    sys.exit(1)
