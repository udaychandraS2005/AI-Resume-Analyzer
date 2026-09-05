import re
from collections import Counter
 
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
 
 
# =========================================================
# SKILL DATABASE
# =========================================================
 
SKILLS = [
    # Programming
    "python",
    "java",
    "c++",
    "c",
    "javascript",
    "typescript",
    "html",
    "css",
    "go",
    "rust",
 
    # Database
    "sql",
    "mysql",
    "postgresql",
    "mongodb",
 
    # Web Development / Frameworks
    "react",
    "angular",
    "vue.js",
    "node.js",
    "django",
    "flask",
    "spring",
    "rest api",
    "graphql",
 
    # Development Tools / DevOps
    "git",
    "github",
    "docker",
    "kubernetes",
    "ci/cd",
    "jenkins",
 
    # Cloud
    "aws",
    "azure",
    "gcp",
 
    # AI / ML / Data
    "machine learning",
    "deep learning",
    "tensorflow",
    "pytorch",
    "pandas",
    "numpy",
 
    # Data Analysis / BI
    "excel",
    "power bi",
    "tableau",
 
    # Embedded Systems
    "embedded systems",
    "embedded c",
    "iot",
    "arduino",
    "esp32",
    "stm32",
    "freertos",
    "mqtt",
 
    # Communication Protocols
    "uart",
    "spi",
    "i2c",
    "can",
 
    # ECE
    "matlab",
    "verilog",
    "systemverilog",
    "vhdl",
    "fpga",
    "vlsi",
 
    # OS
    "linux"
]
 
 
# =========================================================
# TEXT CLEANING
# =========================================================
 
def clean_text(text):
 
    text = text.lower()
 
    text = re.sub(
        r"[^a-z0-9+#.\s]",
        " ",
        text
    )
 
    text = re.sub(
        r"\s+",
        " ",
        text
    )
 
    return text.strip()
 
 
# =========================================================
# SKILL DETECTION
# =========================================================
 
def skill_exists(skill, text):
 
    text = text.lower()
 
    # Special case for C
    if skill == "c":
 
        return bool(
            re.search(
                r"(?<![\w+#])c(?![\w+#])",
                text
            )
        )
 
    # Special case for C++
    if skill == "c++":
 
        return bool(
            re.search(
                r"(?<!\w)c\+\+(?!\w)",
                text
            )
        )
 
    pattern = (
        r"(?<!\w)"
        + re.escape(skill)
        + r"(?!\w)"
    )
 
    return bool(
        re.search(
            pattern,
            text
        )
    )
 
 
# =========================================================
# MATCHED AND MISSING SKILLS
# =========================================================
 
def find_matching_skills(
    resume_text,
    job_description
):
 
    required_skills = [
        skill
        for skill in SKILLS
        if skill_exists(
            skill,
            job_description
        )
    ]
 
    matched_skills = [
        skill
        for skill in required_skills
        if skill_exists(
            skill,
            resume_text
        )
    ]
 
    missing_skills = [
        skill
        for skill in required_skills
        if not skill_exists(
            skill,
            resume_text
        )
    ]
 
    return (
        matched_skills,
        missing_skills
    )
 
 
# =========================================================
# SKILLS SCORE
# =========================================================
 
def calculate_skill_score(
    resume_text,
    job_description
):
 
    matched, missing = find_matching_skills(
        resume_text,
        job_description
    )
 
    total = (
        len(matched)
        + len(missing)
    )
 
    if total == 0:
        return 0
 
    score = (
        len(matched)
        / total
    ) * 100
 
    return round(
        score,
        2
    )
 
 
# =========================================================
# TEXT SIMILARITY
# =========================================================
 
def calculate_similarity_score(
    resume_text,
    job_description
):
 
    resume = clean_text(
        resume_text
    )
 
    job = clean_text(
        job_description
    )
 
    if not resume or not job:
        return 0
 
    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2)
    )
 
    vectors = vectorizer.fit_transform(
        [
            resume,
            job
        ]
    )
 
    similarity = cosine_similarity(
        vectors[0:1],
        vectors[1:2]
    )[0][0]
 
    return round(
        float(similarity) * 100,
        2
    )
 
 
# =========================================================
# KEYWORD SCORE
# =========================================================
 
def calculate_keyword_score(
    resume_text,
    job_description
):
 
    resume_words = set(
        clean_text(
            resume_text
        ).split()
    )
 
    job_words = set(
        clean_text(
            job_description
        ).split()
    )
 
    stop_words = {
        "the", "and", "or", "a", "an",
        "to", "of", "in", "for", "with",
        "on", "is", "are", "we", "our",
        "you", "your", "will", "be",
        "as", "at", "by", "from",
        "this", "that"
    }
 
    important_words = {
        word
        for word in job_words
        if (
            word not in stop_words
            and len(word) > 2
        )
    }
 
    if not important_words:
        return 0
 
    matched_words = (
        important_words
        .intersection(
            resume_words
        )
    )
 
    score = (
        len(matched_words)
        / len(important_words)
    ) * 100
 
    return round(
        score,
        2
    )
 
 
