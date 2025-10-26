from flask import Flask, render_template, request
import numpy as np
import joblib
import os
import pickle
import pandas as pd
import plotly.graph_objs as go
import plotly.io as pio
app = Flask(__name__)

college_data = pd.read_pickle("models/college_data.pkl")
df = pd.read_csv('ctoclg.csv')

try:
    similarity = pickle.load(open('models/similarity.pkl', 'rb'))
    courses_df = pickle.load(open('models/courses.pkl', 'rb'))
    course_list_dicts = pickle.load(open('models/course_list.pkl', 'rb'))
except FileNotFoundError:
    print("Error: One or more model files not found. Make sure 'models/similarity.pkl', 'models/courses.pkl', and 'models/course_list.pkl' exist.")
    exit()
except Exception as e:
    print(f"Error loading model files: {e}")
    exit()

course_names = courses_df['course_name'].values.tolist()
course_url_dict = courses_df.set_index('course_name')['course_url'].to_dict()

def recommend(course_name):
    if course_name not in courses_df['course_name'].values:
        return []

    try:
        index = courses_df[courses_df['course_name'] == course_name].index[0]
        distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
        recommended_courses = []
        for i in distances[1:7]:
            recommended_name = courses_df.iloc[i[0]].course_name
            recommended_url = courses_df.iloc[i[0]].course_url
            recommended_courses.append({'name': recommended_name, 'url': recommended_url})
        return recommended_courses
    except IndexError:
        return []
    except Exception as e:
        print(f"Error during recommendation: {e}")
        return []

@app.route("/", methods=["GET"])
def home():
    return render_template("home.html")


@app.route("/bycourses", methods=["GET", "POST"])
def searchbycourse():
    if request.method == "POST":
        choice = request.form.get("course")
        if choice in df.columns:
            colleges = df[df[choice] == 1][['Code', 'Name', 'url']]
        else:
            colleges = pd.DataFrame(columns=['Code', 'Name', 'url'])
        return render_template("res.html", colleges=colleges, choice=choice)
    else:
        return render_template("ind.html")

@app.route("/bydist", methods=["GET", "POST"])
def searchbydist():
    if request.method == "POST":
        choice = request.form.get("city")
        if choice in df['District'].values:
            colleges = df[df['District'] == choice][['Code', 'Name', 'url']]
        else:
            colleges = pd.DataFrame(columns=['Code', 'Name', 'url'])
        return render_template("indistres.html", colleges=colleges, choice=choice)
    else:
        return render_template("inddist.html")

@app.route('/ecourse', methods=['GET', 'POST'])
def index():
    recommended_courses = []
    selected_course = None
    if request.method == 'POST':
        selected_course = request.form['course_name']
        recommended_courses = recommend(selected_course)
    return render_template('ecourse.html', courses=course_names, recommendations=recommended_courses, selected_course=selected_course)

@app.route('/courseandpath')
def cp():
    return render_template('courses&path.html')

@app.route('/courseandpath/aero')
def aero():
    return render_template('courses/aero.html')

@app.route('/courseandpath/aids')
def aids():
    return render_template('courses/aids.html')

@app.route('/courseandpath/aiml')
def aiml():
    return render_template('courses/aiml.html')

@app.route('/courseandpath/appareltech')
def apparel_tech():
    return render_template('courses/appareltech.html')

@app.route('/courseandpath/auto')
def auto():
    return render_template('courses/auto.html')

@app.route('/courseandpath/biomed')
def biomed():
    return render_template('courses/biomed.html')

@app.route('/courseandpath/biotech')
def biotech():
    return render_template('courses/biotech.html')

@app.route('/courseandpath/ceramic')
def ceramic():
    return render_template('courses/ceramic.html')

@app.route('/courseandpath/chemical')
def chemical():
    return render_template('courses/chemical.html')

@app.route('/courseandpath/civil')
def civil():
    return render_template('courses/civil.html')

@app.route('/courseandpath/csbs')
def csbs():
    return render_template('courses/csbs.html')

@app.route('/courseandpath/cse')
def cse():
    return render_template('courses/cse.html')

@app.route('/courseandpath/ece')
def ece():
    return render_template('courses/ece.html')

@app.route('/courseandpath/eee')
def eee():
    return render_template('courses/eee.html')

@app.route('/courseandpath/ei')
def ei():
    return render_template('courses/ei.html')

@app.route('/courseandpath/elecse')
def ele_cse():
    return render_template('courses/elecse.html')

@app.route('/courseandpath/ev')
def ev():
    return render_template('courses/ev.html')

@app.route('/courseandpath/fash')
def fash():
    return render_template('courses/fash.html')

@app.route('/courseandpath/ft')
def ft():
    return render_template('courses/ft.html')

@app.route('/courseandpath/geo')
def geo():
    return render_template('courses/geo.html')

@app.route('/courseandpath/ic')
def ic():
    return render_template('courses/ic.html')

@app.route('/courseandpath/ind')
def ind():
    return render_template('courses/ind.html')

@app.route('/courseandpath/indbio')
def indbio():
    return render_template('courses/indbio.html')

@app.route('/courseandpath/it')
def it():
    return render_template('courses/it.html')

@app.route('/courseandpath/leather')
def leather():
    return render_template('courses/leather.html')

@app.route('/courseandpath/manu')
def manu():
    return render_template('courses/manu.html')

