import yaml
import gradio as gr

# Load quiz data from YAML file
def load_quiz(path="quiz_data.yaml"):
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data["questions"]

questions = load_quiz()

# Function to handle each quiz step
def quiz_step(answer, idx, score):
    correct = questions[idx]["answer"]
    # Check answer and update score
    if answer == correct:
        feedback = "✅ Correct!"
        score += 1
    else:
        feedback = f"❌ Wrong! The correct answer was **{correct}**."
    idx += 1
    # If more questions, prepare next
    if idx < len(questions):
        next_q = questions[idx]["question"]
        opts   = questions[idx]["options"]
        return (
            feedback,
            next_q,
            gr.update(choices=opts, value=None),
            idx,
            score,
        )
    # Quiz finished
    else:
        summary = f"### Quiz Complete!\nYour final score: **{score}/{len(questions)}**"
        return (
            feedback,
            summary,
            gr.update(visible=False),
            idx,
            score,
        )

# Build Gradio interface
demo = gr.Blocks()
with demo:
    # Display question text
    q_md = gr.Markdown(questions[0]["question"])
    # Radio buttons for options
    answer = gr.Radio(choices=questions[0]["options"], label="Your Answer")
    submit = gr.Button("Submit")
    feedback = gr.Markdown()
    # States for current index and score
    state_idx   = gr.State(0)
    state_score = gr.State(0)

    # Wire up the button
    submit.click(
        fn=quiz_step,
        inputs=[answer, state_idx, state_score],
        outputs=[feedback, q_md, answer, state_idx, state_score]
    )

# Launch app
if __name__ == "__main__":
    demo.launch()