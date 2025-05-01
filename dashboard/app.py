import sys
import os
import io
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
# print(sys.path)
from documetrics.DocuMetrics import ProjectAnalyzer

from flask import Flask, render_template, request, redirect, url_for, send_file
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

    def get_color(val):
        if val < 0.33:
            return "red"
        elif val < 0.66:
            return "yellow"
        else:
            return "green"

    for metric in ['comment_density', 'completeness', 'accuracy', 'conciseness', 'overall_score']:
        val = round(file_data[metric], 2)
        color = get_color(val)

        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=val,
            number={'valueformat': '.2f'},
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
        return None

    file_data = df[df['identifier'] == selected_file]
    if file_data.empty:
        return None

    file_data = df[df['identifier'] == selected_file].iloc[0]
    r_values = [
        round(file_data['comment_density'], 2),
        round(file_data['completeness'], 2),
        round(file_data['accuracy'], 2),
        round(file_data['conciseness'], 2),
        round(file_data['overall_score'], 2),
    ]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=r_values,
        theta=['Comment Density', 'Completeness', 'Accuracy', 'Conciseness'],
        fill='toself',
        name=selected_file
    ))
    fig.update_layout(
        title_text="Documentation Metrics Radar",
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1],
            )
        ),
        margin=dict(t=80, b=20),
        showlegend=False
    )
    fig.update_layout(
        updatemenus=[
            dict(
                type="buttons",
                direction="right",
                x=1.1,
                y=1.15,
                showactive=False,
                buttons=[
                    dict(
                        label="Reset Zoom",
                        method="relayout",
                        args=[{"polar.radialaxis.range": [0, 1]}]
                    )
                ]
            )
        ]
    )
    return fig.to_html(full_html=False, config={
    "displayModeBar": True,       # keep the toolbar
    "scrollZoom": False,          # disable scroll zoom
    "staticPlot": True,           # disables all interactivity including zoom, pan, hover, etc.
    "displaylogo": False          # optional: remove Plotly logo
})


def generate_scatter():
    file_df = df[df['level'] == 'file'].copy()
    file_df['short_name'] = file_df['identifier'].apply(lambda x: os.path.basename(x))
    metrics = ['accuracy', 'completeness', 'conciseness', 'comment_density', 'overall_score']

    # Initial figure with first metric
    fig = px.scatter(
    file_df,
    x='short_name',
    y='accuracy',
    color='doc_type',
    size='line_count',
    hover_data={metric: True for metric in metrics} | {
            'short_name': True,
            'line_count': True,
            'doc_type': True
    },
    labels={
            'short_name': 'File Name',
            'line_count': 'Line Count',
            'doc_type': 'Doc Type',
            'accuracy': 'Accuracy',
            'completeness': 'Completeness',
            'conciseness': 'Conciseness',
            'comment_density': 'Comment Density',
            'overall_score': 'Overall Score'
    }
)
    fig.update_traces(marker=dict(opacity=0.7))
    
    # Add buttons for dropdown menu to switch Y-axis
    fig.update_layout(
        updatemenus=[{
            "buttons": [
                {
                    "method": "update",
                    "label": metric.title().replace("_", " "),
                    "args": [{"y": [file_df[metric]]},
                             {"yaxis": {"title": metric.title().replace("_", " ")}}]
                }
                for metric in metrics
            ],
            "direction": "down",
            "showactive": True,
            "x": 0,
            "y": 1.15,
            "xanchor": "left",
            "yanchor": "top"
        }],
        title="Scatterplot: File vs. Metric",
        yaxis_title="Accuracy",  # initial y-title
        xaxis_title="File",
        margin=dict(t=80, b=40, l=40, r=40)
    )

    return fig.to_html(full_html=False)

def generate_visuals(selected_file, df):
    """
    Helper function to generate all dashboard visuals and file options.

    :param selected_file: The currently selected file identifier
    :param df: The dataframe containing file metrics
    :return: (gauges, radar, scatter, file_options)
    """
    gauges = generate_gauges(selected_file) if selected_file else []
    radar = generate_radar(selected_file) if selected_file else None
    scatter = generate_scatter() if not df.empty else None
    file_options = df[df['level'] == 'file']['identifier'].tolist()
    
    return gauges, radar, scatter, file_options


