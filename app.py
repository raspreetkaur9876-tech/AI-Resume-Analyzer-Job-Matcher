
import streamlit as st
import plotly.graph_objects as go

from resume_analyzer import (
    extract_resume_text,
    calculate_match,
    extract_skills,
    find_missing_skills,
    generate_suggestions,
    generate_interview_questions,
    evaluate_interview_answer
)

# ---------------- PAGE CONFIGURATION ----------------

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0f172a, #172554);
    color: #f8fafc;
}

.main-title {
    font-size: 38px;
    font-weight: 800;
    color: #60a5fa;
    text-align: center;
    padding: 15px;
}

.subtitle {
    text-align: center;
    color: #cbd5e1;
    font-size: 17px;
    margin-bottom: 25px;
}

.stButton > button {
    background: linear-gradient(90deg, #2563eb, #7c3aed);
    color: white;
    border: none;
    border-radius: 10px;
    padding: 12px;
    font-weight: bold;
    width: 100%;
}

.stButton > button:hover {
    background: #1d4ed8;
    color: white;
    border: 1px solid #60a5fa;
}

[data-testid="stMetric"] {
    background: #1e293b;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #334155;
}

[data-testid="stSidebar"] {
    background-color: #111827;
}

h1, h2, h3 {
    color: #93c5fd !important;
}

.stTextArea textarea {
    background-color: #1e293b;
    color: white;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------

st.markdown(
    '<div class="main-title">📄 AI Resume Analyzer & Job Matcher</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Analyze your resume, identify skill gaps, and improve your job match.</div>',
    unsafe_allow_html=True
)

# ---------------- SIDEBAR ----------------

with st.sidebar:
    st.title("⚙️ Dashboard")
    st.write("### Resume Analyzer")
    st.info(
        "Upload your resume and enter a job description "
        "to analyze your skills and text similarity."
    )

    st.markdown("---")
    st.write("**Features**")
    st.write("📄 Resume PDF Upload")
    st.write("📊 Job Match Score")
    st.write("💡 Skill Gap Analysis")
    st.write("🎯 Improvement Suggestions")
    st.write("📥 Download Report")

    st.markdown("---")
    st.caption("Built with Python and Streamlit")

# ---------------- INPUT SECTION ----------------

st.subheader("📂 Upload Your Resume")

uploaded_file = st.file_uploader(
    "Choose your resume (PDF format)",
    type=["pdf"]
)

st.subheader("💼 Job Description")

job_description = st.text_area(
    "Paste the job description here:",
    height=220,
    placeholder="Paste the complete job description here..."
)

# ---------------- ANALYSIS FUNCTIONALITY ----------------

if st.button("🚀 Analyze Resume", use_container_width=True):

    if uploaded_file is None:
        st.warning("Please upload your resume PDF first.")

    elif not job_description.strip():
        st.warning("Please enter a job description.")

    else:
        try:
            with st.spinner("Analyzing your resume..."):

                # Extract resume text
                resume_text = extract_resume_text(uploaded_file)

                if not resume_text.strip():
                    st.error(
                        "No readable text found in the PDF. "
                        "Please upload a text-based PDF."
                    )
                    st.stop()

                # Calculate match score
                match_score = calculate_match(
                    resume_text,
                    job_description
                )

                # Extract skills
                resume_skills, job_skills, missing_skills = find_missing_skills(
                    resume_text,
                    job_description
                )

                # Generate suggestions
                suggestions = generate_suggestions(
                    missing_skills,
                    match_score
                )

            # ---------------- RESULTS ----------------

            st.markdown("---")
            st.header("📊 Resume Analysis Results")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "Resume Match Score",
                    f"{match_score:.1f}%"
                )

            with col2:
                st.metric(
                    "Skills Found",
                    len(resume_skills)
                )

            with col3:
                st.metric(
                    "Missing Skills",
                    len(missing_skills)
                )

            # ---------------- MATCH GAUGE ----------------

            st.subheader("🎯 Job Match Visualization")

            fig = go.Figure(
                go.Indicator(
                    mode="gauge+number",
                    value=match_score,
                    title={"text": "Resume Match Percentage"},
                    number={"suffix": "%"},
                    gauge={
                        "axis": {"range": [0, 100]},
                        "bar": {"color": "#3b82f6"},
                        "steps": [
                            {
                                "range": [0, 40],
                                "color": "#7f1d1d"
                            },
                            {
                                "range": [40, 70],
                                "color": "#854d0e"
                            },
                            {
                                "range": [70, 100],
                                "color": "#166534"
                            }
                        ]
                    }
                )
            )

            fig.update_layout(
                height=300,
                paper_bgcolor="#0f172a",
                font={"color": "white"}
            )

            st.plotly_chart(fig, use_container_width=True)

            # ---------------- SKILLS ANALYSIS ----------------

            st.markdown("---")
            st.header("🧠 Skills Analysis")

            skill_col1, skill_col2 = st.columns(2)

            with skill_col1:
                st.subheader("✅ Skills Found in Resume")

                if resume_skills:
                    for skill in resume_skills:
                        st.success(skill)
                else:
                    st.info("No matching skills detected.")

            with skill_col2:
                st.subheader("❌ Missing Job Skills")

                if missing_skills:
                    for skill in missing_skills:
                        st.error(skill)
                else:
                    st.success("No missing skills detected!")

            # ---------------- SUGGESTIONS ----------------

            st.markdown("---")
            st.header("💡 Improvement Suggestions")

            if suggestions:
                for suggestion in suggestions:
                    st.info(suggestion)
            else:
                st.success("Your resume looks well matched!")

            # ---------------- TEXT REPORT ----------------

            st.markdown("---")
            st.header("📥 Download Analysis Report")

            report = f"""
AI RESUME ANALYZER & JOB MATCHER
================================

RESUME MATCH SCORE: {match_score:.1f}%

SKILLS FOUND IN RESUME:
{', '.join(resume_skills) if resume_skills else 'None'}

SKILLS REQUIRED BY JOB:
{', '.join(job_skills) if job_skills else 'None'}

MISSING SKILLS:
{', '.join(missing_skills) if missing_skills else 'None'}

IMPROVEMENT SUGGESTIONS:
{chr(10).join(suggestions) if suggestions else 'No suggestions.'}

================================
Note:
The match score measures text similarity using TF-IDF
and cosine similarity. It is not an actual ATS score
or a prediction of hiring success.
"""

            st.download_button(
                label="⬇️ Download Report",
                data=report,
                file_name="resume_analysis_report.txt",
                mime="text/plain",
                use_container_width=True
            )

            st.success("Resume analysis completed successfully!")

        except Exception as e:
            st.error(f"An error occurred: {e}")

# ---------------- FOOTER ----------------


# ---------------- INTERVIEW QUESTION GENERATOR ----------------

st.markdown("---")

st.header("🎯 AI Interview Preparation")

st.write(
    "Generate interview practice questions based on your target job description."
)

difficulty = st.selectbox(
    "Select Interview Difficulty",
    ["Beginner", "Intermediate", "Advanced"]
)

if st.button("Generate Interview Questions"):

    if not job_description.strip():

        st.warning(
            "Please enter a job description above first."
        )

    else:

        questions = generate_interview_questions(
            job_description,
            difficulty
        )

        st.success("Interview questions generated!")

        for index, question in enumerate(questions, start=1):

            with st.expander(f"Question {index}"):

                st.write(question)

                st.text_area(
                    "Write your answer:",
                    key=f"interview_answer_{index}"
                )

st.caption(
    "Practice these questions to prepare for your next interview."
)


# ---------------- ANSWER EVALUATION ----------------

st.markdown("---")

st.header("📝 Interview Answer Evaluator")

st.write(
    "Practice your interview answers and receive "
    "instant keyword-based feedback."
)

interview_question = st.text_input(
    "Enter your interview question:",
    placeholder="Example: What is Python?"
)

interview_answer = st.text_area(
    "Write your interview answer:",
    height=150,
    placeholder="Type your answer here..."
)

if st.button("📊 Evaluate My Answer"):

    if not job_description.strip():
        st.warning("Please enter a job description above.")

    elif not interview_answer.strip():
        st.warning("Please enter your answer.")

    else:
        score, feedback = evaluate_interview_answer(
            interview_answer,
            job_description
        )

        st.subheader("Your Evaluation Results")

        st.metric("Keyword Match Score", f"{score}%")

        st.progress(score / 100)

        for item in feedback:
            st.info(item)

        st.caption(
            "This score measures keyword coverage, "
            "not actual interview answer quality."
        )
