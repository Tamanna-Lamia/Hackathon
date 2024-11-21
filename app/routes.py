from flask import render_template, request, redirect, url_for, flash,send_file
from app import app
import pandas as pd
from app.Utils.standardisation import standardise_file
import os
from config import Config, DirectoryPath


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(url_for('home'))

    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(url_for('home'))

    if file and file.filename.endswith('.csv'):
        try:
            # Attempt to read the CSV file with a specified encoding
            print(file)
            data = pd.read_csv(file, encoding='utf-8')  # or try 'latin1'
            print("Read Data")
            print(data)
            standardise_file(file.filename, data)
            processed_data = data.to_dict(orient='records')
            return render_template('output.html', data=processed_data)
        except UnicodeDecodeError:
            flash('Error reading file. Please check the encoding of the CSV.')
            return redirect(url_for('home'))
    
    flash('Invalid file type. Please upload a CSV file.')
    return redirect(url_for('home'))


@app.route('/download_csv', methods=['GET'])
def download_csv():
    # Define the path to the file you want to send
    file_path = os.path.join(DirectoryPath.DOWNLOAD_FOLDER, Config.DOWNLOAD_NAME)
    
    # Check if the file exists
    if not os.path.exists(file_path):
        flash('The file does not exist.')
        return redirect(url_for('home'))

    # Send the file directly for download
    return send_file(file_path, as_attachment=True, download_name= Config.DOWNLOAD_NAME)

@app.route('/visualize')
def visualize():
    plot_files = [
        url_for('static', filename='plots/correlation_heatmap.png'),
        url_for('static', filename='plots/plot1.png'),
        url_for('static', filename='plots/plot2.png'),
        url_for('static', filename='plots/plot3.png')
    ]
    return render_template('analytics.html', plots=plot_files)  # Render a visualization page


