import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
print(sys.path)

from analyzer.DocuMetrics import ProjectAnalyzer

from flask import Flask, render_template, request, redirect
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

app = Flask(__name__)
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load initial dataset
data_path = "mydashboard/all_metrics_combined.csv"

if os.path.exists(data_path):
    df = pd.read_csv(data_path)
else:
    # If no CSV yet, create an empty DataFrame with the expected columns
    df = pd.DataFrame(columns=[
        'identifier', 'comment_density', 'completeness', 'accuracy',
        'conciseness', 'overall_score', 'line_count', 'doc_type', 'level'
    ])

def generate_gauges(selected_file):
    if not selected_file:
        return []  # Return empty list if no file is selected

    file_data = df[df['identifier'] == selected_file]
    if file_data.empty:
        return []
    file_data = file_data.iloc[0]
    gauges = []
    for metric in ['comment_density', 'completeness', 'accuracy', 'conciseness', 'overall_score']:
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=file_data[metric],
            title={'text': metric.replace("_", " ").title()},
            gauge={'axis': {'range': [0, 1]}, 'bar': {'color': "green"}}
        ))
        fig.update_layout(
        width=180,    # << Set width
        height=170,   # << Set height
        margin=dict(l=0, r=0, t=20, b=0), 
        )
        gauges.append(fig.to_html(full_html=False))
    return gauges

def generate_radar(selected_file):
    if not selected_file:
        return None  # No radar if no file selected

    file_data = df[df['identifier'] == selected_file]
    if file_data.empty:
        return None

    file_data = df[df['identifier'] == selected_file].iloc[0]
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=[file_data['comment_density'], file_data['completeness'], file_data['accuracy'], file_data['conciseness'], file_data['overall_score']],
        theta=['Comment Density', 'Completeness', 'Accuracy', 'Conciseness', 'Overall Score'],
        fill='toself',
        name=selected_file
    ))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 1])), showlegend=False)
    return fig.to_html(full_html=False)

def generate_scatter():
    fig = px.scatter(df[df['level'] == 'file'], x='identifier', y='conciseness', color='doc_type', size='line_count')
    fig.update_layout(xaxis_title="Code File", yaxis_title="Conciseness", margin=dict(l=20, r=20, t=20, b=20))
    return fig.to_html(full_html=False)

@app.route("/", methods=["GET", "POST"])
def dashboard():
    print("Dashboard route accessed!")
    global df
    warnings_list = []  # Always define warnings_list first

    if request.method == "POST":
        print("📥 Received form data:")
        print("Request.files keys:", request.files.keys())
        print("Uploaded files:", [f.filename for f in request.files.getlist('files')])

        if 'files' not in request.files:
            return redirect("/")  # No files field in form, go back safely

        uploaded_files = request.files.getlist('files')

        if not uploaded_files or all(file.filename == '' for file in uploaded_files):
            return redirect("/")  # No files selected, reload dashboard

        for uploaded_file in uploaded_files:
            if uploaded_file and uploaded_file.filename.endswith(".py"):
                file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
                uploaded_file.save(file_path)

        # Analyze uploaded files
        warnings_list = ProjectAnalyzer.analyze_and_export(
            input_directory=UPLOAD_FOLDER,
            output_csv="mydashboard/all_metrics_combined.csv"
        )

        # Reload the new dataset
        df = pd.read_csv("mydashboard/all_metrics_combined.csv")

    # --- After POST or for normal GET, prepare dashboard view ---

    selected_file = request.args.get("file")

    if not selected_file or selected_file not in df['identifier'].values:
        file_rows = df[df['level'] == 'file']
        if not file_rows.empty:
            selected_file = file_rows['identifier'].iloc[0]
        else:
            selected_file = None  # No files yet

    gauges = generate_gauges(selected_file) if selected_file else []
    radar = generate_radar(selected_file) if selected_file else None
    scatter = generate_scatter() if not df.empty else None
    file_options = df[df['level'] == 'file']['identifier'].tolist()

    return render_template(
        "dashboard.html",
        gauges=gauges,
        radar=radar,
        scatter=scatter,
        file_options=file_options,
        selected_file=selected_file,
        warnings=warnings_list  # Always pass warnings (empty list if no upload)
    )


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)