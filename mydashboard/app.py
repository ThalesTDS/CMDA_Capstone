from flask import Flask, render_template, request, redirect
from code.DocuMetrics import ProjectAnalyzer
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import os

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load initial dataset
data_path = "mydashboard/all_metrics_combined.csv"
df = pd.read_csv(data_path)

def generate_gauges(selected_file):
    file_data = df[df['identifier'] == selected_file].iloc[0]
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
    global df
    if request.method == "POST":
        uploaded_file = request.files['file']
        if uploaded_file.filename.endswith(".py"):
            file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
            uploaded_file.save(file_path)

            # Analyze new files
            ProjectAnalyzer.analyze_and_export(directory=UPLOAD_FOLDER, output_file="mydashboard/all_metrics_combined.csv")

            # Reload new dataset
            df = pd.read_csv("mydashboard/all_metrics_combined.csv")

            return redirect("/")

    selected_file = request.args.get("file")
    if not selected_file or selected_file not in df['identifier'].values:
        selected_file = df[df['level'] == 'file']['identifier'].iloc[0]

    gauges = generate_gauges(selected_file)
    radar = generate_radar(selected_file)
    scatter = generate_scatter()
    file_options = df[df['level'] == 'file']['identifier'].tolist()

    return render_template("dashboard.html", gauges=gauges, radar=radar, scatter=scatter, file_options=file_options, selected_file=selected_file)

if __name__ == "__main__":
    app.run(debug=True)