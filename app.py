import streamlit as st
 
from resume_parser import (
    extract_text_from_pdf,
    ResumeExtractionError
)
 
MAX_FILE_SIZE_MB = 10
 
from ats_analyzer import (
    calculate_ats_score,
    find_matching_skills,
    detect_job_role,
    get_top_missing_skills,
    extract_job_keywords
)
 
 
# =========================================================
# PAGE SETTINGS
# =========================================================
 
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)
 
 
# =========================================================
# HEADER
# =========================================================
 
st.title(
    "📄 AI Resume Analyzer & ATS Scorer"
)
 
st.write(
    "Analyze your resume against a job "
    "description and identify skills, "
    "keywords and improvement opportunities."
)
 
st.divider()
 
 
# =========================================================
# INPUT SECTION
# =========================================================
 
left, right = st.columns(2)
 
 
with left:
 
    st.subheader(
        "📄 Upload Resume"
    )
 
    uploaded_file = (
        st.file_uploader(
            "Upload your resume (PDF)",
            type=["pdf"]
        )
    )
 
 
with right:
 
    st.subheader(
        "💼 Job Description"
    )
 
    job_description = (
        st.text_area(
            "Paste the job description",
            height=250,
            placeholder=(
                "Paste the complete "
                "job description here..."
            )
        )
    )
 
 
analyze_button = st.button(
    "🔍 Analyze Resume",
    type="primary",
    use_container_width=True
)
 
 
# =========================================================
# ANALYSIS
# =========================================================
 
