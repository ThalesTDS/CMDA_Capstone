import os
import sys
import threading
import tkinter as tk
from tkinter import filedialog

from flask import Flask, request, jsonify, send_file, redirect

# Add the parent directory to the path so we can import
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from documetrics.DocuMetrics import ProjectAnalyzer

app = Flask(__name__,
            static_url_path='',
            static_folder='static')

# Define path to output CSV
OUTPUT_CSV = os.path.join(os.path.dirname(__file__), '..', 'documetrics', 'outputs', 'all_metrics_combined.csv')

# Create outputs directory if it doesn't exist
os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)

# Analysis status tracking
analysis_status = {
    'in_progress': False,
    'progress': 0,  # 0-100%
    'status_message': '',
    'result': None,
    'error': None
}


# Remove subprocess logic, use direct Tkinter dialog for folder selection
def select_folder_dialog():
    """
    Open a native folder dialog and return the selected path or None.
    """
    root = tk.Tk()
    root.withdraw()
    # Make sure the dialog appears on top
    root.attributes('-topmost', True)
    try:
        path = filedialog.askdirectory(title="Select Folder")
        return path if path else None
    except Exception:
        return None
    finally:
        root.destroy()


@app.route('/api/metrics')
def get_metrics():
    """Return metrics data from CSV file."""
    if not os.path.exists(OUTPUT_CSV) or os.path.getsize(OUTPUT_CSV) == 0:
        return jsonify({"error": "No metrics data available. Please analyze a folder first."}), 404

    return send_file(OUTPUT_CSV, mimetype='text/csv')


def run_analysis_task(file_path):
    """Run analysis in a separate thread with progress updates."""
    global analysis_status

    try:
        print("[Analysis] Starting analysis thread")
        analysis_status['in_progress'] = True
        analysis_status['progress'] = 10
        analysis_status['status_message'] = 'Validating path...'
        analysis_status['error'] = None  # Clear previous error

        # Path validation
        analysis_status['progress'] = 20
        analysis_status['status_message'] = 'Beginning analysis...'
        print("[Analysis] Path validated")

        # Run analysis
        analysis_status['progress'] = 40
        analysis_status['status_message'] = 'Processing files...'
        print("[Analysis] Calling ProjectAnalyzer.main")
        result = ProjectAnalyzer.main(file_path)
        print("[Analysis] ProjectAnalyzer.main returned")

        analysis_status['progress'] = 90
        analysis_status['status_message'] = 'Finalizing results...'
        analysis_status['result'] = result

        analysis_status['progress'] = 100
        analysis_status['status_message'] = 'Analysis complete'
        analysis_status['in_progress'] = False
        print("[Analysis] Analysis complete")
    except Exception as e:
        print("[Analysis] Exception occurred:", e)
        analysis_status['error'] = str(e)
        analysis_status['result'] = None
        analysis_status['progress'] = 100  # Ensure progress is set to 100 on error
        analysis_status['in_progress'] = False
        analysis_status['status_message'] = f'Error: {str(e)}'


@app.route('/api/analyze', methods=['POST'])
def analyze_path():
    """Handle folder path analysis."""
    global analysis_status

    # Reset status
    analysis_status = {
        'in_progress': False,
        'progress': 0,
        'status_message': '',
        'result': None,
        'error': None
    }

    data = request.json
    file_path = data.get('path')

    if not file_path:
        return jsonify({"code": -1, "message": "No folder path provided."}), 400

    # Check if analysis is already in progress
    if analysis_status['in_progress']:
        return jsonify({"code": -2, "message": "Analysis already in progress."}), 409

    # Start analysis in a separate thread
    analysis_thread = threading.Thread(target=run_analysis_task, args=(file_path,))
    analysis_thread.start()

    return jsonify({"code": 0, "message": "Analysis started."})


@app.route('/api/file-dialog', methods=['GET'])
def file_dialog():
    """Open a native folder dialog and return the selected path."""
    path = select_folder_dialog()
    if path:
        return jsonify({"path": path})
    return jsonify({"error": "No folder selected"}), 400


@app.route('/api/status')
def get_analysis_status():
    """Get the current status of analysis."""
    return jsonify(analysis_status)


@app.route('/api/download')
def download_metrics():
    """Download metrics for a specific file."""
    file_id = request.args.get('file')

    if not file_id:
        return jsonify({"error": "No file specified."}), 400

    if not os.path.exists(OUTPUT_CSV) or os.path.getsize(OUTPUT_CSV) == 0:
        return jsonify({"error": "Metrics file not found or empty."}), 404

    # In a full implementation, we would filter the CSV for just this file
    # For now, return the full CSV
    return send_file(OUTPUT_CSV,
                     as_attachment=True,
                     download_name=f"{os.path.basename(file_id)}_metrics.csv",
                     mimetype='text/csv')


@app.route('/')
def index():
    """Serve the React app welcome page."""
    return app.send_static_file('index.html')


@app.route('/dashboard')
def dashboard():
    """Serve the dashboard page."""
    # Check if there's analysis data available
    if not os.path.exists(OUTPUT_CSV) or os.path.getsize(OUTPUT_CSV) == 0:
        # Redirect to homepage if no data
        return redirect('/')
    return app.send_static_file('index.html')


# Catch-all route to handle React Router
@app.route('/<path:path>')
def catch_all(path):
    """Catch-all route to support React Router."""
    try:
        return app.send_static_file(path)
    except:
        return app.send_static_file('index.html')


if __name__ == '__main__':
    # Force threaded mode for Flask dev server
    app.run(port=5000, threaded=True, debug=True, use_reloader=True)