# =========================================================
# RESUME COMPLETENESS
# =========================================================
 
def calculate_completeness_score(
    resume_text
):
 
    text = resume_text.lower()
 
    sections = {
 
        "education": [
            "education"
        ],
 
        "skills": [
            "skills",
            "technical skills"
        ],
 
        "projects": [
            "projects",
            "project"
        ],
 
        "profile": [
            "profile",
            "summary",
            "professional summary",
            "objective"
        ],
 
        "contact": [
            "email",
            "phone",
            "linkedin"
        ]
    }
 
    found = 0
 
    for keywords in sections.values():
 
        if any(
            keyword in text
            for keyword in keywords
        ):
 
            found += 1
 
    return round(
        (
            found
            / len(sections)
        ) * 100,
        2
    )
 
 
# =========================================================
# FINAL ATS SCORE
# =========================================================
 
def calculate_ats_score(
    resume_text,
    job_description
):
 
    skill_score = calculate_skill_score(
        resume_text,
        job_description
    )
 
    keyword_score = calculate_keyword_score(
        resume_text,
        job_description
    )
 
    similarity_score = calculate_similarity_score(
        resume_text,
        job_description
    )
 
    completeness_score = calculate_completeness_score(
        resume_text
    )
 
    overall_score = (
        skill_score * 0.40
        + keyword_score * 0.25
        + similarity_score * 0.20
        + completeness_score * 0.15
    )
 
    return {
 
        "overall":
            round(
                overall_score,
                2
            ),
 
        "skills":
            skill_score,
 
        "keywords":
            keyword_score,
 
        "similarity":
            similarity_score,
 
        "completeness":
            completeness_score
    }
 
 
# =========================================================
# JOB ROLE DETECTION
# =========================================================
 
def detect_job_role(
    job_description
):
 
    text = job_description.lower()
 
    roles = {
 
        "Embedded Software Engineer": [
            "embedded",
            "microcontroller",
            "firmware",
            "stm32",
            "esp32",
            "freertos",
            "uart",
            "spi",
            "i2c"
        ],
 
        "Software Developer": [
            "software development",
            "java",
            "python",
            "javascript",
            "backend",
            "frontend",
            "database",
            "api"
        ],
 
        "Machine Learning Engineer": [
            "machine learning",
            "deep learning",
            "tensorflow",
            "pytorch",
            "model training",
            "artificial intelligence"
        ],
 
        "Data Analyst": [
            "data analysis",
            "sql",
            "excel",
            "power bi",
            "tableau",
            "pandas",
            "visualization"
        ],
 
        "IoT Engineer": [
            "iot",
            "internet of things",
            "esp32",
            "arduino",
            "mqtt",
            "sensor",
            "cloud"
        ],
 
        "VLSI / FPGA Engineer": [
            "verilog",
            "systemverilog",
            "vhdl",
            "fpga",
            "vlsi",
            "rtl"
        ]
    }
 
    role_scores = {}
 
    for role, keywords in roles.items():
 
        score = 0
 
        for keyword in keywords:
 
            if keyword in text:
                score += 1
 
        role_scores[role] = score
 
    best_role = max(
        role_scores,
        key=role_scores.get
    )
 
    if role_scores[best_role] == 0:
 
        return (
            "General Technical Role"
        )
 
    return best_role
 
 
# =========================================================
# TOP MISSING SKILLS
# =========================================================
 
def get_top_missing_skills(
    resume_text,
    job_description,
    limit=5
):
 
    _, missing = find_matching_skills(
        resume_text,
        job_description
    )
 
    return missing[:limit]
 
 
# =========================================================
# IMPORTANT JOB KEYWORDS
# =========================================================
 
def extract_job_keywords(
    resume_text,
    job_description,
    limit=10
):
 
    stop_words = {
 
        "the", "and", "for", "with",
        "this", "that", "you", "your",
        "our", "are", "will", "from",
        "have", "has", "job", "role",
        "work", "team", "using",
        "looking", "required",
        "preferred", "skills",
        "experience", "knowledge",
        "develop", "basic"
    }
 
    words = re.findall(
        r"\b[a-zA-Z][a-zA-Z+#.-]{2,}\b",
        job_description.lower()
    )
 
    filtered_words = [
 
        word
 
        for word in words
 
        if word not in stop_words
    ]
 
    frequency = Counter(
        filtered_words
    )
 
    top_keywords = [
 
        word
 
        for word, count
        in frequency.most_common(
            limit
        )
    ]
 
    return top_keywords
