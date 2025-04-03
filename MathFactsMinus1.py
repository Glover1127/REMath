import streamlit as st
import random
import time

# Title and introduction
st.title('✨ Math Facts Subtraction Game 🎈')
st.write("Welcome to the Math Facts Subtraction Game! Test your subtraction skills and advance through all 3 levels to win!")

# Initialize session state
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'level' not in st.session_state:
    st.session_state.level = 1
if 'questions' not in st.session_state:
    st.session_state.questions = []
if 'current_question' not in st.session_state:
    st.session_state.current_question = None
if 'completed_levels' not in st.session_state:
    st.session_state.completed_levels = []

# Select level before starting
def reset_level(level):
    st.session_state.score = 0
    st.session_state.level = level
    st.session_state.questions = []
    st.session_state.current_question = None

level_selected = st.selectbox("Select the level you want to start with:", list(range(1, 4)), index=st.session_state.level-1)
if st.button('Start Selected Level'):
    reset_level(level_selected)

# Generate subtraction questions based on level
def generate_questions(level):
    questions = []
    max_num = {1: 4, 2: 8, 3: 12}[level]  # Max number for each level: 4, 8, 12
    for a in range(max_num + 1):  # 0 to max_num inclusive
        for b in range(a + 1):  # b <= a to avoid negatives
            questions.append((a, b))
    random.shuffle(questions)
    return questions

# Display new question if needed
if st.session_state.current_question is None or not st.session_state.questions:
    st.session_state.questions = generate_questions(st.session_state.level)
    if st.session_state.questions:
        st.session_state.current_question = st.session_state.questions.pop()
    else:
        st.session_state.current_question = (0, 0)  # Fallback

question = st.session_state.current_question
st.write(f"## What is {question[0]} - {question[1]}?")

# Form for submitting answers using Enter
with st.form(key='answer_form', clear_on_submit=True):
    answer = st.text_input("Enter your answer:", key="math_answer_input")
    submit = st.form_submit_button("Submit Answer")

# Progress bar
progress = st.progress(st.session_state.score / 15)
st.write(f"Current score: {st.session_state.score}")

# Check the answer
def check_answer(answer, question):
    correct = question[0] - question[1]
    if int(answer) == correct:
        st.session_state.score += 1
        st.success('Correct! 🎉')
        if st.session_state.score >= 15:
            if st.session_state.level not in st.session_state.completed_levels:
                st.session_state.completed_levels.append(st.session_state.level)
            st.success(f"You've advanced to the next level! 🎆 Level {st.session_state.level + 1}, here you come! 🎈")
            st.balloons()
            time.sleep(2)
            reset_level(min(st.session_state.level + 1, 3))  # Cap at 3 levels
            st.balloons()
            time.sleep(2)
    else:
        st.session_state.score -= 1
        hints = [
            "Keep trying, you'll get the next one!",
            "Almost there, think carefully!",
            "Oops, try counting backwards!",
            "Stay positive, you can do it!",
            "Nice effort, give it another shot!"
        ]
        st.warning(random.choice(hints))
        if st.session_state.score < 0:
            st.error('Score reached -1. Restarting this level.')
            reset_level(st.session_state.level)

    st.session_state.current_question = None

# Handle submission and auto-focus
if submit:
    if answer.strip().isdigit():
        check_answer(answer, question)
        if st.session_state.score < 15 or st.session_state.level == 3:
            st.components.v1.html(
                """
                <script>
                    setTimeout(() => {
                        const input = document.querySelector('input[name="math_answer_input"]');
                        if (input) {
                            input.focus();
                            console.log("Focused on input");
                        } else {
                            console.log("Input not found");
                        }
                    }, 200);
                </script>
                """,
                height=0
            )
            st.rerun()
    else:
        st.error("Please enter a valid number.")

# Display completed levels with balloons
if st.session_state.completed_levels:
    st.write("### Completed Levels 🎈")
    balloon_display = ""
    for lvl in range(1, 4):  # Only 3 levels now
        if lvl in st.session_state.completed_levels:
            balloon_display += f"Level {lvl}: 🎈  "
        else:
            balloon_display += f"Level {lvl}: -  "
    st.write(balloon_display)

# Congratulatory message on final completion
if st.session_state.level == 3 and st.session_state.score >= 15:
    st.success("Congratulations! You've completed all levels! 🎆🎈✨")
    st.balloons()
    time.sleep(2)
    st.write("Thank you for playing the Math Facts Subtraction Game!")