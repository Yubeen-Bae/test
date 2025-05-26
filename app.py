import streamlit as st
import yaml

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

quiz_data = load_quiz_data('questions.yaml')

st.title("📝 Quiz Application")

if not st.session_state.quiz_complete:
    question_data = quiz_data[st.session_state.current_question]
    st.subheader(f"Question {st.session_state.current_question + 1}")
    st.write(question_data['question'])

    selected_option = st.radio("Options", question_data['options'])

    if st.button("Submit Answer"):
        if selected_option == question_data['answer']:
            st.success("✅ Correct!")
            st.session_state.score += 1
        else:
            st.error(f"❌ Wrong! Correct answer: **{question_data['answer']}**")

        if st.session_state.current_question + 1 < len(quiz_data):
            st.session_state.current_question += 1
        else:
            st.session_state.quiz_complete = True
            st.balloons()

else:
    st.subheader("Quiz Completed!")
    st.write(f"🎯 Your Score: **{st.session_state.score}/{len(quiz_data)}**")

    if st.button("Restart Quiz"):
        st.session_state.current_question = 0
        st.session_state.score = 0
        st.session_state.quiz_complete = False
