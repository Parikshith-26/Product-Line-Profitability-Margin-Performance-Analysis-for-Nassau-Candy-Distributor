# 📊 Profitability Analytics Dashboard

**Live App:** https://profitability-analytics-dashboard.streamlit.app/

An interactive Business Intelligence dashboard built using **Streamlit, Pandas, and Plotly** to analyze product-level profitability, margin risks, and revenue concentration patterns.

This project demonstrates real-world analytics workflow: data preparation → KPI engineering → interactive visualization → decision insights.

---

## 🚀 Features

### 🔎 Interactive Filters

* Date range selector
* Division filter
* Margin threshold slider
* Product search

### 📈 Product Profitability Analysis

* Product margin leaderboard
* Profit contribution visualization
* Margin volatility detection
* Volatility risk classification

### 🏢 Division Performance

* Revenue vs Profit comparison
* Margin distribution analysis by division

### ⚠️ Cost Diagnostics

* Cost vs Sales scatter plot
* Dynamic risk flagging (based on margin threshold)

### 📊 Profit Concentration Analysis

* Dual-axis Pareto chart
* Top 20% dependency indicator
* Concentration risk detection

### 🤖 Automated Insights

The dashboard automatically generates executive-level commentary:

* Best performing division
* Weakest margin product
* High-risk product count
* Profit concentration risk
* Margin instability warning

### 📥 Data Export

Download filtered dataset directly as CSV.

---

## 🧠 Key KPIs Used

| KPI                  | Definition                    |
| -------------------- | ----------------------------- |
| Gross Profit         | Sales − Cost                  |
| Gross Margin (%)     | Gross Profit ÷ Sales          |
| Profit per Unit      | Gross Profit ÷ Units          |
| Revenue Contribution | Product Sales ÷ Total Sales   |
| Profit Contribution  | Product Profit ÷ Total Profit |
| Margin Volatility    | Std Dev of Margin over time   |

---

## 🛠 Tech Stack

* **Python**
* **Streamlit**
* **Pandas**
* **Plotly**
* **OpenPyXL**

---

## 📂 Project Structure

```
app.py
nassau_clean.xlsx
requirements.txt
README.md
```

---

## 💡 Business Value

This dashboard helps decision-makers:

* Identify profitable vs risky products
* Detect dependency on few products
* Monitor margin stability
* Evaluate division performance
* Support pricing and cost optimization strategies

---

## ▶️ Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

---

## 📌 Author

Analytics portfolio project demonstrating practical BI dashboard development and business insight generation using Python.

---
