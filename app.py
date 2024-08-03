from flask import Flask, render_template, request
import os
import google.generativeai as genai

app = Flask(__name__)


GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable is not set")

genai.configure(api_key=GEMINI_API_KEY)


generation_config = {
    "temperature": 0.4,
    "top_p": 1,
    "max_output_tokens": 500,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.0-pro",
    generation_config=generation_config,
)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        essay_text = request.form['essay']

        try:
            
            chat_session = model.start_chat(
                history=[
                    {
                        "role": "user",
                        "parts": [
                            "You are an expert essay grader. Please evaluate the following essay based on the criteria provided. Provide a detailed evaluation, including feedback and a score from 1 to 10 for each criterion. Calculate the total score by summing up the individual scores, and provide a final skill level based on the total score.\n\nCriteria:\n1. Grammar: Assess the grammatical correctness of the essay. Look for errors in sentence structure, punctuation, and overall writing mechanics.\n2. Accuracy: Evaluate the accuracy of the information presented in the essay. Ensure that facts are correct and well-supported.\n3. Topic Relevance: Determine how well the essay addresses the given topic. Check if the content is relevant and directly related to the topic.\n4. Creativity: Assess the originality and creativity of the essay. Consider how unique and innovative the ideas presented are.\n5. MLA Format: Check if the essay adheres to MLA formatting guidelines, including in-text citations, works cited page, and overall formatting.\n6. Professionalism: Evaluate the formal tone and overall presentation of the essay. Look for a clear, organized, and well-presented analysis.\n\n**Essay:**\n{essay_text}\n\nProvide feedback for each criterion and include the score in the following format:\n\nGrammar:\nScore: [score]\nFeedback: [detailed feedback]\n\nAccuracy:\nScore: [score]\nFeedback: [detailed feedback]\n\nTopic Relevance:\nScore: [score]\nFeedback: [detailed feedback]\n\nCreativity:\nScore: [score]\nFeedback: [detailed feedback]\n\nMLA Format:\nScore: [score]\nFeedback: [detailed feedback]\n\nProfessionalism:\nScore: [score]\nFeedback: [detailed feedback]\n\n**Overall Score:\nScore: [total_score]\n\nSkill Level:\n- Rookie: Total score below 50\n- Intern: Total score between 50 and 69\n- Pro: Total score 70 and above\n\nPlease provide the feedback and scores in a clear and organized manner. Thank you!\n",
                        ],
                    }
                ]
            )

            response = chat_session.send_message(essay_text)
            feedback = response.text

           
            lines = feedback.splitlines()
            skill_level = ""
            for line in lines:
                if "Skill Level:" in line:
                    skill_level = line.split("Skill Level:")[1].strip()

            
            feedback = "\n".join(line for line in lines if "Skill Level:" not in line)

            return render_template('index.html', feedback=feedback, skill_level=skill_level)

        except Exception as e:
            print(f"An error occurred: {e}")
            return render_template('index.html', error=str(e))
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
