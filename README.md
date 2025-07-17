***Damoov_Diving_Score***

This branch contains FastAPI endpoints for driving performance and safety dashboard summaries.
It integrates existing score pipeline logic and ensures all metrics are calculated per unique trip.

✅ Features
Performance Summary API
/performance_summary
→ Returns new drivers, active drivers, trip count, mileage, time-driven.

Safe Driving Summary API
/safe_driving_summary
→ Returns safety score, acceleration, braking, cornering, speeding, phone usage scores.

Eco Driving Summary API
/eco_driving_summary
→ Returns eco score, brake score, tire score, fuel score.

Safety Dashboard Summary API
/safety_dashboard_summary

→ Combines key metrics:
Safety score, trips, drivers, mileage, driving time, average & max speed (in km/h),
phone usage %, speeding %, combined % (phone + speeding), unique tags count.

🔧 Setup Instructions
Clone repository and checkout this branch:
git checkout feature/api-dashboard

Install required packages:

pip install fastapi uvicorn pandas sqlite3

Run the API server:--

uvicorn performance_metrics:app --reload

Test APIs locally using Postman or Swagger UI.

📊 Notes:--

Speeds are reported in km/h as per latest project guidelines.
All APIs use SQLite sample table (SampleTable) for demonstration.
Filtering applies by time range: last_1_week, last_2_weeks, last_1_month, last_2_months.