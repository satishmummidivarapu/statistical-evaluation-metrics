import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import re

# 1. Page Configuration (Must be first)
st.set_page_config(
    page_title="Statistical Evaluation Metrics",
    page_icon="📈",
    layout="wide"
)

# 2. Custom CSS for UI/UX Improvements (Colors, Shadows, Cards)
st.markdown("""
    <style>
    /* Main background */
    .stApp {
        background-color: #f4f7f6;
    }
    /* Info Cards */
    .metric-card {
        background-color: #ffffff;
        padding: 25px;
        border-radius: 12px;
        border-left: 6px solid #1f77b4;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 25px;
    }
    /* Result Display Card */
    .result-card {
        background-color: #e8f4f8;
        padding: 30px;
        border-radius: 12px;
        text-align: center;
        border: 2px solid #1f77b4;
        box-shadow: 0 4px 10px rgba(31, 119, 180, 0.2);
        margin: 20px 0px;
    }
    .result-value {
        font-size: 48px;
        font-weight: bold;
        color: #1f77b4;
    }
    .result-title {
        font-size: 20px;
        color: #333333;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Header & Banner Image
# Using a professional data analytics placeholder image
st.image("https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=2000&q=80", use_container_width=True)
st.title("📊 Statistical Evaluation Metrics Suite")
st.markdown("Evaluate your environmental, hydrological, and research models with precision.")
st.markdown("---")

# 4. Metric Dictionary
metrics_info = {
    "Root Mean Square Error (RMSE)": {
        "key": "RMSE",
        "definition": "Measures the square root of the average variance of residuals. It penalizes larger errors heavily.",
        "formula": r"$$\text{RMSE}=\sqrt{\frac{1}{n}\sum_{i=1}^{n}(X_{obs,i}-X_{sim,i})^2}$$",
        "range": "• **Optimal Value:** 0.0\n• **Interpretation:** Lower values indicate better model performance."
    },
    "Mean Absolute Error (MAE)": {
        "key": "MAE",
        "definition": "Calculates the average of the absolute differences between observations and simulations. Does not overly penalize outliers.",
        "formula": r"$$\text{MAE}=\frac{1}{n}\sum_{i=1}^{n}\lvert X_{obs,i}-X_{sim,i}\rvert$$",
        "range": "• **Optimal Value:** 0.0\n• **Interpretation:** Lower values signify higher accuracy."
    },
    "Mean Bias Error (MBE)": {
        "key": "MBE",
        "definition": "Measures the systematic tendency of a model to over- or underestimate the observed parameters.",
        "formula": r"$$\text{MBE}=\frac{1}{n}\sum_{i=1}^{n}(X_{sim,i}-X_{obs,i})$$",
        "range": "• **Optimal Value:** 0.0\n• **Interpretation:** Negative values indicate underestimation, positive indicate overestimation."
    },
    "Nash-Sutcliffe Efficiency (NSE)": {
        "key": "NSE",
        "definition": "Evaluates how well a model predicts relative to the mean of observations.",
        "formula": r"$$\text{NSE}=1-\frac{\sum_{i=1}^{n}(X_{obs,i}-X_{sim,i})^2}{\sum_{i=1}^{n}(X_{obs,i}-\bar{X}_{obs})^2}$$",
        "range": "• **Optimal Value:** 1.0\n• **Ranges:** >0.75 (Very Good), 0.65-0.75 (Good), 0.50-0.65 (Satisfactory)"
    },
    "Coefficient of Determination (R²)": {
        "key": "R²",
        "definition": "Quantifies the proportion of the variance in the observed data that can be predicted from the simulated model.",
        "formula": r"$$R^2=\left[\frac{\sum(X_{obs,i}-\bar{X}_{obs})(X_{sim,i}-\bar{X}_{sim})}{\sqrt{\sum(X_{obs,i}-\bar{X}_{obs})^2}\sqrt{\sum(X_{sim,i}-\bar{X}_{sim})^2}}\right]^2$$",
        "range": "• **Optimal Value:** 1.0\n• **Interpretation:** Values > 0.60 are generally accepted as satisfactory."
    }
}

# 5. Metric Selection
selected_metric_name = st.selectbox(
    "🎯 Select the Evaluation Metric you want to calculate:",
    options=list(metrics_info.keys())
)
metric_key = metrics_info[selected_metric_name]["key"]

# 6. Dynamic Information Card
st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
st.subheader(f"About {metric_key}")
st.write(metrics_info[selected_metric_name]["definition"])
st.markdown(metrics_info[selected_metric_name]["formula"])
st.markdown(metrics_info[selected_metric_name]["range"])
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")

# 7. Smart Input Parsing Function for Excel Data
def parse_pasted_data(raw_text):
    """Splits text by newlines, tabs, or commas and converts to floats"""
    if not raw_text.strip():
        return []
    # Replace tabs and commas with spaces, then split by whitespace/newlines
    cleaned_items = re.split(r'[\n\r\t, ]+', raw_text.strip())
    # Filter out empty strings and convert to float
    parsed = []
    for item in cleaned_items:
        try:
            parsed.append(float(item))
        except ValueError:
            pass # Ignore non-numeric text like headers if pasted accidentally
    return parsed

# 8. Data Input Setup
st.subheader("📥 Data Input Setup")
approach = st.radio(
    "Choose your data provision method:",
    options=["Approach 1: Copy-Paste directly from Excel", "Approach 2: File Upload (CSV or Excel)"]
)

obs_data, sim_data = [], []
data_ready = False

if approach == "Approach 1: Copy-Paste directly from Excel":
    st.info("💡 **Tip:** Go to your Excel file, highlight the entire column of numbers, copy (Ctrl+C), and paste (Ctrl+V) directly into the boxes below. One number per line.")
    col1, col2 = st.columns(2)
    with col1:
        obs_input = st.text_area("📋 Paste Observed Data:", height=250, placeholder="e.g.\n12.5\n14.1\n15.8")
    with col2:
        sim_input = st.text_area("📋 Paste Simulated Data:", height=250, placeholder="e.g.\n11.8\n14.5\n15.2")
    
    obs_data = parse_pasted_data(obs_input)
    sim_data = parse_pasted_data(sim_input)
    
    if len(obs_data) > 0 and len(sim_data) > 0:
        if len(obs_data) == len(sim_data):
            st.success(f"✅ Successfully read {len(obs_data)} data points!")
            data_ready = True
        else:
            st.error(f"⚠️ Dataset mismatch! Observed has {len(obs_data)} values, but Simulated has {len(sim_data)} values.")

else:
    uploaded_file = st.file_uploader("Upload your evaluation dataset (.csv or .xlsx):", type=["csv", "xlsx"])
    st.markdown("*(Ensure your file has two columns specifically named **Observed** and **Simulated**)*")
    
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            
            if "Observed" in df.columns and "Simulated" in df.columns:
                df_clean = df[["Observed", "Simulated"]].dropna()
                obs_data = df_clean["Observed"].tolist()
                sim_data = df_clean["Simulated"].tolist()
                if len(obs_data) > 0:
                    st.success(f"✅ Successfully loaded {len(obs_data)} data points from file!")
                    data_ready = True
                else:
                    st.error("The uploaded document contains no valid rows of numbers.")
            else:
                st.error("⚠️ Required column headers missing. Ensure headers are exactly 'Observed' and 'Simulated'.")
        except Exception as e:
            st.error(f"Error reading file: {e}")

# 9. Math Execution (Calculates only the selected metric)
def calculate_single_metric(obs, sim, metric):
    o = np.array(obs)
    s = np.array(sim)
    n = len(o)
    
    if metric == "RMSE":
        return np.sqrt(np.mean((o - s)**2))
    elif metric == "MAE":
        return np.mean(np.abs(o - s))
    elif metric == "MBE":
        return np.mean(s - o)
    elif metric == "NSE":
        mean_obs = np.mean(o)
        return 1 - (np.sum((o - s)**2) / np.sum((o - mean_obs)**2))
    elif metric == "R²":
        correlation_matrix = np.corrcoef(o, s)
        return correlation_matrix[0,1]**2 if correlation_matrix.shape == (2,2) else 0.0

# 10. Evaluation Trigger & Visualizations
if data_ready:
    if st.button("🚀 Calculate & Generate Plots", type="primary", use_container_width=True):
        
        # Calculate only the requested metric
        result_value = calculate_single_metric(obs_data, sim_data, metric_key)
        
        # Display the single output in a beautiful custom card
        st.markdown(f"""
            <div class='result-card'>
                <div class='result-title'>Final Calculated {metric_key}</div>
                <div class='result-value'>{result_value:.4f}</div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.subheader("📈 Model Comparison Visualizations")
        
        indices = list(range(1, len(obs_data) + 1))
        
        # Plot 1: Time Series Trend
        fig_line = go.Figure()
        fig_line.add_trace(go.Scatter(x=indices, y=obs_data, mode='lines+markers', name='Observed', line=dict(color='#1f77b4', width=2)))
        fig_line.add_trace(go.Scatter(x=indices, y=sim_data, mode='lines+markers', name='Simulated', line=dict(color='#ff7f0e', dash='dash', width=2)))
        fig_line.update_layout(
            title="Observed vs. Simulated Trend Analysis",
            xaxis_title="Data Index Points",
            yaxis_title="Values",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=True, gridcolor='#e0e0e0'),
            yaxis=dict(showgrid=True, gridcolor='#e0e0e0'),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_line, use_container_width=True)
        
        # Plot 2: 1:1 Scatter Plot
        fig_scatter = go.Figure()
        fig_scatter.add_trace(go.Scatter(x=obs_data, y=sim_data, mode='markers', name='Data Points', marker=dict(color='#2ca02c', size=10, opacity=0.7)))
        
        # Identity Line
        min_val = min(min(obs_data), min(sim_data))
        max_val = max(max(obs_data), max(sim_data))
        fig_scatter.add_trace(go.Scatter(x=[min_val, max_val], y=[min_val, max_val], mode='lines', name='1:1 Perfect Fit', line=dict(color='gray', dash='dot')))
        
        fig_scatter.update_layout(
            title=f"Scatter Analysis (Evaluated by {metric_key})",
            xaxis_title="Observed Data",
            yaxis_title="Simulated Data",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=True, gridcolor='#e0e0e0'),
            yaxis=dict(showgrid=True, gridcolor='#e0e0e0'),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
else:
    st.info("Waiting for data input. Please provide data and click the button to generate your metrics and charts.")
