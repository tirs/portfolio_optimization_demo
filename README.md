# Portfolio Optimization Demo

This interactive Streamlit application demonstrates the performance difference between fast optimization and standard optimization methods in portfolio management.

## Features

- **Interactive Asset Slider**: Adjust the number of assets (100-1000) to see how optimization time scales
- **Simulated Optimization**: Compare standard (O(n^1.8)) vs. fast (constant time) optimization methods
- **Visual Comparisons**: 
  - Side-by-side portfolio results
  - Computation time comparison
  - Scaling projections
  - Portfolio allocation visualization
- **Professional UI**: Clean, executive-style layout with dynamic text updates

## Installation

1. Clone this repository
2. Install the required packages:

```bash
pip install streamlit numpy pandas matplotlib plotly
```

## Running the Application

Run the Streamlit app with:

```bash
streamlit run portfolio_optimization_demo.py
```

The application will open in your default web browser.

## Deployment (Optional)

To deploy this application on Streamlit Cloud:

1. Push this code to a GitHub repository
2. Log in to [Streamlit Cloud](https://streamlit.io/cloud)
3. Create a new app and connect it to your GitHub repository
4. Select the `portfolio_optimization_demo.py` file as the main file

## Usage

1. Use the slider to select the number of assets in your portfolio
2. Adjust the risk tolerance if desired
3. Click "Compare Optimization Methods" to run the simulation
4. Explore the results, charts, and insights

## Notes

- All data is simulated for demonstration purposes
- The application is designed to showcase UI/UX and performance differences, not actual portfolio optimization algorithms