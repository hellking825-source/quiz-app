from flask import Flask, render_template, request, redirect, url_for, session
from questions import QUESTIONS

app = Flask(__name__)
app.secret_key = "change-this-to-something-secret"  # needed for session to work


@app.route("/")
def index():
    return render_template("index.html", total_questions=len(QUESTIONS))


@app.route("/start")
def start():
    # reset quiz state
    session["current_q"] = 0
    session["score"] = 0
    session["answers"] = []
    return redirect(url_for("quiz"))


@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    if "current_q" not in session:
        return redirect(url_for("index"))

    current_q = session["current_q"]

    if request.method == "POST":
        selected = request.form.get("option")
        correct_answer = QUESTIONS[current_q]["answer"]

        if selected == correct_answer:
            session["score"] += 1

        session["answers"].append(
            {
                "question": QUESTIONS[current_q]["question"],
                "selected": selected,
                "correct_answer": correct_answer,
                "is_correct": selected == correct_answer,
            }
        )

        session["current_q"] += 1
        session.modified = True

        if session["current_q"] >= len(QUESTIONS):
            return redirect(url_for("result"))

        return redirect(url_for("quiz"))

    # GET request: show current question
    if current_q >= len(QUESTIONS):
        return redirect(url_for("result"))

    question_data = QUESTIONS[current_q]
    return render_template(
        "quiz.html",
        question=question_data,
        q_number=current_q + 1,
        total_questions=len(QUESTIONS),
    )


@app.route("/result")
def result():
    if "score" not in session:
        return redirect(url_for("index"))

    score = session["score"]
    total = len(QUESTIONS)
    answers = session.get("answers", [])

    return render_template(
        "result.html", score=score, total=total, answers=answers
    )


if __name__ == "__main__":
    app.run(debug=True)
