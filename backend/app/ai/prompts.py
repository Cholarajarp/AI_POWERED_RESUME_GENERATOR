# Prompt templates and versions for AI tasks

PROMPTS = {
    "ats_v1": {
        "description": "ATS scoring: return numeric score, matched and missing keywords, suggested bullets.",
        "system": "You are an expert hiring manager and resume reviewer. Return JSON with 'score', 'matched_keywords', 'missing_keywords', 'suggested_bullets'.",
        "template": "Given job description:\n{job}\nand resume:\n{resume}\nReturn JSON as described."
    },
    "rewrite_v1": {
        "description": "Rewrite resume bullets to match role, concise and achievement-focused.",
        "system": "You are a senior resume writer. Output rewritten resume text with bullets prioritized for the role.",
        "template": "Role: {role}\nResume: {resume}\nReturn rewritten resume content."
    },
    "question_gen_v1": {
        "description": "Generate interview questions for a role and difficulty.",
        "system": "You are an interview coach. Return a list of questions with ids and difficulty.",
        "template": "Role: {role}\nDifficulty: {difficulty}\nReturn JSON list of questions."
    },
    "eval_v1": {
        "description": "Evaluate a candidate's answer against rubric and score.",
        "system": "You are an expert interviewer and provide a numeric score and feedback.",
        "template": "Question: {question}\nAnswer: {answer}\nReturn JSON with 'score' (0-100) and 'feedback'."
    }
}
