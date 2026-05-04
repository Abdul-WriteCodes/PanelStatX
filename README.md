#  PanelStatX

<p align="center">
  <img src="Assets/PSX1.png" alt="PanelStatX Logo" width="800"/>
</p>


PanelStatX is a web-based AI-powered panel regression analysis system. 

🤢The Problem

In carrying out panel regression, rsearchers and students struggle with:
- Expensive tools like Stata
- Steep learning curve (R, Python)
- Time-consuming workflows

🤓The Solution

PanelStatX solve this high cost of accessibility and steep technical learning curve problem that comes with Stata, R and Python. is built as a no-code statistical analysis system that let users:
- Upload your dataset
- Run panel regression instantly
- Get results + interpretation

---

## Key Features

The system is designed and equipped with:
-	Five different model estimators for handling panel data. These are:
	- 📈Pooled OLS
	- 🏢Fixed Effects
	- 🔄Fixed Effects (Two-Way)
	- ⚙️Random Effects (GLS)
	- 📉First Difference

The system analyse panel dataset and produce outputs that covers:
- 📋 Coefficient Summary Metrics (standard errors, t-statistics, p-values with significance stars (`***`, `**`, `*`))
- 📐 Model Fit Metrics (R², Adjusted R², AIC, BIC, F-statistic)
- 🔬 Model Diagnostic (Hausman Test, Jarque-Bera Test, Durbin-Watson Statistic, Breusch-Pagan Test)
- 📊 Visual Results (Entity-level comparison bar charts, Correlation heatmaps, Residual Distribution Plots for understanding error distribution and detect deviations from normality.
	-	🔁Q-Q Plots that visually assess whether residuals follow a theoretical normal distribution.
	-	✅️Fitted vs Actual Scatter plots that evaluate model performance by comparing predicted vs actual values.


-	📥Downloadable Report (.docx)
Report contain Model Fit Result, Coeffint summary Table, Diagnostic Result, as well as AI'gnerated explanation of thd result

---
## Workflow
To use PanelStatX:

- 📵No software installation is needed
- 🚫 No command line is needed
- 🚫 No code is required.
  
✅️It is very easy and direct to use by anyone under 3 minutes based on key 6 steps**

1. 🔑Get an access key that comes with loaded credits
2. Visit the app and enter your key on the landing screen. 
3. 🔼Upload your panel dataset (CSV or excel file) in the side bar
4. ⚙️Configure your model and run analysis in the sidebar
    - ▶️select columns variables (i.e dependent and independent variables)
    - ▶️Choose any model from the 5 estimators
    - ▶️Click 'Run Analysis' and results will appear instantly across five tabs
5. 🔍View Results and Explore — check diagnostics, visualise entity trends, ask the AI explainer questions
7. 📄Download full results of the analysis + AI explained outputs as docx

👉 **[Try the Live System Here](https://panelstatx.streamlit.app/)**

---


