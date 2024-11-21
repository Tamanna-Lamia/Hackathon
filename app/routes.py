from flask import render_template, request, redirect, url_for, flash
from app import app
import pandas as pd

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
            data = pd.read_csv(file, encoding='ISO-8859-1')  # or try 'latin1'
            processed_data = data.to_dict(orient='records')
            return render_template('output.html', data=processed_data)
        except UnicodeDecodeError:
            flash('Error reading file. Please check the encoding of the CSV.')
            return redirect(url_for('home'))
    
    flash('Invalid file type. Please upload a CSV file.')
    return redirect(url_for('home'))


@app.route('/download_csv', methods=['GET'])
def download_csv():
    if 'processed_data' not in globals():
        flash('No data available for download.')
        return redirect(url_for('home'))

    df = pd.DataFrame(processed_data)
    temp_file_path = 'uploads/processed_data.csv'
    df.to_csv(temp_file_path, index=False)

    # Serve the file for download
    response = send_file(temp_file_path, as_attachment=True, download_name='processed_data.csv')
    
    return response

@app.route('/visualize')
def visualize():
    # Logic for visualization or passing data to the new page
    return render_template('analytics.html')  # Render a visualization page


