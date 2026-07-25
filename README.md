# AI Resume Analyzer & ATS Scoring System

An intelligent resume analysis application that compares a candidate's resume with a job description and provides an ATS-style compatibility score.

The application uses Natural Language Processing (NLP), TF-IDF, cosine similarity, keyword matching, and skill detection to identify strengths, missing skills, and areas for resume improvement.

## Features

- PDF resume upload and text extraction
- ATS-style resume match score
- Automatic job role detection
- Skill matching
- Missing skill identification
- Priority skill-gap detection
- Job description keyword extraction
- Resume completeness analysis
- TF-IDF and cosine similarity analysis
- Personalized resume recommendations
- Interactive Streamlit dashboard

## Technologies Used

- Python
- Streamlit
- Scikit-learn
- NLP
- TF-IDF
- Cosine Similarity
- Regular Expressions
- PyPDF

## How It Works

The user uploads a resume in PDF format and provides a job description.

The system extracts the resume text and compares it with the job description using multiple analysis methods.

The overall ATS-style score is calculated using:

| Component | Weight |
|---|---:|
| Skills Match | 40% |
| Keyword Match | 25% |
| Text Similarity | 20% |
| Resume Completeness | 15% |

The application then displays matched skills, missing skills, important job keywords, the detected job role, and recommendations for improving alignment with the position.

## Project Structure

```text
AI-Resume-Analyzer/
│
├── app.py
├── ats_analyzer.py
├── resume_parser.py
├── requirements.txt
├── README.md
└── .gitignore
```

### app.py

Contains the Streamlit user interface and controls the application workflow.

### ats_analyzer.py

Contains the ATS scoring, skill matching, keyword extraction, job-role detection, and text-similarity logic.

### resume_parser.py

Extracts text from uploaded PDF resumes.

## Installation

Clone the repository:

```bash
git clone https://github.com/udaychandraS2005/AI-Resume-Analyzer.git
```

Move into the project directory:

```bash
cd AI-Resume-Analyzer
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

## Run the Application

Start the Streamlit application:

```bash
streamlit run app.py
```

Then open the local Streamlit URL displayed in the terminal.

## Example Analysis

The application can provide:

- Detected job role
- Overall resume match percentage
- Skills match score
- Keyword match score
- Text similarity score
- Resume completeness score
- Matched technical skills
- Missing technical skills
- Priority skills to develop
- Important job-description keywords
- Resume improvement recommendations

## Future Improvements

- DOCX resume support
- Semantic similarity using transformer models
- AI-generated resume recommendations
- Resume section quality analysis
- Downloadable ATS analysis reports
- Expanded job-role and technical-skill database

## Disclaimer

This project provides an ATS-style resume matching estimate for educational and portfolio purposes. Actual Applicant Tracking Systems may use different parsing, ranking, and screening methods.

## Author

**Uday Chandra S**

Electronics and Communication Engineering Student  
SJC Institute of Technology

LinkedIn: https://www.linkedin.com/in/uday-chandra-52675632b

GitHub: https://github.com/udaychandraS2005