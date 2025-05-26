import streamlit as st
import yaml
import csv
import os
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
    st.session_state.interactions = []

quiz_data = load_quiz_data('questions.yaml')

st.title("📝 Quiz Application")

# Quiz display
if not st.session_state.quiz_complete:
    q_idx = st.session_state.current_question
    question_data = quiz_data[q_idx]
    st.subheader(f"Question {q_idx + 1}")
    st.write(question_data['question'])

    selected_option = st.radio("Options", question_data['options'])

    if st.button("Submit Answer"):
        # Log interaction immediately
        timestamp = datetime.now().isoformat()
        correct = selected_option == question_data['answer']
        interaction = {
            'timestamp': timestamp,
            'question': question_data['question'],
            'selected_option': selected_option,
            'correct_answer': question_data['answer'],
            'correctness': correct
        }
        # Append to CSV file
        file_path = 'interaction_log.csv'
        write_header = not os.path.exists(file_path) or os.stat(file_path).st_size == 0
        with open(file_path, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=interaction.keys())
            if write_header:
                writer.writeheader()
            writer.writerow(interaction)

        # Update score and feedback
        if correct:
            st.success("✅ Correct!")
            st.session_state.score += 1
        else:
            st.error(f"❌ Wrong! Correct answer: **{question_data['answer']}**")

        # Next question or finish
        if q_idx + 1 < len(quiz_data):
            st.session_state.current_question += 1
        else:
            st.session_state.quiz_complete = True
            st.balloons()

# Completion view
else:
    st.subheader("Quiz Completed!")
    st.write(f"🎯 Your Score: **{st.session_state.score}/{len(quiz_data)}**")

    if st.button("Restart Quiz"):
        st.session_state.current_question = 0
        st.session_state.score = 0
        st.session_state.quiz_complete = False
