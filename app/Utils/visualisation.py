import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import plotly.graph_objects as go
from plotly.graph_objects import Figure
import os 
from statsmodels.tsa.arima.model import ARIMA
import plotly.express as px
import plotly.io as pio
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from config import DirectoryPath

def save_fig_as_png(fig, fig_name):
    #folder_path = r"C:\Users\alkav\Documents\Hackathon\plots"
    folder_path = DirectoryPath.PLOTS_FOLDER
    file_path = os.path.join(folder_path,fig_name )

    fig.write_image(file_path, engine="kaleido", format = "png")

def plot1(df):
    # Assuming df is your dataframe
    # Select numerical columns (excluding Date)
    numerical_cols = df.select_dtypes(include=['float64', 'int64']).columns
    X = df[numerical_cols]

    # Standardize the features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Perform PCA
    pca = PCA()
    X_pca = pca.fit_transform(X_scaled)

    # Calculate explained variance ratio
    explained_variance_ratio = pca.explained_variance_ratio_
    cumulative_variance_ratio = np.cumsum(explained_variance_ratio)

    # Create an interactive scree plot using Plotly
    fig = go.Figure()

    # Add individual explained variance
    fig.add_trace(go.Scatter(
        x=np.arange(1, len(explained_variance_ratio) + 1),
        y=explained_variance_ratio,
        mode='lines+markers',
        name='Individual',
        line=dict(color='blue'),
        marker=dict(symbol='circle', size=8)
    ))

    # Add cumulative explained variance
    fig.add_trace(go.Scatter(
        x=np.arange(1, len(cumulative_variance_ratio) + 1),
        y=cumulative_variance_ratio,
        mode='lines+markers',
        name='Cumulative',
        line=dict(color='red'),
        marker=dict(symbol='circle', size=8)
    ))

    # Update layout to make the background white
    fig.update_layout(
        title='Scree Plot (Explained Variance)',
        xaxis_title='Principal Component',
        yaxis_title='Explained Variance Ratio',
        template='plotly',  # Use the default Plotly template for white background
        hovermode='closest',
        legend=dict(x=0.1, y=0.9),
        margin=dict(l=50, r=50, t=50, b=50),
        plot_bgcolor='white',  # Set the background color of the plot area
        paper_bgcolor='white'  # Set the background color of the whole paper (figure)
    )
    save_fig_as_png(fig,"plot1.png")

def plot2(df):
    # Check if 'Date' column exists
    if 'Date' not in df.columns:
        print("Date column is missing from the dataframe")
    else:
        # Convert 'Date' to datetime
        df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)

        # Check if there are any NaT values after conversion
        if df['Date'].isnull().any():
            print("Some values in 'Date' could not be converted to datetime")
        else:
            # Set 'Date' as the index
            df.set_index('Date', inplace=True)

    # Fit ARIMA model
    model = ARIMA(df['Consumption'], order=(5, 1, 0))
    model_fit = model.fit()

    # Forecast the next 30 days
    forecast = model_fit.forecast(steps=30)

    # Create a date range for the forecasted period
    forecast_dates = pd.date_range(df.index[-1], periods=31, freq='D')[1:]

    # Create the interactive plot
    fig = go.Figure()

    # Add historical data to the plot
    fig.add_trace(go.Scatter(x=df.index, y=df['Consumption'], mode='lines', name='Historical Data',
                            line=dict(color='blue')))

    # Add forecast data to the plot
    fig.add_trace(go.Scatter(x=forecast_dates, y=forecast, mode='lines', name='Forecast',
                            line=dict(color='red', dash='dash')))

    # Update layout for better interactivity and set white background
    fig.update_layout(
        title='Energy Consumption Forecast (Next 30 Days)',
        xaxis_title='Date',
        yaxis_title='Energy Consumption',
        template='plotly_white',  # Set white background
        hovermode='closest',
        plot_bgcolor='white',  # Set the plot background to white
        paper_bgcolor='white'  # Set the paper background to white
    )
    save_fig_as_png(fig, "plot2.png")

def plot3(df):
        # Create a colorful interactive scatter plot with different colors for each weather code
    fig = px.scatter(df,
                    x='daylight_duration (s)',
                    y='Consumption',
                    color='daylight_duration (s)',
                    title='Colorful Interactive Scatter Plot of daylight_duration (s) vs Energy Consumption',
                    labels={'daylight_duration (s)': 'daylight_duration (s)',
                            'Consumption': 'Energy Consumption'},
                    hover_data=['daylight_duration (s)', 'daylight_duration (s)'])

    # Update layout
    fig.update_layout(
        title_x=0.5,
        plot_bgcolor='white',
        width=900,
        height=600
    )

    # Add grid
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')


    save_fig_as_png(fig,"plot3.png")

def plot4(df):
    # Create interactive scatter plot with color based on temperature
    fig = px.scatter(df,
                    x='weather_code (wmo code)',
                    y='Consumption',
                    color='weather_code (wmo code)',  # Adding color based on temperature
                    color_continuous_scale='viridis',  # Using a colorful scale
                    title='Interactive Scatter Plot of Weather Code vs Energy Consumption',
                    labels={'weather_code (wmo code)': 'Weather Code (WMO Code)',
                            'Consumption': 'Energy Consumption',
                            'weather_code (wmo code)': 'weather_code (wmo code)'},
                    hover_data=['weather_code (wmo code)', 'weather_code (wmo code)'])

    # Update layout
    fig.update_layout(
        title_x=0.5,
        plot_bgcolor='white',
        width=900,
        height=600
    )

    # Add grid
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
    save_fig_as_png(fig, "plot4.png")

def plot5(df):
    corr = df.corr()  # Correlation matrix
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
    plt.title("Correlation Heatmap")
    folder_path = DirectoryPath.PLOTS_FOLDER
    file_path = os.path.join(folder_path,"correlation_heatmap.png" )
    plt.savefig(file_path, dpi=300, bbox_inches='tight')


def plot6(df):
    # Standardize the data
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df[['Consumption', 'temperature_2m_max (°C)', 'temperature_2m_max (°C)',
                                        'temperature_2m_max (°C)', 'rain_sum (mm)', 'snowfall_sum (cm)',
                                        'wind_speed_10m_max (km/h)']])

    # Perform PCA to reduce to 2 dimensions
    pca_2d = PCA(n_components=2)
    X_pca_2d = pca_2d.fit_transform(X_scaled)

    # Apply KMeans clustering
    kmeans = KMeans(n_clusters=3, random_state=42)
    clusters = kmeans.fit_predict(X_pca_2d)

    # Create a DataFrame for plotting
    pca_df = pd.DataFrame(X_pca_2d, columns=['PC1', 'PC2'])
    pca_df['Cluster'] = clusters

    # Create an interactive scatter plot for PCA clusters
    fig = px.scatter(pca_df, x='PC1', y='PC2', color='Cluster',
                    title='Interactive PCA Clusters',
                    labels={'PC1': 'Principal Component 1', 'PC2': 'Principal Component 2'})

    # Update layout
    fig.update_layout(
        title_x=0.5,
        plot_bgcolor='white',
        width=900,
        height=600
    )

    save_fig_as_png(fig, "plot6.png")


def visualise_data(data):
    plot1(data)
    plot2(data)
    plot3(data)
    plot4(data)
    # plot5(data)
    # plot6(data)
