
import re
import PyPDF2
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Extract text from PDF resume
def extract_resume_text(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    return text


# Clean text
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9+#.\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


# Calculate resume and job similarity
def calculate_match(resume_text, job_description):
    documents = [
        clean_text(resume_text),
        clean_text(job_description)
    ]

    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(documents)

    similarity = cosine_similarity(
        tfidf_matrix[0:1],
        tfidf_matrix[1:2]
    )[0][0]

    return round(similarity * 100, 2)


# Extract skills from resume
def extract_skills(text):

    skills_list = [
        "python", "java", "c++", "sql",
        "machine learning", "deep learning",
        "artificial intelligence", "data analysis",
        "pandas", "numpy", "matplotlib",
        "scikit-learn", "tensorflow", "pytorch",
        "excel", "power bi", "tableau",
        "html", "css", "javascript",
        "flask", "streamlit", "nlp",
        "communication", "problem solving",
        "data visualization", "git", "github"
    ]

    text = clean_text(text)

    found_skills = []

    for skill in skills_list:
        pattern = r'(?<!\w)' + re.escape(skill) + r'(?!\w)'

        if re.search(pattern, text):
            found_skills.append(skill.title())

    return found_skills


# Find missing skills
def find_missing_skills(resume_text, job_description):

    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_description)

    missing_skills = [
        skill for skill in job_skills
        if skill not in resume_skills
    ]

    return resume_skills, job_skills, missing_skills


# Generate improvement suggestions
def generate_suggestions(missing_skills, match_score):

    suggestions = []

    if missing_skills:
        suggestions.append(
            "Consider developing these job-related skills: "
            + ", ".join(missing_skills)
        )

    if match_score < 40:
        suggestions.append(
            "Add more relevant experience and skills "
            "that genuinely match the job requirements."
        )

    elif match_score < 70:
        suggestions.append(
            "Improve your resume by highlighting relevant "
            "projects and technical experience."
        )

    else:
        suggestions.append(
            "Your resume has good textual similarity "
            "with the job description. Review it for accuracy."
        )

    suggestions.append(
        "Keep your resume clear, professional and updated."
    )

    return suggestions


def generate_interview_questions(job_description, difficulty="Beginner"):

    skills = extract_skills(job_description)

    questions = {
        "Python": [
            "What are the main features of Python?",
            "Explain the difference between a list and a tuple.",
            "What are Python functions?"
        ],
        "Machine Learning": [
            "What is Machine Learning?",
            "Explain supervised and unsupervised learning.",
            "What is overfitting?"
        ],
        "SQL": [
            "What is the difference between WHERE and HAVING?",
            "Explain primary keys and foreign keys.",
            "What are SQL joins?"
        ],
        "Java": [
            "What is object-oriented programming?",
            "Explain inheritance in Java.",
            "What is polymorphism?"
        ],
        "Data Analysis": [
            "What is data cleaning?",
            "Why is data visualization important?",
            "What is exploratory data analysis?"
        ]
    }

    selected_questions = []

    for skill in skills:
        for category, category_questions in questions.items():
            if category.lower() == skill.lower():
                selected_questions.extend(category_questions)

    if not selected_questions:
        selected_questions = [
            "Tell me about yourself.",
            "What are your technical strengths?",
            "Why are you interested in this job?",
            "Describe a project you have completed.",
            "How do you approach solving problems?"
        ]

    return selected_questions[:10]

def evaluate_interview_answer(answer, job_description):

    if not answer.strip():
        return 0, ["Please write an answer first."]


    job_skills = extract_skills(job_description)

    answer_clean = clean_text(answer)

    if not job_skills:
        return 0, ["No relevant skills found in the job description."]

    matched_skills = []

    for skill in job_skills:
        if skill.lower() in answer_clean:
            matched_skills.append(skill)

    score = round((len(matched_skills) / len(job_skills)) * 100)

    feedback = []

    if score >= 70:
        feedback.append("Good answer! You included several relevant skills.")
    elif score >= 40:
        feedback.append("Fair answer. Try including more relevant technical skills.")
    else:
        feedback.append("Your answer could be more relevant to the target job.")

    missing = [
        skill for skill in job_skills
        if skill not in matched_skills
    ]

    if missing:
        feedback.append("Consider discussing: " + ", ".join(missing))

    return score, feedback
