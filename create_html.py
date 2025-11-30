import json


def create_html(mcqs, output_file="quiz.html"):
    """
    Generates an interactive HTML quiz file from a list of MCQ dictionaries.

    Args:
        mcqs (list): A list of dictionaries, where each dictionary
                     has 'question', 'options' (list), and 'correct' (str/char).
        output_file (str): The name of the HTML file to create.
    """
    # 1. Error handling for empty or erroneous input
    if not mcqs or ("error" in mcqs[0] if isinstance(mcqs[0], dict) else False):
        html = "<html><body><h1>Error: No MCQs generated or an error occurred.</h1></body></html>"
    else:
        # Start of the HTML structure
        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>AI Quiz</title>
    <style>
        body {{
            font-family: 'Segoe UI', sans-serif;
            padding: 20px;
            background: linear-gradient(135deg, #e3ecff, #f5f7fa);
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            flex-direction: column;
            animation: fadeIn 1s ease-in-out;
        }}
        @keyframes fadeIn {{
            from {{ opacity: 0; }}
            to {{ opacity: 1; }}
        }}
        h1 {{
            text-align: center;
            color: #2a2a72;
            margin-bottom: 20px;
        }}
        .quiz-container {{
            width: 100%;
            max-width: 600px;
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 6px 20px rgba(0,0,0,0.15);
            animation: fadeUp 0.8s ease forwards;
        }}
        @keyframes fadeUp {{
            from {{ transform: translateY(20px); opacity: 0; }}
            to {{ transform: translateY(0); opacity: 1; }}
        }}
        .question-box {{
            display: none;
            margin-bottom: 20px;
        }}
        .question-box.active {{
            display: block;
        }}
        label {{
            display: block;
            padding: 12px;
            border-radius: 10px;
            margin: 8px 0;
            cursor: pointer;
            background: #eef1f7;
            transition: 0.3s;
        }}
        label:hover {{
            background: #d9e1ff;
        }}
        .correct {{
            background-color: #b7ffb7 !important;
        }}
        .incorrect {{
            background-color: #ffb7b7 !important;
        }}
        button {{
            display: block;
            width: 100%;
            padding: 15px;
            font-size: 18px;
            border: none;
            background: #2a2a72;
            color: white;
            border-radius: 10px;
            cursor: pointer;
            margin-top: 20px;
            transition: 0.3s;
        }}
        button:hover {{
            background: #1e1e5a;
            transform: scale(1.02);
        }}
        .progress-bar {{
            height: 15px;
            background: #eef1f7;
            border-radius: 10px;
            margin-bottom: 20px;
            overflow: hidden;
        }}
        .progress-bar-fill {{
            height: 100%;
            width: 0%;
            background: #2a2a72;
            transition: width 0.5s ease;
        }}
        footer {{
            text-align: center;
            margin-top: 30px;
            padding: 20px;
            color: #333;
            font-size: 14px;
        }}
        @media(max-width: 600px){{
            .quiz-container {{
                padding: 20px;
            }}
            label {{
                padding: 10px;
            }}
            button {{
                padding: 12px;
            }}
        }}
    </style>
</head>
<body>

<h1>AI Quiz</h1>
<div class="quiz-container">
    <div class="progress-bar"><div class="progress-bar-fill"></div></div>
    <form id="quizForm">
"""

        # 2. Correctly iterate and generate HTML for each question
        for i, mcq in enumerate(mcqs):
            options_html = "".join(
                [
                    f'<label><input type="radio" name="q{i}" value="{chr(65+j)}"> {opt}</label>'
                    for j, opt in enumerate(mcq["options"])
                ]
            )

            html += f"""
        <div class="question-box" id="q{i}">
            <p><strong>Question {i+1}:</strong> {mcq['question']}</p>
            {options_html}
            <button type="button" onclick="nextQuestion({i})">{'Next' if i < len(mcqs)-1 else 'Submit'}</button>
        </div>
"""

        # End of the HTML form and start of JavaScript
        html += (
            """
    </form>
</div>

 <script>
const mcqs = """
            + json.dumps(mcqs)
            + """;

let current = 0;
let answers = new Array(mcqs.length).fill(null); 
let score = 0;
const total = mcqs.length;

document.getElementById('q0').classList.add('active');
updateProgress(current);

function nextQuestion(i) {
    const selected = document.querySelector(`input[name="q${i}"]:checked`);

    if (!selected) {
        alert("Please select an option!");
        return;
    }

    answers[i] = selected.value;

    // Move to next question
    if (i < total - 1) {
        document.getElementById(`q${i}`).classList.remove('active');
        document.getElementById(`q${i+1}`).classList.add('active');
        current++;
        updateProgress(current);
    } else {
        showResult();
    }
}

function updateProgress(index) {
    const fill = document.querySelector('.progress-bar-fill');
    fill.style.width = ((index + 1) / total * 100) + '%';
}

function showResult() {

    mcqs.forEach((q, i) => {
        if (answers[i] === q.correct) score++;
    });

    let reportHTML = `
        <h2 style="text-align:center; color:#2a2a72;">Quiz Complete!</h2>
        <h3 style="text-align:center; color:#2a2a72;">Your Score: ${score} / ${total}</h3>
        <hr><h3>Detailed Report</h3>
    `;

    mcqs.forEach((q, i) => {
        reportHTML += `
            <div style="margin-bottom:20px; padding:15px; border-radius:10px; background:#f3f4ff">
                <p><b>Q${i+1}: ${q.question}</b></p>
                <p>Your Answer: <b>${answers[i] || "Not answered"}</b></p>
                <p>Correct Answer: <b style="color:green">${q.correct}</b></p>
            </div>
        `;
    });

    reportHTML += `
        <button onclick="goHome()" style="
            display:block;width:100%;padding:15px;background:#2a2a72;color:white;
            border:none;border-radius:10px;font-size:18px;cursor:pointer;">
            Return Home
        </button>
    `;

    const container = document.querySelector('.quiz-container');
    container.innerHTML = reportHTML;
}

function goHome() {
    window.location.href = "/";
}
</script>


<footer>
Created by <b>Ahmad Raza Khan</b> • AI Quiz Generator © 2025
</footer>

</body>
</html>
"""
        )

    # 4. Correct file writing
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Quiz HTML created: {output_file}")
