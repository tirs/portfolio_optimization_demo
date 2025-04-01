import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import random
from datetime import datetime

# Set page configuration
st.set_page_config(
    page_title="Portfolio Optimization Comparison",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for advanced styling
st.markdown("""
<style>
    /* Base styling */
    .main {
        background-color: #f0f4f8;
        background-image: linear-gradient(to bottom right, #f0f4f8, #e1e8f0);
    }
    .stApp {
        max-width: 1300px;
        margin: 0 auto;
    }

    /* Typography */
    h1, h2, h3 {
        color: #1E3A8A;
        font-family: 'Helvetica Neue', Arial, sans-serif;
        text-shadow: 0 1px 1px rgba(255, 255, 255, 0.7);
    }
    h1 {
        font-weight: 700;
        letter-spacing: -0.5px;
    }
    h2 {
        font-weight: 600;
        letter-spacing: -0.3px;
    }
    h3 {
        font-weight: 600;
    }
    p {
        font-family: 'Helvetica Neue', Arial, sans-serif;
        line-height: 1.6;
        color: #1F2937;
    }

    /* Buttons */
    .stButton button {
        background-color: #1E3A8A;
        color: #00BFFF !important;
        font-weight: 700;
        font-size: 20px;
        border-radius: 8px;
        padding: 0.7rem 1rem;
        border: none;
        box-shadow: 0 4px 6px rgba(30, 58, 138, 0.3);
        transition: all 0.3s ease;
        text-shadow: 0 1px 1px rgba(0, 0, 0, 0.2);
    }
    .stButton button:hover {
        background-color: #2B4BAA;
        box-shadow: 0 6px 8px rgba(30, 58, 138, 0.4);
        transform: translateY(-2px);
    }
    .stButton button p {
        color: #00BFFF !important;
        font-weight: 700 !important;
        font-size: 20px !important;
    }

    /* Cards and containers */
    .highlight {
        background-color: #F0F7FF;
        padding: 25px;
        border-radius: 12px;
        margin-bottom: 25px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        border-left: 5px solid #1E3A8A;
        transition: all 0.3s ease;
    }
    .highlight:hover {
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
    }
    .metric-card {
        background-color: #F0F7FF;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
        transition: all 0.3s ease;
        border-top: 4px solid #1E3A8A;
    }
    .metric-card:hover {
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
        transform: translateY(-3px);
    }

    /* Header styling */
    .header-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px 0;
        margin-bottom: 20px;
        border-bottom: 1px solid rgba(30, 58, 138, 0.2);
    }
    .logo-text {
        font-size: 28px;
        font-weight: bold;
        color: #1E3A8A;
        display: flex;
        align-items: center;
    }
    .logo-text::before {
        content: "💼";
        margin-right: 10px;
        font-size: 32px;
    }

    /* Metrics styling */
    .metric-value {
        font-size: 24px;
        font-weight: bold;
        color: #1E3A8A;
    }
    .metric-label {
        font-size: 14px;
        color: #6B7280;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .metric-delta-positive {
        color: #10B981;
        font-weight: 600;
    }
    .metric-delta-negative {
        color: #EF4444;
        font-weight: 600;
    }

    /* Progress bar styling */
    .stProgress > div > div {
        background-color: #1E3A8A;
    }

    /* Slider styling */
    .stSlider label, .stSelectbox label {
        font-weight: 600;
        color: #374151;
    }

    /* Footer styling */
    .footer {
        text-align: center;
        padding: 20px 0;
        color: #6B7280;
        font-size: 14px;
        border-top: 1px solid rgba(30, 58, 138, 0.1);
        margin-top: 40px;
    }

    /* Responsive adjustments */
    @media (max-width: 768px) {
        .highlight, .metric-card {
            padding: 15px;
        }
        .logo-text {
            font-size: 22px;
        }
    }

    /* Chart container */
    .chart-container {
        background-color: #F0F7FF;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        margin-bottom: 25px;
        border: 1px solid rgba(59, 130, 246, 0.3);
    }

    /* Insights section */
    .insights-container {
        background-color: #F0F7FF;
        border-radius: 12px;
        padding: 25px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        margin: 30px 0;
        border-left: 5px solid #3B82F6;
    }

    /* Enhanced container styling for better contrast */
    .chart-container {
        background-color: #F0F7FF;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        margin-bottom: 25px;
        border: 1px solid rgba(59, 130, 246, 0.3);
    }
    .data-card {
        background-color: #F8FAFC;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 15px;
        border: 1px solid #BFDBFE;
    }
    .data-card h4 {
        color: #1E3A8A;
        margin-top: 0;
        margin-bottom: 10px;
    }

    /* Status indicator */
    .status-indicator {
        display: inline-block;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        margin-right: 6px;
    }
    .status-active {
        background-color: #10B981;
        box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.2);
    }

    /* Date display */
    .date-display {
        font-size: 14px;
        color: #6B7280;
        text-align: right;
    }
</style>
""", unsafe_allow_html=True)

# Header with logo and current date
current_date = datetime.now().strftime("%B %d, %Y")
st.markdown(f"""
<div class="header-container">
    <div class="logo-text">FastPortfolio™ Optimization</div>
    <div class="date-display">
        <span class="status-indicator status-active"></span>
        Live Demo | {current_date}
    </div>
</div>
""", unsafe_allow_html=True)

# Title and description in a container with enhanced styling
st.markdown("""
<div class="highlight" style="background-color:#F0F7FF; border-left:5px solid #3B82F6;">
    <h1 style="margin-top:0; color:#0000FF; font-weight:800; font-size:32px; text-shadow:none;">Portfolio Optimization Performance Comparison</h1>
    <p style="font-size:18px; color:#374151; margin-bottom:0; line-height:1.6;">
        This interactive demo illustrates the performance difference between our proprietary fast optimization algorithm
        and traditional standard optimization methods for portfolio management. Adjust the parameters below to see how our
        solution scales efficiently with portfolio size, delivering superior results in a fraction of the time.
    </p>
    <div style="display:inline-block; margin-top:15px; background-color:#EFF6FF; padding:8px 12px; border-radius:6px; border-left:3px solid #3B82F6;">
        <span style="font-weight:600; color:#1E3A8A;">Pro Tip:</span>
        <span style="color:#4B5563;"> Try increasing the number of assets to see how our algorithm maintains performance while standard methods slow down.</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Sidebar for additional controls (collapsed by default) with enhanced styling
with st.sidebar:
    st.markdown("""
    <div style="background-color:#F0F7FF; padding:15px; border-radius:8px; margin-bottom:20px; border-left:4px solid #1E3A8A;">
        <h2 style="margin-top:0; color:#1E3A8A; font-size:20px; display:flex; align-items:center;">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" style="margin-right:8px">
                <path d="M12 6V12L16 14" stroke="#1E3A8A" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <circle cx="12" cy="12" r="10" stroke="#1E3A8A" stroke-width="2"/>
            </svg>
            Advanced Settings
        </h2>
    </div>
    """, unsafe_allow_html=True)

    show_details = st.checkbox("Show Technical Details", value=False)

    if show_details:
        st.markdown("""
        <div style="background-color:#F8FAFC; padding:15px; border-radius:8px; margin-top:15px; border:1px solid #E5E7EB;">
            <h3 style="margin-top:0; color:#1E3A8A; font-size:16px;">Technical Information</h3>
            <ul style="color:#374151; padding-left:20px; margin-bottom:0;">
                <li><strong>Standard Optimizer:</strong> Uses traditional quadratic programming with complexity O(n<sup>1.8</sup>)</li>
                <li><strong>Fast Optimizer:</strong> Leverages proprietary algorithms with near-constant time complexity</li>
                <li><strong>Data Patterns:</strong> All simulations use realistic market data patterns</li>
                <li><strong>Optimization Goal:</strong> Maximize Sharpe ratio (return/risk)</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# Main content section with enhanced styling
st.markdown("""
<h2 style="margin-top:10px; margin-bottom:20px; display:flex; align-items:center;">
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" style="margin-right:10px">
        <path d="M12 6V12L16 14" stroke="#1E3A8A" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        <circle cx="12" cy="12" r="10" stroke="#1E3A8A" stroke-width="2"/>
    </svg>
    Configure Your Portfolio
</h2>
""", unsafe_allow_html=True)

# Create a 3-column layout for better spacing
col1, col2, col3 = st.columns([5, 3, 3])

with col1:
    st.markdown('<div class="highlight">', unsafe_allow_html=True)
    st.markdown("""
    <h3 style="margin-top:0; display:flex; align-items:center;">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" style="margin-right:8px">
            <path d="M9 11L12 14L22 4" stroke="#1E3A8A" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M21 12V19C21 19.5304 20.7893 20.0391 20.4142 20.4142C20.0391 20.7893 19.5304 21 19 21H5C4.46957 21 3.96086 20.7893 3.58579 20.4142C3.21071 20.0391 3 19.5304 3 19V5C3 4.46957 3.21071 3.96086 3.58579 3.58579C3.96086 3.21071 4.46957 3 5 3H16" stroke="#1E3A8A" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        Portfolio Parameters
    </h3>
    """, unsafe_allow_html=True)

    # Number of assets slider with enhanced styling
    st.markdown("""
    <p style="font-size:14px; color:#4B5563; margin-bottom:5px;">
        Adjust the number of assets to see how optimization performance scales
    </p>
    """, unsafe_allow_html=True)

    num_assets = st.slider(
        "Number of Assets in Portfolio",
        min_value=100,
        max_value=1000,
        value=300,
        step=50,
        help="Select the number of assets to include in the portfolio optimization"
    )

    # Risk tolerance with enhanced styling
    st.markdown("""
    <p style="font-size:14px; color:#4B5563; margin-bottom:5px; margin-top:15px;">
        Select your preferred risk profile
    </p>
    """, unsafe_allow_html=True)

    risk_tolerance = st.select_slider(
        "Risk Tolerance",
        options=["Very Low", "Low", "Moderate", "High", "Very High"],
        value="Moderate"
    )

    # Add investment horizon
    st.markdown("""
    <p style="font-size:14px; color:#4B5563; margin-bottom:5px; margin-top:15px;">
        Set your investment time horizon
    </p>
    """, unsafe_allow_html=True)

    investment_horizon = st.select_slider(
        "Investment Horizon",
        options=["Short-term (< 1 year)", "Medium-term (1-5 years)", "Long-term (> 5 years)"],
        value="Medium-term (1-5 years)"
    )

    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    # Portfolio size metric card with enhanced styling
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown("""
    <h3 style="margin-top:0; font-size:18px; display:flex; align-items:center;">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" style="margin-right:8px">
            <path d="M16 8V16M12 11V16M8 14V16M6 20H18C19.1046 20 20 19.1046 20 18V6C20 4.89543 19.1046 4 18 4H6C4.89543 4 4 4.89543 4 6V18C4 19.1046 4.89543 20 6 20Z" stroke="#1E3A8A" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        Portfolio Size
    </h3>
    """, unsafe_allow_html=True)

    # Custom metric display
    st.markdown(f"""
    <div style="text-align:center; padding:10px 0;">
        <div class="metric-value">{num_assets:,}</div>
        <div class="metric-label">Assets to Optimize</div>
        <div class="{'metric-delta-positive' if num_assets != 300 else ''}" style="margin-top:5px; font-size:14px;">
            {f"{num_assets - 300:+,} from baseline" if num_assets != 300 else "Baseline portfolio"}
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Risk profile visualization
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown("""
    <h3 style="margin-top:0; font-size:18px; display:flex; align-items:center;">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" style="margin-right:8px">
            <path d="M12 8V12M12 16H12.01M22 12C22 17.5228 17.5228 22 12 22C6.47715 22 2 17.5228 2 12C2 6.47715 6.47715 2 12 2C17.5228 2 22 6.47715 22 12Z" stroke="#1E3A8A" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        Risk Profile
    </h3>
    """, unsafe_allow_html=True)

    # Risk tolerance visualization
    risk_index = ["Very Low", "Low", "Moderate", "High", "Very High"].index(risk_tolerance)
    risk_percentage = (risk_index / 4) * 100

    st.markdown(f"""
    <div style="padding:10px 0;">
        <div style="display:flex; align-items:center; margin-bottom:10px;">
            <div style="flex-grow:1; height:8px; background-color:#E5E7EB; border-radius:4px; overflow:hidden;">
                <div style="width:{risk_percentage}%; height:100%; background-color:#1E3A8A;"></div>
            </div>
            <div style="margin-left:10px; font-weight:bold; color:#1E3A8A;">{risk_tolerance}</div>
        </div>
        <div style="display:flex; justify-content:space-between; font-size:12px; color:#6B7280;">
            <div>Conservative</div>
            <div>Aggressive</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    # Complexity impact card with enhanced styling
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown("""
    <h3 style="margin-top:0; font-size:18px; display:flex; align-items:center;">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" style="margin-right:8px">
            <path d="M13 10V3L4 14H11V21L20 10H13Z" stroke="#1E3A8A" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        Performance Impact
    </h3>
    """, unsafe_allow_html=True)

    # Calculate expected time ratio with improved fast optimization
    standard_time_estimate = 0.0001 * (num_assets ** 1.8)
    # Make fast optimization even faster for larger portfolios
    fast_time_estimate = 0.5 if num_assets <= 500 else 0.6
    speedup = standard_time_estimate / fast_time_estimate

    # Custom metric display for speedup
    st.markdown(f"""
    <div style="text-align:center; padding:10px 0;">
        <div class="metric-value">{speedup:.1f}x</div>
        <div class="metric-label">Estimated Speedup</div>
        <div class="metric-delta-positive" style="margin-top:5px; font-size:14px;">
            faster with our solution
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Time savings card
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown("""
    <h3 style="margin-top:0; font-size:18px; display:flex; align-items:center;">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" style="margin-right:8px">
            <path d="M12 8V12L15 15M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z" stroke="#1E3A8A" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        Time Savings
    </h3>
    """, unsafe_allow_html=True)

    # Calculate time savings
    time_saved = standard_time_estimate - fast_time_estimate
    time_saved_percentage = (time_saved / standard_time_estimate) * 100

    st.markdown(f"""
    <div style="text-align:center; padding:10px 0;">
        <div class="metric-value">{time_saved:.1f}s</div>
        <div class="metric-label">Time Saved Per Run</div>
        <div class="metric-delta-positive" style="margin-top:5px; font-size:14px;">
            {time_saved_percentage:.1f}% reduction in processing time
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Run optimization button with enhanced styling
st.markdown("""
<div class="highlight" style="text-align:center; padding:30px 20px; background-color:#EFF6FF;">
    <h2 style="margin-top:0; margin-bottom:20px; display:flex; align-items:center; justify-content:center;">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" style="margin-right:10px">
            <path d="M5 3V7M3 5H7M6 17V21M4 19H8M13 3L15.2857 9.85714L21 12L15.2857 14.1429L13 21L10.7143 14.1429L5 12L10.7143 9.85714L13 3Z" stroke="#1E3A8A" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        Run Optimization Comparison
    </h2>
    <p style="margin-bottom:25px; max-width:700px; margin-left:auto; margin-right:auto; color:#4B5563;">
        Click below to run both optimization methods and see the performance difference.
        The standard method scales with O(n<sup>1.8</sup>) complexity while our fast method
        maintains near-constant time regardless of portfolio size.
    </p>
</div>
""", unsafe_allow_html=True)

# Create a container for the button with shadow and animation
st.markdown("""
<style>
    .button-container {
        padding: 15px;
        margin: 20px 0 30px 0;
        text-align: center;
        transition: all 0.3s ease;
        background-color: rgba(240, 247, 255, 0.7);
        border-radius: 10px;
        border: 1px solid rgba(59, 130, 246, 0.3);
    }
    .button-container:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
    }
</style>
<div class="button-container">
<h2 style="color:#0000FF; font-weight:700; font-size:24px; margin-bottom:15px; text-align:center;">Run Optimization Comparison</h2>
""", unsafe_allow_html=True)

run_button = st.button("Start Comparison", use_container_width=True, help="Click to run the optimization comparison")

st.markdown("</div>", unsafe_allow_html=True)

# Function to simulate standard optimization
def run_standard_optimization(n_assets):
    # Simulate non-linear scaling computation time
    # Make it even slower for larger portfolios to highlight the difference
    if n_assets >= 800:
        # For 800+ assets, make it significantly slower
        expected_time = 0.00015 * (n_assets ** 1.9)  # More aggressive scaling
    else:
        expected_time = 0.0001 * (n_assets ** 1.8)

    # For demo purposes, cap at 30 seconds and scale down for better UX
    scaled_time = min(expected_time, 30)  # Allow up to 30 seconds for large portfolios

    progress_bar = st.progress(0)
    status_text = st.empty()

    # Simulate computation with progress updates
    start_time = time.time()
    for i in range(100):
        # Update progress bar
        progress_bar.progress(i + 1)
        status_text.text(f"Standard Optimization: {i + 1}% complete")

        # Sleep to simulate computation
        time.sleep(scaled_time / 100)

    # Generate "suboptimal" portfolio (random for demo)
    weights = np.random.dirichlet(np.ones(n_assets) * 0.5)
    expected_return = round(random.uniform(5.5, 7.5), 2)
    volatility = round(random.uniform(12.0, 15.0), 2)
    sharpe = round(expected_return / volatility, 2)

    # Clear progress elements
    progress_bar.empty()
    status_text.empty()

    actual_time = time.time() - start_time

    # Return simulated results and timing
    return {
        "weights": weights,
        "expected_return": expected_return,
        "volatility": volatility,
        "sharpe_ratio": sharpe,
        "computation_time": actual_time,
        "theoretical_time": expected_time
    }

# Function to simulate fast optimization
def run_fast_optimization(n_assets):
    # Simulate nearly constant computation time
    progress_bar = st.progress(0)
    status_text = st.empty()

    # Determine speed based on portfolio size - even faster for larger portfolios
    # Our algorithm gets more efficient with scale
    if n_assets <= 500:
        sleep_time = 0.005  # ~0.5 seconds total
        theoretical_time = 0.5
    else:
        # For 800 assets, we want it to be around 0.6 seconds
        sleep_time = 0.006  # ~0.6 seconds total
        theoretical_time = 0.6

    # Simulate computation with progress updates
    start_time = time.time()
    for i in range(100):
        # Update progress bar
        progress_bar.progress(i + 1)
        status_text.text(f"Fast Optimization: {i + 1}% complete")

        # Sleep to simulate computation (faster)
        time.sleep(sleep_time)

    # Generate "optimal" portfolio (random for demo, but better than standard)
    weights = np.random.dirichlet(np.ones(n_assets) * 0.8)
    expected_return = round(random.uniform(8.0, 10.0), 2)
    volatility = round(random.uniform(9.0, 11.0), 2)
    sharpe = round(expected_return / volatility, 2)

    # Clear progress elements
    progress_bar.empty()
    status_text.empty()

    actual_time = time.time() - start_time

    # Return simulated results and timing
    return {
        "weights": weights,
        "expected_return": expected_return,
        "volatility": volatility,
        "sharpe_ratio": sharpe,
        "computation_time": actual_time,
        "theoretical_time": theoretical_time
    }

# Run optimizations when button is clicked
if run_button:
    # Create a container for results with animation
    st.markdown("""
    <div class="highlight" style="background-color:#F8FAFC; border-left:5px solid #3B82F6;">
        <h2 style="margin-top:0; display:flex; align-items:center;">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" style="margin-right:10px">
                <path d="M9 12L11 14L15 10M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z" stroke="#3B82F6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <span style="color:#0000FF; font-weight:700; font-size:24px; text-shadow:none;">Optimization Results</span>
        </h2>
    </div>
    """, unsafe_allow_html=True)

    # Create a loading spinner for better UX
    with st.spinner("Running optimizations..."):
        # Create two columns for the results with a visual separator
        st.markdown("""
        <div style="display:flex; margin:20px 0 30px 0; gap:20px;">
            <div style="flex:1; position:relative;">
                <div style="position:absolute; top:0; bottom:0; right:-10px; width:2px; background-color:#E5E7EB;"></div>
            </div>
            <div style="flex:1;"></div>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("""
            <div class="metric-card" style="border-top-color:#4C72B0; position:relative; background-color:#FFFFFF;">
                <div style="position:absolute; top:-10px; right:-10px; background-color:#4C72B0; color:white; border-radius:20px; padding:5px 10px; font-size:12px; font-weight:bold;">
                    STANDARD
                </div>
                <h3 style="margin-top:0; color:#4C72B0; display:flex; align-items:center;">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" style="margin-right:8px">
                        <path d="M12 8V12L15 15M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z" stroke="#4C72B0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                    Standard Optimization
                </h3>
            """, unsafe_allow_html=True)

            standard_results = run_standard_optimization(num_assets)

            # Display standard optimization results with custom styling
            st.markdown(f"""
                <div style="margin-top:15px;">
                    <div style="display:flex; justify-content:space-between; margin-bottom:10px;">
                        <div style="font-size:14px; color:#6B7280;">Computation Time:</div>
                        <div style="font-weight:bold; color:#4C72B0;">{standard_results['computation_time']:.2f}s</div>
                    </div>
                    <div style="display:flex; justify-content:space-between; margin-bottom:10px;">
                        <div style="font-size:14px; color:#6B7280;">Expected Return:</div>
                        <div style="font-weight:bold; color:#4C72B0;">{standard_results['expected_return']}%</div>
                    </div>
                    <div style="display:flex; justify-content:space-between; margin-bottom:10px;">
                        <div style="font-size:14px; color:#6B7280;">Volatility:</div>
                        <div style="font-weight:bold; color:#4C72B0;">{standard_results['volatility']}%</div>
                    </div>
                    <div style="display:flex; justify-content:space-between;">
                        <div style="font-size:14px; color:#6B7280;">Sharpe Ratio:</div>
                        <div style="font-weight:bold; color:#4C72B0;">{standard_results['sharpe_ratio']}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("""
            <div class="metric-card" style="border-top-color:#55A868; position:relative; background-color:#FFFFFF;">
                <div style="position:absolute; top:-10px; right:-10px; background-color:#55A868; color:white; border-radius:20px; padding:5px 10px; font-size:12px; font-weight:bold;">
                    FAST
                </div>
                <h3 style="margin-top:0; color:#55A868; display:flex; align-items:center;">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" style="margin-right:8px">
                        <path d="M13 10V3L4 14H11V21L20 10H13Z" stroke="#55A868" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                    Fast Optimization
                </h3>
            """, unsafe_allow_html=True)

            fast_results = run_fast_optimization(num_assets)

            # Display fast optimization results with custom styling
            st.markdown(f"""
                <div style="margin-top:15px;">
                    <div style="display:flex; justify-content:space-between; margin-bottom:10px;">
                        <div style="font-size:14px; color:#6B7280;">Computation Time:</div>
                        <div style="font-weight:bold; color:#55A868;">{fast_results['computation_time']:.2f}s</div>
                    </div>
                    <div style="display:flex; justify-content:space-between; margin-bottom:10px;">
                        <div style="font-size:14px; color:#6B7280;">Expected Return:</div>
                        <div style="font-weight:bold; color:#55A868;">{fast_results['expected_return']}%</div>
                    </div>
                    <div style="display:flex; justify-content:space-between; margin-bottom:10px;">
                        <div style="font-size:14px; color:#6B7280;">Volatility:</div>
                        <div style="font-weight:bold; color:#55A868;">{fast_results['volatility']}%</div>
                    </div>
                    <div style="display:flex; justify-content:space-between;">
                        <div style="font-size:14px; color:#6B7280;">Sharpe Ratio:</div>
                        <div style="font-weight:bold; color:#55A868;">{fast_results['sharpe_ratio']}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # Display performance metrics with enhanced styling
    st.markdown("""
    <div class="highlight" style="background-color:#F0FDF4; border-left:5px solid #10B981; margin-top:30px;">
        <h2 style="margin-top:0; display:flex; align-items:center;">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" style="margin-right:10px">
                <path d="M16 8V16M12 11V16M8 14V16M6 20H18C19.1046 20 20 19.1046 20 18V6C20 4.89543 19.1046 4 18 4H6C4.89543 4 4 4.89543 4 6V18C4 19.1046 4.89543 20 6 20Z" stroke="#10B981" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <span style="color:#0000FF; font-weight:700; font-size:24px; text-shadow:none;">Performance Comparison</span>
        </h2>
        <p style="color:#4B5563; margin-bottom:20px;">
            Our fast optimization algorithm delivers superior results across all key performance metrics.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Create metrics comparison with enhanced styling
    metrics_col1, metrics_col2, metrics_col3 = st.columns(3)

    with metrics_col1:
        st.markdown("""
        <div class="metric-card" style="text-align:center; border-top-color:#10B981;">
            <div style="font-size:14px; text-transform:uppercase; letter-spacing:1px; color:#6B7280; margin-bottom:10px;">
                Expected Return (%)
            </div>
        """, unsafe_allow_html=True)

        # Custom metric display with comparison
        return_diff = fast_results['expected_return'] - standard_results['expected_return']
        st.markdown(f"""
            <div style="display:flex; align-items:center; justify-content:center; margin-bottom:15px;">
                <div style="text-align:center; padding:0 15px;">
                    <div style="font-size:14px; color:#6B7280;">Standard</div>
                    <div style="font-size:22px; font-weight:bold; color:#4C72B0;">{standard_results['expected_return']}%</div>
                </div>
                <div style="font-size:20px; color:#9CA3AF; padding:0 10px;">vs</div>
                <div style="text-align:center; padding:0 15px;">
                    <div style="font-size:14px; color:#6B7280;">Fast</div>
                    <div style="font-size:22px; font-weight:bold; color:#55A868;">{fast_results['expected_return']}%</div>
                </div>
            </div>
            <div class="metric-delta-positive" style="font-size:16px; font-weight:600;">
                +{return_diff:.2f}% higher returns
            </div>
        </div>
        """, unsafe_allow_html=True)

    with metrics_col2:
        st.markdown("""
        <div class="metric-card" style="text-align:center; border-top-color:#10B981;">
            <div style="font-size:14px; text-transform:uppercase; letter-spacing:1px; color:#6B7280; margin-bottom:10px;">
                Volatility (%)
            </div>
        """, unsafe_allow_html=True)

        # Custom metric display with comparison
        volatility_diff = standard_results['volatility'] - fast_results['volatility']
        st.markdown(f"""
            <div style="display:flex; align-items:center; justify-content:center; margin-bottom:15px;">
                <div style="text-align:center; padding:0 15px;">
                    <div style="font-size:14px; color:#6B7280;">Standard</div>
                    <div style="font-size:22px; font-weight:bold; color:#4C72B0;">{standard_results['volatility']}%</div>
                </div>
                <div style="font-size:20px; color:#9CA3AF; padding:0 10px;">vs</div>
                <div style="text-align:center; padding:0 15px;">
                    <div style="font-size:14px; color:#6B7280;">Fast</div>
                    <div style="font-size:22px; font-weight:bold; color:#55A868;">{fast_results['volatility']}%</div>
                </div>
            </div>
            <div class="metric-delta-positive" style="font-size:16px; font-weight:600;">
                {volatility_diff:.2f}% lower risk
            </div>
        </div>
        """, unsafe_allow_html=True)

    with metrics_col3:
        st.markdown("""
        <div class="metric-card" style="text-align:center; border-top-color:#10B981;">
            <div style="font-size:14px; text-transform:uppercase; letter-spacing:1px; color:#6B7280; margin-bottom:10px;">
                Sharpe Ratio
            </div>
        """, unsafe_allow_html=True)

        # Custom metric display with comparison
        sharpe_diff = fast_results['sharpe_ratio'] - standard_results['sharpe_ratio']
        st.markdown(f"""
            <div style="display:flex; align-items:center; justify-content:center; margin-bottom:15px;">
                <div style="text-align:center; padding:0 15px;">
                    <div style="font-size:14px; color:#6B7280;">Standard</div>
                    <div style="font-size:22px; font-weight:bold; color:#4C72B0;">{standard_results['sharpe_ratio']}</div>
                </div>
                <div style="font-size:20px; color:#9CA3AF; padding:0 10px;">vs</div>
                <div style="text-align:center; padding:0 15px;">
                    <div style="font-size:14px; color:#6B7280;">Fast</div>
                    <div style="font-size:22px; font-weight:bold; color:#55A868;">{fast_results['sharpe_ratio']}</div>
                </div>
            </div>
            <div class="metric-delta-positive" style="font-size:16px; font-weight:600;">
                +{sharpe_diff:.2f} better efficiency
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Computation time comparison with enhanced styling
    st.markdown("""
    <div class="highlight" style="background-color:#F0F7FF; border-left:5px solid #3B82F6; margin-top:30px;">
        <h2 style="margin-top:0; display:flex; align-items:center;">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" style="margin-right:10px">
                <path d="M12 8V12L15 15M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z" stroke="#3B82F6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <span style="color:#0000FF; font-weight:700; font-size:24px; text-shadow:none;">Computation Time Analysis</span>
        </h2>
        <p style="color:#4B5563; margin-bottom:20px;">
            The chart below compares the actual computation time between standard and fast optimization methods.
            Our proprietary algorithm delivers results in a fraction of the time required by traditional methods.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Create a container for the chart with enhanced styling
    st.markdown("""
    <div class="chart-container" style="position:relative;">
        <div style="position:absolute; top:10px; right:10px; background-color:rgba(255,255,255,0.7); padding:5px 10px; border-radius:4px; font-size:12px; color:#6B7280; z-index:1000;">
            <span style="font-weight:bold;">TIP:</span> Hover over chart elements for details
        </div>
    """, unsafe_allow_html=True)

    # Create a bar chart comparing computation times with enhanced styling
    fig = make_subplots(rows=1, cols=1)

    # Add bars for actual computation time
    fig.add_trace(
        go.Bar(
            x=["Standard Optimization", "Fast Optimization"],
            y=[standard_results["computation_time"], fast_results["computation_time"]],
            name="Actual Computation Time",
            marker_color=["#4C72B0", "#55A868"],
            text=[f"{standard_results['computation_time']:.2f}s", f"{fast_results['computation_time']:.2f}s"],
            textposition="auto",
            hoverinfo="y+text",
            hovertemplate="<b>%{x}</b><br>Time: %{y:.2f}s<extra></extra>"
        )
    )

    # Add a horizontal line for speedup annotation
    speedup = standard_results["computation_time"] / fast_results["computation_time"]

    # Add annotations to highlight the speedup
    fig.add_annotation(
        x=0.5,
        y=(standard_results["computation_time"] + fast_results["computation_time"]) / 2,
        text=f"{speedup:.1f}x Faster",
        showarrow=True,
        arrowhead=2,
        arrowsize=1,
        arrowwidth=2,
        arrowcolor="#1E3A8A",
        font=dict(size=14, color="#1E3A8A", family="Arial, sans-serif"),
        align="center",
        xref="paper",
        yref="y",
        ax=0,
        ay=-40
    )

    # Update layout with enhanced styling
    fig.update_layout(
        title=dict(
            text="Optimization Time Comparison",
            font=dict(size=22, color="#0047AB", family="Arial, sans-serif", weight="bold"),
            x=0.5,
            xanchor="center"
        ),
        xaxis=dict(
            title="Optimization Method",
            title_font=dict(size=14, color="#1E3A8A", family="Arial, sans-serif"),
            tickfont=dict(size=12, color="#374151"),
            showgrid=True,
            gridcolor="#E5E7EB"
        ),
        yaxis=dict(
            title="Time (seconds)",
            title_font=dict(size=14, color="#1E3A8A", family="Arial, sans-serif"),
            tickfont=dict(size=12, color="#374151"),
            gridcolor="#E5E7EB"
        ),
        height=400,
        template="plotly_white",
        margin=dict(l=20, r=20, t=60, b=40),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#F0F7FF",
        hoverlabel=dict(
            bgcolor="#E6F0FF",
            font_size=14,
            font_family="Arial, sans-serif"
        )
    )

    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Display theoretical scaling for larger portfolios with enhanced styling
    st.markdown("""
    <div class="highlight" style="background-color:#F0FDF4; border-left:5px solid #10B981; margin-top:30px;">
        <h2 style="margin-top:0; display:flex; align-items:center;">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" style="margin-right:10px">
                <path d="M7 15L12 20L17 15M7 9L12 4L17 9" stroke="#10B981" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <span style="color:#0000FF; font-weight:700; font-size:24px; text-shadow:none;">Scaling Projection</span>
        </h2>
        <p style="color:#4B5563; margin-bottom:20px;">
            The chart below projects how computation time would scale with increasing portfolio size.
            Note how standard optimization time grows non-linearly while our fast optimization remains nearly constant,
            creating an exponentially widening performance gap as portfolio size increases.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Create a container for the scaling chart with enhanced styling
    st.markdown("""
    <div class="chart-container" style="position:relative;">
        <div style="position:absolute; top:10px; right:10px; background-color:rgba(255,255,255,0.7); padding:5px 10px; border-radius:4px; font-size:12px; color:#6B7280; z-index:1000;">
            <span style="font-weight:bold;">TIP:</span> Hover over chart elements for details
        </div>
    """, unsafe_allow_html=True)

    # Create data for scaling chart with more data points for smoother curve
    asset_sizes = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
    # Use the updated formula for standard times - slower for larger portfolios
    standard_times = []
    for n in asset_sizes:
        if n >= 800:
            standard_times.append(0.00015 * (n ** 1.9))
        else:
            standard_times.append(0.0001 * (n ** 1.8))

    # Fast times are now even faster and slightly variable
    fast_times = [0.5 if n <= 500 else 0.6 for n in asset_sizes]

    # Create scaling chart with enhanced styling
    fig2 = go.Figure()

    # Add area under standard optimization curve
    fig2.add_trace(
        go.Scatter(
            x=asset_sizes,
            y=standard_times,
            mode="lines+markers",
            name="Standard Optimization",
            line=dict(color="#4C72B0", width=4, shape="spline"),
            marker=dict(size=8, color="#4C72B0", line=dict(width=1, color="white")),
            hovertemplate="<b>Assets: %{x}</b><br>Time: %{y:.2f}s<extra></extra>",
            fill="tozeroy",
            fillcolor="rgba(76, 114, 176, 0.1)"
        )
    )

    # Add area under fast optimization curve
    fig2.add_trace(
        go.Scatter(
            x=asset_sizes,
            y=fast_times,
            mode="lines+markers",
            name="Fast Optimization",
            line=dict(color="#55A868", width=4, shape="spline"),
            marker=dict(size=8, color="#55A868", line=dict(width=1, color="white")),
            hovertemplate="<b>Assets: %{x}</b><br>Time: %{y:.2f}s<extra></extra>",
            fill="tozeroy",
            fillcolor="rgba(85, 168, 104, 0.1)"
        )
    )

    # Add vertical line at current asset count with enhanced styling
    fig2.add_vline(
        x=num_assets,
        line=dict(dash="dash", color="#6B7280", width=2),
        annotation=dict(
            text=f"Current: {num_assets} assets",
            font=dict(size=14, color="#1E3A8A"),
            bgcolor="rgba(255, 255, 255, 0.8)",
            bordercolor="#E5E7EB",
            borderwidth=1,
            borderpad=4,
            x=num_assets,
            xanchor="left",
            yanchor="top"
        ),
        annotation_position="top right"
    )

    # Add annotation to highlight the growing gap
    max_asset = 1000
    standard_max_time = 0.00015 * (max_asset ** 1.9)  # Updated formula
    fast_max_time = 0.6  # Updated faster time

    fig2.add_annotation(
        x=max_asset,
        y=(standard_max_time + fast_max_time) / 2,
        text=f"{standard_max_time/fast_max_time:.1f}x gap at 1,000 assets",
        showarrow=True,
        arrowhead=2,
        arrowsize=1,
        arrowwidth=2,
        arrowcolor="#1E3A8A",
        font=dict(size=14, color="#1E3A8A", family="Arial, sans-serif"),
        align="center",
        xref="x",
        yref="y",
        ax=-60,
        ay=0
    )

    # Update layout with enhanced styling
    fig2.update_layout(
        title=dict(
            text="Optimization Time Scaling by Portfolio Size",
            font=dict(size=22, color="#0047AB", family="Arial, sans-serif", weight="bold"),
            x=0.5,
            xanchor="center"
        ),
        xaxis=dict(
            title="Number of Assets",
            title_font=dict(size=14, color="#1E3A8A", family="Arial, sans-serif"),
            tickfont=dict(size=12, color="#374151"),
            gridcolor="#E5E7EB",
            showgrid=True
        ),
        yaxis=dict(
            title="Time (seconds)",
            title_font=dict(size=14, color="#1E3A8A", family="Arial, sans-serif"),
            tickfont=dict(size=12, color="#374151"),
            gridcolor="#E5E7EB",
            showgrid=True
        ),
        height=500,
        template="plotly_white",
        margin=dict(l=20, r=20, t=60, b=40),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            bgcolor="rgba(255, 255, 255, 0.8)",
            bordercolor="#E5E7EB",
            borderwidth=1
        ),
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#F0F7FF",
        hoverlabel=dict(
            bgcolor="#FFFFFF",
            font_size=14,
            font_family="Arial, sans-serif",
            font_color="#1F2937"
        ),
        hovermode="x unified"
    )
    
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Portfolio allocation visualization with enhanced styling
    st.markdown("""
    <div class="highlight" style="background-color:#F0F7FF; border-left:5px solid #6366F1; margin-top:30px;">
        <h2 style="margin-top:0; display:flex; align-items:center;">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" style="margin-right:10px">
                <path d="M11 3.05493C6.50005 3.55238 3 7.36745 3 12C3 16.9706 7.02944 21 12 21C16.6326 21 20.4476 17.5 20.9451 13H11V3.05493Z" stroke="#6366F1" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M20.4878 9H15V3.5123C17.5572 4.41613 19.5839 6.44285 20.4878 9Z" stroke="#6366F1" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <span style="color:#0000FF; font-weight:700; font-size:24px; text-shadow:none;">Portfolio Allocation Comparison</span>
        </h2>
        <p style="color:#4B5563; margin-bottom:20px;">
            The charts below show the top 10 holdings in each optimized portfolio.
            Notice how our fast optimization algorithm creates a more balanced allocation
            with better diversification across assets.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Create a container for the allocation charts with enhanced styling
    st.markdown("""
    <div class="chart-container" style="position:relative;">
        <div style="position:absolute; top:10px; right:10px; background-color:rgba(255,255,255,0.7); padding:5px 10px; border-radius:4px; font-size:12px; color:#6B7280; z-index:1000;">
            <span style="font-weight:bold;">TIP:</span> Hover over chart elements for details
        </div>
    """, unsafe_allow_html=True)

    # Create simplified visualization of top holdings
    top_n = 10  # Show top 10 holdings
    
    # Sort weights and get top holdings
    std_top_indices = np.argsort(standard_results["weights"])[-top_n:][::-1]
    fast_top_indices = np.argsort(fast_results["weights"])[-top_n:][::-1]
    
    std_top_weights = standard_results["weights"][std_top_indices]
    fast_top_weights = fast_results["weights"][fast_top_indices]
    
    # Create labels for assets
    std_labels = [f"Asset {i+1}" for i in std_top_indices]
    fast_labels = [f"Asset {i+1}" for i in fast_top_indices]
    
    # Create subplots
    fig3 = make_subplots(
        rows=1, cols=2,
        subplot_titles=("Standard Optimization", "Fast Optimization"),
        specs=[[{"type": "pie"}, {"type": "pie"}]]
    )
    
    # Add pie charts
    fig3.add_trace(
        go.Pie(
            labels=std_labels,
            values=std_top_weights,
            name="Standard",
            marker=dict(colors=plt.cm.Blues(np.linspace(0.5, 0.9, len(std_top_weights)))),
            textinfo="label+percent",
            hole=0.4,
        ),
        row=1, col=1
    )
    
    fig3.add_trace(
        go.Pie(
            labels=fast_labels,
            values=fast_top_weights,
            name="Fast",
            marker=dict(colors=plt.cm.Greens(np.linspace(0.5, 0.9, len(fast_top_weights)))),
            textinfo="label+percent",
            hole=0.4,
        ),
        row=1, col=2
    )
    
    # Update layout with enhanced styling
    fig3.update_layout(
        height=500,
        template="plotly_white",
        margin=dict(l=20, r=20, t=80, b=20),
        annotations=[
            dict(
                text="Top 10 Holdings",
                x=0.5,
                y=0.5,
                font=dict(size=16, color="#1E3A8A", family="Arial, sans-serif"),
                showarrow=False
            )
        ],
        title=dict(
            text="Portfolio Allocation Comparison",
            font=dict(size=22, color="#0047AB", family="Arial, sans-serif", weight="bold"),
            x=0.5,
            xanchor="center"
        ),
        plot_bgcolor="#F8FAFC",
        paper_bgcolor="#F0F7FF",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5,
            bgcolor="rgba(255, 255, 255, 0.8)",
            bordercolor="#E5E7EB",
            borderwidth=1
        ),
        hoverlabel=dict(
            bgcolor="white",
            font_size=14,
            font_family="Arial, sans-serif"
        )
    )

    # Update subplot titles with better styling
    fig3.update_annotations(
        font=dict(size=16, color="#4B5563", family="Arial, sans-serif")
    )

    st.plotly_chart(fig3, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Add comparison insights with enhanced styling
    st.markdown("""
    <div style="display:flex; justify-content:space-between; margin-top:10px; margin-bottom:30px; flex-wrap:wrap; gap:15px;">
        <div style="flex:1; min-width:250px; background-color:#EBF5FF; padding:18px; border-radius:8px; box-shadow:0 4px 6px rgba(0, 0, 0, 0.05); border-left:4px solid #4C72B0;">
            <h4 style="color:#4C72B0; margin-top:0; font-size:16px; display:flex; align-items:center;">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" style="margin-right:8px">
                    <path d="M12 8V12L15 15M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z" stroke="#4C72B0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                Standard Optimization
            </h4>
            <ul style="color:#374151; margin-bottom:0; padding-left:20px; line-height:1.6;">
                <li><strong>Less balanced</strong> allocation across assets</li>
                <li><strong>Higher concentration</strong> in top assets</li>
                <li>Potentially <strong>higher specific risk</strong> exposure</li>
            </ul>
        </div>
        <div style="flex:1; min-width:250px; background-color:#ECFDF5; padding:18px; border-radius:8px; box-shadow:0 4px 6px rgba(0, 0, 0, 0.05); border-left:4px solid #55A868;">
            <h4 style="color:#55A868; margin-top:0; font-size:16px; display:flex; align-items:center;">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" style="margin-right:8px">
                    <path d="M13 10V3L4 14H11V21L20 10H13Z" stroke="#55A868" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                Fast Optimization
            </h4>
            <ul style="color:#374151; margin-bottom:0; padding-left:20px; line-height:1.6;">
                <li><strong>More balanced</strong> diversification strategy</li>
                <li><strong>Optimal risk-adjusted</strong> weight distribution</li>
                <li>Better <strong>long-term performance</strong> potential</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Key insights with enhanced styling - using Streamlit components instead of raw HTML
    st.markdown("""
    <div class="insights-container">
        <h2 style="margin-top:0; display:flex; align-items:center;">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" style="margin-right:10px">
                <path d="M9 21H5C4.46957 21 3.96086 20.7893 3.58579 20.4142C3.21071 20.0391 3 19.5304 3 19V5C3 4.46957 3.21071 3.96086 3.58579 3.58579C3.96086 3.21071 4.46957 3 5 3H19C19.5304 3 20.0391 3.21071 20.4142 3.58579C20.7893 3.96086 21 4.46957 21 5V19C21 19.5304 20.7893 20.0391 20.4142 20.4142C20.0391 20.7893 19.5304 21 19 21H15M9 21V15C9 14.4696 9.21071 13.9609 9.58579 13.5858C9.96086 13.2107 10.4696 13 11 13H13C13.5304 13 14.0391 13.2107 14.4142 13.5858C14.7893 13.9609 15 14.4696 15 15V21M9 21H15M12 7H12.01M8 7H8.01M16 7H16.01M12 10H12.01M8 10H8.01M16 10H16.01" stroke="#3B82F6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <span style="color:#0000FF; font-weight:700; font-size:24px; text-shadow:none;">Key Insights</span>
        </h2>
    </div>
    """, unsafe_allow_html=True)

    # Create two columns for the insights using Streamlit's column layout
    insights_col1, insights_col2 = st.columns(2)

    with insights_col1:
        st.markdown("""
        <div style="background-color:#F8FAFC; padding:25px; border-radius:12px; box-shadow:0 4px 12px rgba(0, 0, 0, 0.05); height:100%;">
            <h3 style="margin-top:0; color:#1E3A8A; display:flex; align-items:center;">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" style="margin-right:8px">
                    <path d="M16 8V16M12 11V16M8 14V16M6 20H18C19.1046 20 20 19.1046 20 18V6C20 4.89543 19.1046 4 18 4H6C4.89543 4 4 4.89543 4 6V18C4 19.1046 4.89543 20 6 20Z" stroke="#1E3A8A" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                <span style="color:#0000FF; font-weight:700; font-size:18px;">Performance Summary</span>
            </h3>
        </div>
        """, unsafe_allow_html=True)

        # Speed improvement metric
        st.markdown(f"""
        <div style="display:flex; align-items:center; margin-bottom:15px; background-color:#FFFFFF; padding:12px; border-radius:8px; border:1px solid #E5E7EB;">
            <div style="width:40px; height:40px; background-color:#EFF6FF; border-radius:50%; display:flex; align-items:center; justify-content:center; margin-right:15px;">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                    <path d="M13 10V3L4 14H11V21L20 10H13Z" stroke="#3B82F6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
            </div>
            <div>
                <div style="font-size:15px; color:#0000FF; font-weight:600;">Speed Improvement</div>
                <div style="font-size:18px; font-weight:bold; color:#1E3A8A;">{standard_results['computation_time']/fast_results['computation_time']:.1f}x faster</div>
            </div>
        </div>
      """, unsafe_allow_html=True)

        # Return enhancement metric
        st.markdown(f"""
          <div style="display:flex; align-items:center; margin-bottom:15px; background-color:#FFFFFF; padding:12px; border-radius:8px; border:1px solid #E5E7EB;">
            <div style="width:40px; height:40px; background-color:#ECFDF5; border-radius:50%; display:flex; align-items:center; justify-content:center; margin-right:15px;">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                    <path d="M16 8V16M12 11V16M8 14V16M6 20H18C19.1046 20 20 19.1046 20 18V6C20 4.89543 19.1046 4 18 4H6C4.89543 4 4 4.89543 4 6V18C4 19.1046 4.89543 20 6 20Z" stroke="#10B981" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>
            <div>
                <div style="font-size:15px; color:#0000FF; font-weight:600;">Return Enhancement</div>
                <div style="font-size:18px; font-weight:bold; color:#10B981;">+{fast_results['expected_return'] - standard_results['expected_return']:.2f}%</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Risk reduction metric
        st.markdown(f"""
        <div style="display:flex; align-items:center; margin-bottom:15px; background-color:#F3F4F6; padding:12px; border-radius:8px;">
            <div style="width:40px; height:40px; background-color:#FEF2F2; border-radius:50%; display:flex; align-items:center; justify-content:center; margin-right:15px;">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                    <path d="M12 9V11M12 15H12.01M5.07183 19H18.9282C20.4678 19 21.4301 17.3333 20.6603 16L13.7321 4C12.9623 2.66667 11.0378 2.66667 10.268 4L3.33978 16C2.56998 17.3333 3.53223 19 5.07183 19Z" stroke="#EF4444" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
            </div>
            <div>
                <div style="font-size:14px; color:#6B7280;">Risk Reduction</div>
                <div style="font-size:18px; font-weight:bold; color:#EF4444;">-{standard_results['volatility'] - fast_results['volatility']:.2f}%</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Efficiency metric
        st.markdown(f"""
        <div style="display:flex; align-items:center; background-color:#F3F4F6; padding:12px; border-radius:8px;">
            <div style="width:40px; height:40px; background-color:#EFF6FF; border-radius:50%; display:flex; align-items:center; justify-content:center; margin-right:15px;">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                    <path d="M9 12L11 14L15 10M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z" stroke="#6366F1" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
            </div>
            <div>
                <div style="font-size:14px; color:#6B7280;">Efficiency (Sharpe)</div>
                <div style="font-size:18px; font-weight:bold; color:#6366F1;">+{fast_results['sharpe_ratio'] - standard_results['sharpe_ratio']:.2f}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with insights_col2:
        st.markdown("""
        <div style="background-color:#F8FAFC; padding:25px; border-radius:12px; box-shadow:0 4px 12px rgba(0, 0, 0, 0.05); height:100%;">
            <h3 style="margin-top:0; color:#1E3A8A; display:flex; align-items:center;">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" style="margin-right:8px">
                    <path d="M7 15L12 20L17 15M7 9L12 4L17 9" stroke="#1E3A8A" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                <span style="color:#0000FF; font-weight:700; font-size:18px;">Scaling Benefits</span>
            </h3>
        </div>
        """, unsafe_allow_html=True)

        # Scaling comparison
        st.markdown(f"""
        <div style="background-color:#FFFFFF; padding:15px; border-radius:8px; margin-bottom:15px; border:1px solid #E5E7EB;">
            <div style="font-size:16px; color:#0000FF; font-weight:600; margin-bottom:5px;">At 1,000 assets:</div>
            <div style="display:flex; justify-content:space-between; margin-bottom:10px;">
                <div style="font-size:16px; font-weight:bold; color:#4C72B0;">Standard:</div>
                <div style="font-size:16px; font-weight:bold; color:#4C72B0;">{0.00015 * (1000 ** 1.9):.1f} seconds</div>
            </div>
            <div style="display:flex; justify-content:space-between;">
                <div style="font-size:16px; font-weight:bold; color:#55A868;">Fast:</div>
                <div style="font-size:16px; font-weight:bold; color:#55A868;">0.6 seconds</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Explanation text
        st.markdown("""
        <p style="color:#4B5563; line-height:1.6;">
            With larger portfolios, the performance gap widens exponentially. Our algorithm maintains
            near-constant time complexity regardless of portfolio size, while traditional methods
            slow down dramatically as the number of assets increases.
        </p>
        """, unsafe_allow_html=True)

        # Business impact
        st.markdown("""
        <div style="background-color:#FFFFFF; padding:15px; border-radius:8px; margin-top:15px; border:1px solid #BFDBFE;">
            <div style="font-weight:bold; color:#0000FF; margin-bottom:5px; font-size:16px;">Business Impact</div>
            <ul style="color:#4B5563; margin-bottom:0; padding-left:20px;">
                <li>Faster decision-making in volatile markets</li>
                <li>Ability to process larger, more diverse portfolios</li>
                <li>Reduced computational costs and infrastructure needs</li>
                <li>More frequent rebalancing opportunities</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# Enhanced footer with current year
current_year = datetime.now().year
st.markdown(f"""
<div class="footer">
    <div style="display:flex; justify-content:center; align-items:center; margin-bottom:10px;">
        <div style="font-size:20px; font-weight:bold; color:#1E3A8A; display:flex; align-items:center;">
            <span style="margin-right:8px;">💼</span> FastPortfolio™
        </div>
    </div>
    <div style="margin-bottom:10px;">
        <a href="#" style="color:#3B82F6; text-decoration:none; margin:0 10px;">Documentation</a>
        <a href="#" style="color:#3B82F6; text-decoration:none; margin:0 10px;">API</a>
        <a href="#" style="color:#3B82F6; text-decoration:none; margin:0 10px;">Contact</a>
    </div>
    <p style="color:#6B7280; font-size:14px; margin-bottom:5px;">
        © {current_year} FastPortfolio™ | Enterprise Demo Version 1.2
    </p>
    <p style="color:#9CA3AF; font-size:12px; margin:0;">
        All data simulated for demonstration purposes. Performance metrics are illustrative only.
    </p>
</div>
""", unsafe_allow_html=True)
