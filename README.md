# Engineering Career Advisor – Tamil Nadu

A Flask-based engineering education and career guidance application for students and parents exploring engineering colleges, courses, career paths, and admission possibilities in Tamil Nadu.

The application brings several student-oriented tools together in one place:

- Search government engineering colleges by course.
- Search government engineering colleges by district.
- Explore free online courses for computer science and related domains.
- View course overviews, career paths, typical eligibility, and job roles.
- Take a domain-oriented engineering quiz.
- Estimate college admission possibilities from a cutoff mark, category, and course.

## Features

### Government college search by course

Select an engineering course to view matching colleges from the bundled `ctoclg.csv` dataset. Results include the college code, college name, and website link.

### Government college search by district

Select a Tamil Nadu district to list matching colleges and their official website links.

### Course recommendation system

The `/ecourse` module uses the serialized course data and similarity matrix in `models/` to recommend six related online courses for a selected course. Recommended course links open in a new browser tab.

### Course and career-path guides

The `/courseandpath` section contains individual guides for engineering domains such as Computer Science, Information Technology, Artificial Intelligence and Data Science, Electronics and Communication, Mechanical, Civil, Robotics, Biotechnology, Textile Technology, and others. The guides describe relevant study options, typical eligibility, postgraduate pathways, and possible job roles.

### Engineering-domain quiz

The `/quiz` page provides a quiz experience to help users explore engineering domains that may match their interests.

### Cutoff-based college possibility estimator

The `/cutoff` and `/predict` flow filters the bundled college cutoff data by:

- Course
- Reservation category
- Entered cutoff mark

Each matching college is classified as **High**, **Medium**, or **Low** possibility using the difference between the entered cutoff and the stored college cutoff:

| Classification | Condition |
|---|---|
| High | Difference is at least 5 |
| Medium | Difference is from 0 up to, but not including, 5 |
| Low | Difference is below 0 |

The results page displays the matching colleges, sorted by score, together with interactive Plotly bar and pie charts.

## Technology stack

- **Python**
- **Flask** for the web application
- **Pandas** and **NumPy** for data processing
- **scikit-learn/joblib/pickle** for the bundled recommendation artifacts
- **Plotly** for cutoff-result visualizations
- **Jinja2** templates for server-rendered pages
- **HTML/CSS/JavaScript**, including Tailwind CSS via CDN on the course recommendation page
- **Gunicorn** included in the dependency list for deployment

## Project structure

```text
eng-adv/
├── app.py                         # Flask application and route definitions
├── requirements.txt               # Pinned Python dependencies
├── ctoclg.csv                    # Course-wise Tamil Nadu college dataset
├── models/
│   ├── college_data.pkl           # College cutoff data
│   ├── course_list.pkl            # Serialized course list
│   ├── courses.pkl                # Course names and URLs
│   └── similarity.pkl             # Course similarity matrix
├── static/
│   ├── assests/                   # Images and other static assets
│   └── possibility_plot.png       # Static plot asset
└── templates/
    ├── home.html                  # Landing page
    ├── ind.html                   # Course-search form
    ├── res.html                   # Course-search results
    ├── inddist.html               # District-search form
    ├── indistres.html             # District-search results
    ├── ecourse.html               # Course recommendation page
    ├── courses&path.html          # Course and career-path index
    ├── courses/                   # Individual course guides
    ├── quiz.html                  # Engineering-domain quiz
    ├── cutoff.html                # Cutoff input form
    └── cutoffresult.html           # Cutoff results and charts
```

## Requirements

- Python 3.10 or newer is recommended.
- `pip` and a virtual environment tool.
- The repository's bundled files under `models/`, `static/`, and `templates/` must remain in their expected locations. The application loads these files using relative paths from the project root.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/monish18106/eng-adv.git
   cd eng-adv
   ```

2. Create and activate a virtual environment:

   **macOS/Linux**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

   **Windows PowerShell**

   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

3. Install the pinned dependencies:

   ```bash
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

## Running locally

Start the Flask application from the repository root:

```bash
python app.py
```

The application runs with Flask debug mode enabled by the current source configuration. Open the local URL shown in the terminal, typically:

```text
http://127.0.0.1:5000
```

For a production-style process using the included Gunicorn dependency:

```bash
gunicorn app:app
```

## Application routes

| Route | Purpose |
|---|---|
| `/` | Landing page |
| `/bycourses` | Search colleges by engineering course |
| `/bydist` | Search colleges by district |
| `/ecourse` | Recommend related online courses |
| `/courseandpath` | Browse course and career-path guides |
| `/quiz` | Take the engineering-domain quiz |
| `/cutoff` | Open the cutoff estimator |
| `/predict` | Process cutoff-estimator submissions |

The course guide pages are available below `/courseandpath/`, with route names for the individual engineering domains defined in `app.py`.

## Data and recommendation artifacts

The repository includes the data and serialized artifacts required to run the application without a separate model-training step:

- `ctoclg.csv` contains college codes, names, districts, website URLs, and course availability indicators.
- `models/college_data.pkl` contains college, course, category, cutoff, and chance-related records used by the cutoff estimator.
- `models/courses.pkl` contains course names and course URLs.
- `models/course_list.pkl` contains the serialized list used to populate the course input suggestions.
- `models/similarity.pkl` contains the similarity matrix used to generate related-course recommendations.

Do not rename or move these files unless the corresponding paths in `app.py` are updated as well.

## How the cutoff estimator works

When a user submits a cutoff, category, and course, the application filters `models/college_data.pkl` and calculates:

```text
Score = entered cutoff - stored college cutoff
```

It then assigns the possibility category, creates Plotly visualizations, sorts the colleges by score in descending order, and renders the results in `templates/cutoffresult.html`.

The labels are estimates based on the bundled dataset and the application's scoring rule. They should not be treated as an official admission guarantee.

## Troubleshooting

### Model or data files are not found

Run the application from the repository root and verify that the following files exist:

```text
models/college_data.pkl
models/similarity.pkl
models/courses.pkl
models/course_list.pkl
ctoclg.csv
```

### A course recommendation is empty

The submitted course name must match one of the course names loaded from `models/courses.pkl`. Use the suggestions shown by the course input field.

### No colleges are returned

Check that the selected course or district matches the values present in `ctoclg.csv`. The course search uses the CSV column names, while the district search uses the values in the `District` column.

### Plotly charts do not render

The cutoff results embed Plotly chart HTML generated by the server. Confirm that Plotly is installed from `requirements.txt` and that the `/predict` request completes successfully.

## Important notes

- This project is intended as an educational guidance tool.
- College availability, cutoff values, course information, and external links may change over time.
- Admission decisions should be verified against official college, counselling, and government sources.
- The application currently starts with `debug=True` in `app.py`; disable debug mode before deploying to a public production environment.

## License

No license file is currently included in the repository. Add a license before redistributing or reusing the project if a particular open-source license is intended.