@app.route("/", methods=["GET", "POST"])
def dashboard():
    global df
    warnings_list = []  # Always define warnings_list first

    if request.method == "POST":
        print("Received form data:")
        print("Request.files keys:", request.files.keys())
        print("Uploaded files:", [f.filename for f in request.files.getlist('files')])

        if 'files' not in request.files:
            print("No 'files' field found in form!")
            return redirect("/")  # No files field in form, go back safely

        uploaded_files = request.files.getlist('files')

        if not uploaded_files or all(file.filename == '' for file in uploaded_files):
            print("No files selected for upload!")
            return redirect("/")  # No files selected, reload dashboard

        for uploaded_file in uploaded_files:
            if uploaded_file and uploaded_file.filename.endswith(".py"):
                file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
                uploaded_file.save(file_path)
                print(f"Saved uploaded file to {file_path}")

        # Analyze uploaded files
        print("Running ProjectAnalyzer on uploaded files...")
        try:
            ProjectAnalyzer.analyze_and_export(
                UPLOAD_FOLDER,
                "mydashboard/all_metrics_combined.csv"
            )
            print("ProjectAnalyzer completed successfully.")
        except Exception as e:
            print(f"Error running ProjectAnalyzer: {e}")
            return redirect(url_for('dashboard'))

         # Reload the DataFrame
        try:
            df = pd.read_csv("mydashboard/all_metrics_combined.csv")
            print("Successfully reloaded all_metrics_combined.csv")
        except Exception as e:
            print(f"Error loading CSV: {e}")         
   

        return redirect(url_for('dashboard'))
    # --- After POST or for normal GET, prepare dashboard view ---

    selected_file = request.args.get("file")

    if not selected_file or selected_file not in df['identifier'].values:
        fallback_rows = df[df['level'].isin(['file', 'project'])]
        if not fallback_rows.empty:
            selected_file = fallback_rows['identifier'].iloc[0]
        else:
            selected_file = None  # No files yet
    
    # Generate Dashboard Visuals
    gauges, radar, scatter, _ = generate_visuals(selected_file, df)

    # Show both files and project-level entry in dropdown/tabs
    display_rows = df[df['level'].isin(['file', 'project'])].copy()
    display_rows['filename'] = display_rows['identifier'].apply(
        lambda path: os.path.basename(path) if path != "Project Results" else "Summary"
    )
    # Sort so "Project Results" appears first
    display_rows['sort_order'] = display_rows['identifier'].apply(
    lambda x: 0 if x == "Project Results" else 1
    )
    display_rows = display_rows.sort_values(by='sort_order')

    file_options = list(zip(display_rows['identifier'], display_rows['filename']))
    selected_filename = None
    for identifier, fname in file_options:
        if identifier == selected_file:
            selected_filename = fname
            break

    return render_template(
        "dashboard.html",
        gauges=gauges,
        radar=radar,
        scatter=scatter,
        file_options=file_options,
        selected_file=selected_file,
        selected_filename=selected_filename,
        warnings=warnings_list  # Always pass warnings (empty list if no upload)
    )

@app.route("/download_metrics", methods=["GET"])
def download_metrics():
    selected_file = request.args.get("file")
    if not selected_file:
        return "No file specified", 400

    # Filter the selected row
    file_data = df[df['identifier'] == selected_file]
    if file_data.empty:
        return "File not found", 404

    # Convert to CSV in memory
    csv_buffer = io.StringIO()
    file_data.to_csv(csv_buffer, index=False)

    # Return as downloadable file
    csv_buffer.seek(0)
    return send_file(
        io.BytesIO(csv_buffer.getvalue().encode()),
        mimetype='text/csv',
        as_attachment=True,
        download_name=f"{os.path.basename(selected_file)}_metrics.csv"
    )
print("Reached app.run()")
if __name__ == "__main__":
    app.run(debug=True, port=5007, use_reloader=False)