@app.route('/courseandpath/matsci')
def matsci():
    return render_template('courses/matsci.html')

@app.route('/courseandpath/mech')
def mech():
    return render_template('courses/mech.html')

@app.route('/courseandpath/mecht')
def mecht():
    return render_template('courses/mecht.html')

@app.route('/courseandpath/metall')
def metall():
    return render_template('courses/metall.html')

@app.route('/courseandpath/min')
def min_course():
    return render_template('courses/min.html')

@app.route('/courseandpath/ph')
def ph():
    return render_template('courses/ph.html')

@app.route('/courseandpath/print')
def print_course():
    return render_template('courses/print.html')

@app.route('/courseandpath/pro')
def pro():
    return render_template('courses/pro.html')

@app.route('/courseandpath/pt')
def pt():
    return render_template('courses/pt.html')

@app.route('/courseandpath/rob')
def rob():
    return render_template('courses/rob.html')

@app.route('/courseandpath/rub')
def rub():
    return render_template('courses/rub.html')

@app.route('/courseandpath/textile')
def textile():
    return render_template('courses/textile.html')

@app.route('/quiz')
def quiz():
    return render_template('quiz.html')


@app.route('/cutoff')
def ct():
    courses = {
        'AERO': 'Aeronautical Engineering',
        'AIDS': 'Artificial Intelligence & Data Science',
        'AUTO': 'Automobile Engineering',
        'BIOT': 'Biotechnology',
        'BME': 'Bio-Medical Engineering',
        'CERA': 'Ceramic Engineering',
        'CHE': 'Chemical Engineering',
        'CIV': 'Civil Engineering',
        'CSE': 'Computer Science and Engineering',
        'ECE': 'Electronics and Communication Engineering',
        'ECSE': 'Electronics & Computer Science Engineering',
        'EEE': 'Electrical and Electronics Engineering',
        'EI': 'Electronics and Instrumentation',
        'ENV': 'Environmental Engineering',
        'FASH': 'Fashion Technology',
        'GEO': 'Geo-Informatics',
        'IC': 'Instrumentation & Control',
        'INBIO': 'Industrial Biotechnology',
        'IND': 'Industrial Engineering',
        'IT': 'Information Technology',
        'MECH': 'Mechanical Engineering',
        'MECT': 'Mechatronics Engineering',
        'METAL': 'Metallurgical Engineering',
        'MINI': 'Mining Engineering',
        'PETRO': 'Petroleum Engineering',
        'PHARMA': 'Pharmaceutical Engineering',
        'PRINT': 'Printing Technology',
        'PROD': 'Production Engineering',
        'ROBO': 'Robotics Engineering',
        'RUBER': 'Rubber Technology',
        'TEXT': 'Textile Technology',
        'VLSI': 'VLSI Design',
        'MATS': 'Materials Engineering',
        'MANU': 'Manufacturing Engineering',
        'LEA': 'Leather Technology',
        'FT': 'Food Technology'
    }
    categories = ['OC','BC','BCM','MBC','SC','SCA','ST']
    return render_template('cutoff.html', courses=courses, categories=categories)

@app.route('/predict', methods=['POST'])
def predict():
    cutoff = float(request.form['cutoff'])
    category = request.form['category']
    course = request.form['course']

    # Filter data
    df_filtered = college_data[(college_data['Course']==course) & (college_data['Category']==category)].copy()
    df_filtered['Score'] = cutoff - df_filtered['Cutoff']

    # Classify High / Medium / Low
    conditions = [
        df_filtered['Score'] >= 5,
        (df_filtered['Score'] < 5) & (df_filtered['Score'] >= 0),
        df_filtered['Score'] < 0
    ]
    choices = ['High','Medium','Low']
    df_filtered['Possibility'] = np.select(conditions, choices, default='Low')

    # --- Plotly Bar Chart ---
    bar_data = df_filtered.groupby('Possibility')['Name'].count().reindex(['High','Medium','Low']).fillna(0)
    bar_fig = go.Figure(
        data=[go.Bar(
            x=bar_data.index,
            y=bar_data.values,
            marker_color=['#2ecc71','#f1c40f','#e74c3c'],
            text=bar_data.values,
            textposition='auto'
        )]
    )
    bar_fig.update_layout(
        title='College Admission Possibilities',
        xaxis_title='Possibility',
        yaxis_title='Number of Colleges',
        template='plotly_dark',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    bar_div = pio.to_html(bar_fig, full_html=False)

    # --- Plotly Pie Chart ---
    pie_data = df_filtered['Possibility'].value_counts().reindex(['High','Medium','Low']).fillna(0)
    pie_fig = go.Figure(
        data=[go.Pie(
            labels=pie_data.index,
            values=pie_data.values,
            marker_colors=['#2ecc71','#f1c40f','#e74c3c'],
            hole=0.3
        )]
    )
    pie_fig.update_layout(title='Possibility Distribution', template='plotly_dark')
    pie_div = pio.to_html(pie_fig, full_html=False)

    # Sort colleges
    df_filtered = df_filtered.sort_values(by='Score', ascending=False)
    colleges = df_filtered[['Code','Name','Cutoff','Score','Possibility']].to_dict(orient='records')

    return render_template('cutoffresult.html', colleges=colleges, bar_div=bar_div, pie_div=pie_div)

if __name__ == "__main__":
    app.run(debug=True)