if analyze_button:
 
    if uploaded_file is None:
 
        st.warning(
            "Please upload your resume."
        )
 
    elif not job_description.strip():
 
        st.warning(
            "Please paste a job description."
        )
 
    elif uploaded_file.size > MAX_FILE_SIZE_MB * 1024 * 1024:
 
        st.error(
            f"This file is larger than the "
            f"{MAX_FILE_SIZE_MB}MB limit. "
            "Please upload a smaller PDF."
        )
 
    else:
 
        extraction_error = None
        resume_text = ""
 
        with st.spinner(
            "Analyzing resume..."
        ):
 
            try:
                resume_text = (
                    extract_text_from_pdf(
                        uploaded_file
                    )
                )
            except ResumeExtractionError as exc:
                extraction_error = str(exc)
 
 
        if extraction_error:
 
            st.error(
                extraction_error
            )
 
        elif not resume_text.strip():
 
            st.error(
                "Unable to extract text from this PDF. "
                "If this is a scanned or image-based resume, "
                "try exporting a text-based PDF instead."
            )
 
        else:
 
            # =============================================
            # RUN ANALYSIS
            # =============================================
 
            scores = calculate_ats_score(
                resume_text,
                job_description
            )
 
            matched_skills, missing_skills = (
                find_matching_skills(
                    resume_text,
                    job_description
                )
            )
 
            detected_role = (
                detect_job_role(
                    job_description
                )
            )
 
            priority_skills = (
                get_top_missing_skills(
                    resume_text,
                    job_description
                )
            )
 
            job_keywords = (
                extract_job_keywords(
                    resume_text,
                    job_description
                )
            )
 
            score = scores[
                "overall"
            ]
 
 
            st.divider()
 
 
            # =============================================
            # JOB ROLE
            # =============================================
 
            st.header(
                "🎯 Detected Job Role"
            )
 
            st.info(
                detected_role
            )
 
 
            # =============================================
            # OVERALL SCORE
            # =============================================
 
            st.header(
                "📊 ATS Match Score"
            )
 
            st.progress(
                min(
                    int(score),
                    100
                )
            )
 
            st.metric(
                "Overall Resume Match",
                f"{score}%"
            )
 
 
            if score >= 80:
 
                st.success(
                    "Excellent match!"
                )
 
            elif score >= 65:
 
                st.success(
                    "Good match!"
                )
 
            elif score >= 50:
 
                st.info(
                    "Moderate match. "
                    "Your resume can be improved "
                    "for this role."
                )
 
            else:
 
                st.warning(
                    "Low match. Your resume "
                    "needs more alignment with "
                    "this job description."
                )
 
 
            # =============================================
            # SCORE BREAKDOWN
            # =============================================
 
            st.header(
                "📈 Score Breakdown"
            )
 
            col1, col2, col3, col4 = (
                st.columns(4)
            )
 
 
            with col1:
 
                st.metric(
                    "Skills Match",
                    f'{scores["skills"]}%'
                )
 
 
            with col2:
 
                st.metric(
                    "Keyword Match",
                    f'{scores["keywords"]}%'
                )
 
 
            with col3:
 
                st.metric(
                    "Text Similarity",
                    f'{scores["similarity"]}%'
                )
 
 
            with col4:
 
                st.metric(
                    "Resume Completeness",
                    f'{scores["completeness"]}%'
                )
 
 
            st.divider()
 
 
            # =============================================
            # PRIORITY MISSING SKILLS
            # =============================================
 
            st.header(
                "🔥 Priority Missing Skills"
            )
 
            if priority_skills:
 
                columns = st.columns(
                    len(priority_skills)
                )
 
                for index, skill in enumerate(
                    priority_skills
                ):
 
                    with columns[index]:
 
                        st.warning(
                            skill.upper()
                        )
 
            else:
 
                st.success(
                    "No major skill gaps detected."
                )
 
 
            # =============================================
            # MATCHED / MISSING SKILLS
            # =============================================
 
            left_skills, right_skills = (
                st.columns(2)
            )
 
 
            with left_skills:
 
                st.header(
                    "✅ Matched Skills"
                )
 
                if matched_skills:
 
                    for skill in matched_skills:
 
                        st.write(
                            f"✅ {skill.upper()}"
                        )
 
                else:
 
                    st.write(
                        "No matched skills detected."
                    )
 
 
            with right_skills:
 
                st.header(
                    "❌ Missing Skills"
                )
 
                if missing_skills:
 
                    for skill in missing_skills:
 
                        st.write(
                            f"❌ {skill.upper()}"
                        )
 
                else:
 
                    st.success(
                        "No missing skills detected."
                    )
 
 
            st.divider()
 
 
            # =============================================
            # JOB KEYWORDS
            # =============================================
 
            st.header(
                "🔑 Important Job Keywords"
            )
 
            if job_keywords:
 
                keyword_text = " • ".join(
                    keyword.upper()
                    for keyword
                    in job_keywords
                )
 
                st.info(
                    keyword_text
                )
 
 
            # =============================================
            # RECOMMENDATIONS
            # =============================================
 
            st.header(
                "💡 Resume Recommendations"
            )
 
 
            if priority_skills:
 
                st.write(
                    "### Skills worth learning "
                    "for this role"
                )
 
                st.caption(
                    "Do not add these skills to "
                    "your resume until you actually "
                    "learn or use them."
                )
 
                for skill in priority_skills:
 
                    st.write(
                        f"• {skill.upper()}"
                    )
 
 
            if scores["keywords"] < 60:
 
                st.write(
                    "• Use relevant terminology "
                    "from the job description when "
                    "it accurately describes your "
                    "skills or projects."
                )
 
 
            if scores["similarity"] < 50:
 
                st.write(
                    "• Improve your project bullet "
                    "points so they demonstrate "
                    "experience relevant to this role."
                )
 
 
            if scores["completeness"] < 100:
 
                st.write(
                    "• Include Profile, Skills, "
                    "Projects, Education and Contact "
                    "sections."
                )
 
 
            if scores["skills"] < 60:
 
                st.write(
                    "• Focus on developing the "
                    "highest-priority technical "
                    "skills required by this role."
                )
 
 
            if score >= 75:
 
                st.write(
                    "• Your resume has strong "
                    "alignment. Add measurable "
                    "achievements to strengthen it "
                    "further."
                )
 
 
            st.divider()
 
 
            st.caption(
                "This application provides an "
                "ATS-style match estimate for "
                "educational and portfolio purposes. "
                "Employer ATS systems may use "
                "different scoring methods."
            )
