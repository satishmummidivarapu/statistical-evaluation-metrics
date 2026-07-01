import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# Page Configuration
st.set_page_config(
    page_title="Statistical Evaluation Metrics",
    page_icon="📊",
    layout="wide"
)

# Custom Background Styling
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .metric-box {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# Main Heading
st.title("Statistical Evaluation Metrics")
st.markdown("---")

# 1. Metric Dictionary with Info, Formulas, and Permissible Ranges
metrics_info = {
    "Root Mean Square Error (RMSE)": {
        "definition": "Measures the square root of the average variance of residuals. It penalizes larger errors heavily, making it an excellent indicator of overall model precision.",
        "formula": r"$$\text{RMSE}=\sqrt{\frac{1}{n}\sum_{i=1}^{n}(X_{obs,i}-X_{sim,i})^2}$$",
        "range": "• **Optimal Value:** 0.0\n• **Interpretation:** Lower values indicate better model performance. In environmental and hydrological modeling, an RMSE-to-observation standard deviation ratio (RSR) $\le0.70$ is generally considered satisfactory for basin-scale validation."
    },
    "Mean Absolute Error (MAE)": {
        "definition": "Calculates the average of the absolute differences between observations and simulations. Unlike RMSE, it weights all individual errors equally without penalizing outliers.",
        "formula": r"$$\text{MAE}=\frac{1}{n}\sum_{i=1}^{n}\lvert X_{obs,i}-X_{sim,i}\rvert$$",
        "range": "• **Optimal Value:** 0.0\n• **Interpretation:** Lower values signify higher accuracy. Preferred when error distributions are normally distributed and extreme variance penalty is not required."
    },
    "Mean Bias Error (MBE)": {
        "definition": "Measures the systematic tendency of a model to over- or underestimate the observed parameters across the tracking timeline.",
        "formula": r"$$\text{MBE}=\frac{1}{n}\sum_{i=1}^{n}(X_{sim,i}-X_{obs,i})$$",
        "range": "• **Optimal Value:** 0.0\n• **Interpretation:** Negative values ($\text{MBE}<0$) indicate systematic underestimation, while positive values ($\text{MBE}>0$) indicate overestimation. A percentage bias (PBIAS) within $\pm25\%$ is typically acceptable for hydro-climatic simulations."
    },
    "Nash-Sutcliffe Efficiency (NSE)": {
        "definition": "A normalized statistic that determines the relative magnitude of the residual variance compared to the measured data variance. It evaluates how well a model predicts relative to the mean of observations.",
        "formula": r"$$\text{NSE}=1-\frac{\sum_{i=1}^{n}(X_{obs,i}-X_{sim,i})^2}{\sum_{i=1}^{n}(X_{obs,i}-\bar{X}_{obs})^2}$$",
        "range": "• **Optimal Value:** 1.0\n• **Permissible Ranges:**\n  - $\text{NSE}>0.75$: Very Good\n  - $0.65<\text{NSE}\le0.75$: Good\n  - $0.50\le\text{NSE}\le0.65$: Satisfactory\n  - $\text{NSE}<0.50$: Unsatisfactory"
    },
    "Coefficient of Determination (R²)": {
        "definition": "Quantifies the proportion of the variance in the observed data that can be predicted from the simulated model output, assessing linear correlation.",
        "formula": r"$$R^2=\left[\frac{\sum(X_{obs,i}-\bar{X}_{obs})(X_{sim,i}-\bar{X}_{sim})}{\sqrt{\sum(X_{obs,i}-\bar{X}_{obs})^2}\sqrt{\sum(X_{sim,i}-\bar{X}_{sim})^2}}\right]^2$$",
        "range": "• **Optimal Value:** 1.0\n• **Interpretation:** Ranges from 0 to 1. Values exceeding 0.60 are widely accepted as satisfactory in complex natural resource modeling frameworks, though it should ideally be paired with a metric identifying systematic bias."
    }
}

# 2. Metric Selection Interface (Names Only)
selected_metric_name = st.selectbox(
    "Select an Evaluation Metric to Explore:",
    options=list(metrics_info.keys())
)

# 3. Dynamic Information Card Display
st.markdown("<div class='metric-box'>", unsafe_allow_html=True)
st.subheader(f"About {selected_metric_name}")
st.write(metrics_info[selected_metric_name]["definition"])

st.markdown("### Mathematical Formulation")
st.markdown(metrics_info[selected_metric_name]["formula"])

st.markdown("### Research Permissible Ranges & Interpretation")
st.markdown(metrics_info[selected_metric_name]["range"])
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")

# 4. Input Approach Setup
st.subheader("Data Input Setup")
approach = st.radio(
    "Choose data provision approach:",
    options=["Approach 1: Direct Copy-Paste", "Approach 2: File Upload (CSV or Excel)"]
)

obs_data = []
sim_data = []
data_ready = False

if approach == "Approach 1: Direct Copy-Paste":
    col1, col2 = st.columns(2)
    with col1:
        obs_input = st.text_area("Observed Values (Comma-separated numbers):", value="12.5, 14.1, 15.8, 16.2, 18.0, 19.1, 21.4")
    with col2:
        sim_input = st.text_area("Simulated Values (Comma-separated numbers):", value="11.8, 14.5, 15.2, 16.9, 17.5, 19.8, 20.9")
    
    try:
        obs_data = [float(x.strip()) for x in obs_input.split(",") if x.strip() != ""]
        sim_data = [float(x.strip()) for x in sim_input.split(",") if x.strip() != ""]
        if len(obs_data) == len(sim_data) and len(obs_data) > 0:
            data_ready = True
        elif len(obs_data) != len(sim_data):
            st.error(f"Dataset length mismatch. Observed elements: {len(obs_data)} | Simulated elements: {len(sim_data)}")
    except ValueError:
        st.error("Please verify that all inputs are valid numeric values separated by commas.")

else:
    uploaded_file = st.file_uploader("Upload your evaluation dataset:", type=["csv", "xlsx"])
    
    st.markdown("#### Predefined Target Layout Format")
    st.markdown("Your file must contain exactly two main numeric columns labeled precisely as shown below:")
    
    template_df = pd.DataFrame({
        "Observed": [12.50, 14.10, 15.80],
        "Simulated": [11.80, 14.50, 15.20]
    })
    st.table(template_df)
    
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
                    data_ready = True
                else:
                    st.error("The uploaded document contains no valid rows of numbers.")
            else:
                st.error("Required column mappings missing. Ensure headers are titled precisely 'Observed' and 'Simulated'.")
        except Exception as e:
            st.error(f"Error executing file parsing structure: {e}")

# 5. Math Execution Functions
def calculate_metrics(obs, sim):
    o = np.array(obs)
    s = np.array(sim)
    n = len(o)
    
    rmse = np.sqrt(np.mean((o - s)**2))
    mae = np.mean(np.abs(o - s))
    mbe = np.mean(s - o)
    
    mean_obs = np.mean(o)
    nse = 1 - (np.sum((o - s)**2) / np.sum((o - mean_obs)**2))
    
    correlation_matrix = np.corrcoef(o, s)
    if correlation_matrix.shape == (2,2):
        r_sq = correlation_matrix[0,1]**2
    else:
        r_sq = 0.0
        
    return {"RMSE": rmse, "MAE": mae, "MBE": mbe, "NSE": nse, "R²": r_sq}

# 6. Evaluation Trigger & Visualizations Panel
if data_ready:
    if st.button("Calculate & Generate Plots", type="primary"):
        results = calculate_metrics(obs_data, sim_data)
        
        st.markdown("---")
        st.subheader("Estimation Outputs")
        
        # Display selected metric prominently, and show others alongside for context
        m_keys = {"Root Mean Square Error (RMSE)": "RMSE", "Mean Absolute Error (MAE)": "MAE", 
                  "Mean Bias Error (MBE)": "MBE", "Nash-Sutcliffe Efficiency (NSE)": "NSE", 
                  "Coefficient of Determination (R²)": "R²"}
        
        primary_key = m_keys[selected_metric_name]
        
        st.metric(label=f"Target Valuation: {selected_metric_name}", value=f"{results[primary_key]:.4f}")
        
        # Comprehensive output tracking grid
        c1, c2, c3, c4, c5 = st.columns(5)
        c1.metric("RMSE", f"{results['RMSE']:.3f}")
        c2.metric("MAE", f"{results['MAE']:.3f}")
        c3.metric("MBE", f"{results['MBE']:.3f}")
        c4.metric("NSE", f"{results['NSE']:.3f}")
        c5.metric("R²", f"{results['R²']:.3f}")
        
        st.markdown("---")
        st.subheader("Model Comparison Visualizations")
        
        indices = list(range(1, len(obs_data) + 1))
        
        # Plot 1: Time Series / Trend Comparison Line Chart
        fig_line = go.Figure()
        fig_line.add_trace(go.Scatter(x=indices, y=obs_data, mode='lines+markers', name='Observed', line=dict(width=2)))
        fig_line.add_trace(go.Scatter(x=indices, y=sim_data, mode='lines+markers', name='Simulated', line=dict(dash='dash', width=2)))
        fig_line.update_layout(
            title="Observed vs. Simulated Values Comparison",
            xaxis_title="Data Index Points",
            yaxis_title="Value Scope",
            template="plotly_white",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_line, use_container_width=True)
        
        # Plot 2: 1:1 Scatter Plot
        fig_scatter = go.Figure()
        fig_scatter.add_trace(go.Scatter(x=obs_data, y=sim_data, mode='markers', name='Data Elements', marker=dict(size=10)))
        
        # Identity Line coordinates tracking
        min_val = min(min(obs_data), min(sim_data))
        max_val = max(max(obs_data), max(sim_data))
        fig_scatter.add_trace(go.Scatter(x=[min_val, max_val], y=[min_val, max_val], mode='lines', name='1:1 Fit Line', line=dict(color='gray', dash='dot')))
        
        fig_scatter.update_layout(
            title="Scatter Analysis with 1:1 Perfect Fit Reference",
            xaxis_title="Observed Baseline",
            yaxis_title="Simulated Estimate",
            template="plotly_white",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
else:
    st.info("Awaiting structural balance verification. Supply uniform tracking coordinates to execute processing configurations.")