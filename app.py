import streamlit as st
import yaml
import csv
import io
from datetime import datetime

# Load quiz data from YAML file
def load_quiz_data(file_path):
    with open(file_path, 'r') as file:
        quiz_data = yaml.safe_load(file)
    return quiz_data['quiz']

# Initialize quiz session state
if 'current_question' not in st.session_state:
    st.session_state.current_question = 0
    st.session_state.score = 0
    st.session_state.quiz_complete = False
    st.session_state.interactions = []  # Initialize interaction log

quiz_data = load_quiz_data('questions.yaml')

st.title("📝 Quiz Application")

# Display quiz
if not st.session_state.quiz_complete:
    q_idx = st.session_state.current_question
    question_data = quiz_data[q_idx]
    st.subheader(f"Question {q_idx + 1}")
    st.write(question_data['question'])

    selected_option = st.radio("Options", question_data['options'])

    if st.button("Submit Answer"):
        # Record interaction
        timestamp = datetime.now().isoformat()
        correct = selected_option == question_data['answer']
        st.session_state.interactions.append({
            'timestamp': timestamp,
            'question': question_data['question'],
            'selected_option': selected_option,
            'correct_answer': question_data['answer'],
            'correctness': correct
        })

        # Provide feedback
        if correct:
            st.success("✅ Correct!")
            st.session_state.score += 1
        else:
            st.error(f"❌ Wrong! Correct answer: **{question_data['answer']}**")

        # Move to next question or complete
        if q_idx + 1 < len(quiz_data):
            st.session_state.current_question += 1
        else:
            st.session_state.quiz_complete = True
            st.balloons()

# Quiz complete view
else:
    st.subheader("Quiz Completed!")
    st.write(f"🎯 Your Score: **{st.session_state.score}/{len(quiz_data)}**")

    # Download interaction log as CSV
    if st.session_state.interactions:
        csv_buffer = io.StringIO()
        writer = csv.DictWriter(csv_buffer, fieldnames=[
            'timestamp', 'question', 'selected_option', 'correct_answer', 'correctness'
        ])
        writer.writeheader()
        writer.writerows(st.session_state.interactions)
        st.download_button(
            label="Download Interaction Log",
            data=csv_buffer.getvalue(),
            file_name='interaction_log.csv',
            mime='text/csv'
        )

    # Restart quiz
    if st.button("Restart Quiz"):
        st.session_state.current_question = 0
        st.session_state.score = 0
        st.session_state.quiz_complete = False
        st.session_state.interactions = []  # Reset interaction log
