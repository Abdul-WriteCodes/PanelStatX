# ⬡ PanelStatX

<p align="center">
  <img src="Assets/PSX1.png" alt="PanelStatX Logo" width="800"/>
</p>


PanelStatX is a web-based AI-powered panel regression analysis system. It is built as a no-code statistical analysis system for economists, researchers, students, analysts, and data professionals who need to carry out rigorous panel regression.

PanelStatX stands out for its:
-	Simplicity: No complex installation or set up is required
-	Accessibility: It can be accessed and used via Android/iOS mobile phones, laptop and desktop devices
-	User Friendliness: It is purely a no-code system with a very low steep learning curve. It eliminates friction of writing compex Python scripts, R packages, or mastering use of heavyweight statistical software for panel regression
-	Hybrid Performance: It combines institutional-grade econometric methods with an AI-powered explainer.
-	Intelligence: It uses Large Language Model (GPT-4o) as a intelligent layer to explain results for users with no statistical background

---

## Key Features
Analysing panel data correctly requires specialised estimators that account for hidden differences between entities and time trends.
 
PanelStatX automatically handles these complexities, enabling users to focus on interpretation rather than implementation. 

The system is designed and equipped with:
-	Core Regression Models
	- **📈Pooled OLS**: Provides a baseline regression model that treats all observations as homogeneous, ignoring both entity-specific and time-specific effects. Useful for initial benchmarking and comparison.
	
	- **🏢Fixed Effects**: Controls for unobserved, time-invariant heterogeneity across entities (e.g., firms, countries) using within-transformation (demeaning). Ideal when entity-specific or time-specific characteristics may bias results
	
	- **🔄Fixed Effects (Two-Way)**: Simultaneously controls for both entity-specific and time-specific unobserved effects. This is particularly useful in real-world datasets where both dimensions influence outcomes.
	
	- **⚙️Random Effects (GLS)**: Assumes entity-specific effects are random and uncorrelated with regressors. Uses the Swamy-Arora variance components estimator and quasi-demeaning transformation for efficient estimation
	
	- **📉First Difference**: Eliminates entity-specific fixed effects by differencing consecutive time periods. Useful for robustness checks and when strict exogeneity assumptions may be violated

-	Statistical Diagnostics
	- **📋 Coefficient Summary Table**: system compute and report standard errors, t-statistics, p-values, and significance stars (`***`, `**`, `*`) for easy interpretation.
	- **📐Model Fit Metrics**: system compute and report R², Adjusted R², AIC, BIC, and F-statistic for evaluating model performance
	- **🧪 Model Diagnostic** 
		- **⚖️Hausman Test**: system compute and report Hausman test metrics to help users determine whether **Fixed Effects** or **Random Effects** is more appropriate for your data.
		- **🔔Jarque-Bera Test**: Checks whether residuals follow a normal distribution
		- **🔁Durbin-Watson Statistic**: Detects autocorrelation in residuals (serial correlation across time).
		- **📉Breusch-Pagan Test**: Tests for heteroskedasticity (non-constant variance in errors).
	
	
-	AI Explainer using the powerful GPT-4o model from OpenAI
	- One-click narrative interpretation of your full regression output
	- Covers model choice rationale, coefficient economic meaning, statistical significance, model fit quality, and caveats (endogeneity, heteroskedasticity, etc.)
	- Ask custom follow-up questions directly — e.g. *"Is variable x1 economically significant?"*

-	Visualisations
	- Interactive Plotly charts throughout — time-series lines by entity, entity mean bar charts, residual diagnostics, correlation heatmaps, distribution plots
	- All charts are dark-themed and render inline — no export needed to share insights at a glance
	 Residual distribution plots, Q-Q plots, fitted vs actual scatter, and leverage analysis

-	Downloadable Report **Word (.docx) report** containing:
	- Model summary and fit statistics table
	- Full coefficient estimates table (with significance highlighting)
	- Residual diagnostics table with auto-generated interpretations
	- AI write-up section 

---

## Why Choose PanelStatX?
PanelStatX is designed to be the fastest path from raw panel data to a presentation-ready, defensible analysis — whether you're a PhD researcher, a policy analyst, or an analyst building models for a client. Here is how PanelStatX compares with other tools/system

| | PanelStatX | Stata / EViews | R (`plm`) | Excel |
|---|---|---|---|---|
| Runs in the browser | ✅ | ❌ | ❌ | ✅ |
| No installation | ✅ | ❌ | ❌ | ✅ |
| Fixed + Random Effects | ✅ | ✅ | ✅ | ❌ |
| Hausman Test | ✅ | ✅ | ✅ | ❌ |
| Breusch-Pagan Test | ✅ | ✅ | ✅ | ❌ |
| AI plain-language explanation | ✅ | ❌ | ❌ | ❌ |
| Downloadable Word report | ✅ | ❌ | ❌ | ❌ |
| No code required | ✅ | ❌ | ❌ | ✅ |
| Pay-per-analysis (no subscription) | ✅ | ❌ | ✅ | ✅ |



---

## Getting Started (End Users)

**To use PanelStatX, no software installation is needed, No command line is needed. No code is required. Very easy and direct under 5 minutes based on key 7 processes**

1. **Get an access key** — purchase credits to receive your unique key
2. **Visit the app** and enter your key on the landing screen. Your remaining credit balance is shown in the sidebar at all times. You can top it up anytime
3. **Upload your panel dataset** in the side bar — CSV or Excel files with columns for your entity ID, time period, dependent variable, and independent variables
4. **Configure your model** in the sidebar — select columns, choose estimator, set options
5. **Run Analysis** — results appear instantly across five tabs
6. **Explore** — check diagnostics, visualise entity trends, ask the AI explainer questions
7. **Download** your Word report when ready

👉 **[Try the Live System Here](https://achievit.streamlit.app/)**

---

## Support, Credits & Access

PanelStatX operates on a **prepaid credit system**. 
-	Credits are tied to your e-mail and unique **access key (PSX-xxxx-xxxx-xxx)** , issued at purchase
-	**Credits never expire**. Users can use them at their own pace, on their own schedule, from anywhere in the world
-	There are no monthly fees/subscription, and no usage windows to worry about
-	Your unique access key works from any device and any browser. 
-	Each analysis run costs 1 credit. Explanation of Results using AI also cost 1 credit. When credit balance hit zero, none of this will work

For access key issues, credit top-ups, or technical questions, contact the PanelStatX team directly. Include your access key (first 4 characters only) and a description of the issue.

---

*⬡ PanelStatX · Panel Regression Analysis System · Powered by GPT-4*