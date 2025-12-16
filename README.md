# User Funnel Analysis (End-to-End Product Analytics)

This project analyzes user behavior across a product funnel — from signup to checkout — to identify drop-offs, conversion issues, and actionable product insights.

The analysis is performed using SQL for data extraction, Excel for validation and summaries, and Power BI for interactive visualization.

---

## 🔍 Business Problem

Users are signing up but not completing checkout.

Key questions:
- Where do users drop off in the funnel?
- Does conversion differ by device?
- Are some cities experiencing higher checkout friction?
- Is the issue discovery-related or checkout-related?

---

## 🧱 Funnel Stages

1. Signup  
2. Product View  
3. Add to Cart  
4. Checkout  

---

## 🗂️ Project Structure

user-funnel-analysis/
│
├── data/
│ └── events.csv
│
├── sql/
│ └── funnel_analysis.sql
│
├── excel/
│ └── Funnel_Analysis.xlsx
│
├── powerbi/
│ └── User_Funnel_Analysis.pbix
│
├── screenshots/
│ ├── funnel.png
│ ├── city_conversion.png
│ └── device_conversion.png
│
└── README.md

pgsql
Copy code

---

## 🧠 Key Insights

- **Checkout is the biggest drop-off point**  
  ~40% of users drop at checkout, significantly higher than earlier funnel stages.

- **Mobile users convert worse than desktop**  
  Mobile checkout conversion (~40%) is much lower than desktop (~60%), indicating mobile UX or payment friction.

- **Tier-1 cities show higher checkout friction**  
  Cities like Mumbai and Bangalore have lower checkout conversion compared to smaller cities, suggesting congestion, payment latency, or trust issues.

- **Product View → Add to Cart is healthy**  
  The major problem is not product discovery, but checkout completion.

---

## 🛠 Product Recommendations

- Simplify mobile checkout  
  - Reduce form fields  
  - Enable one-tap payments (UPI, saved cards)

- Optimize checkout performance in Tier-1 cities  
  - Payment retries  
  - Faster API response monitoring

- Introduce checkout nudges  
  - “Complete purchase in 1 step”  
  - Trust badges and delivery assurance

- Improve late-stage analytics  
  - Track payment failure reasons  
  - Add checkout error logging

---

## 🧰 Tools Used

- **SQL** — Funnel aggregation and user-level analysis  
- **Excel** — Funnel summary, conversion %, drop-offs, insights  
- **Power BI** — Funnel visualization and city/device breakdown  

---

## 📌 Notes

- Power BI `.pbix` file may not render directly on GitHub; screenshots are provided for reference.
- This project focuses on decision-making insights, not just metric reporting.

---

## 👤 Author

Akshika Rawat  
