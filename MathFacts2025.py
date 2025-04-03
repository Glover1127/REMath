import streamlit as st
import random
import time

# --- CONFIGURE PAGE ---
st.set_page_config(page_title="Math Facts Game", page_icon="🧮", layout="centered")

# --- GAME VARIABLES ---
LEVELS = {i: [(i, x) for x in range(13)] for i in range(13)}
LEVELS[13] = [(a, b) for a in range(13) for b in range(13)]  # Level 14 (all numbers)
TIME_LIMIT = 7  # 7 seconds per question
POINTS_TO_LEVEL_UP = 15

# --- ENCOURAGING MESSAGES ---
ENCOURAGING_MESSAGES = [
    "Almost! Try again!", "You'll get it next time!", "Keep going!", "Nice effort!", "Think about it carefully!"
]

# --- CUSTOM THEMES ---
THEMES = {
    "Space": "🌌", "Jungle": "🌿", "Ocean": "🌊", "Robots": "🤖", "Classic": "🎲"
}

# --- CUSTOM AVATARS ---
AVATARS = {
    "Monkey": "🐵", "Robot": "🤖", "Astronaut": "🚀", "Shark": "🦈", "Wizard": "🧙"
}

# --- SESSION STATE INITIALIZATION ---
if "level" not in st.session_state:
    st.session_state.level = 1
    st.session_state.score = 0
    st.session_state.problem = None
    st.session_state.start_time = None
    st.session_state.theme = None
    st.session_state.avatar = None

# --- THEME & AVATAR SELECTION BEFORE GAME START ---
if st.session_state.theme is None or st.session_state.avatar is None:
    st.title("🎮 Welcome to the Math Facts Game!")
    st.subheader("Pick your theme and avatar before you begin:")

    theme_choice = st.radio("Select a theme:", list(THEMES.keys()), horizontal=True)
    avatar_choice = st.radio("Choose your avatar:", list(AVATARS.keys()), horizontal=True)

    if st.button("Start Game! 🚀"):
        st.session_state.theme = theme_choice
        st.session_state.avatar = avatar_choice
        st.experimental_rerun()

# --- DISPLAY SELECTED THEME & AVATAR ---
st.sidebar.header(f"Your Theme: {THEMES[st.session_state.theme]}")
st.sidebar.header(f"Your Avatar: {AVATARS[st.session_state.avatar]}")

# --- GENERATE RANDOM PROBLEM ---
if st.session_state.problem is None or time.time() - st.session_state.start_time > TIME_LIMIT:
    st.session_state.problem = random.choice(LEVELS[st.session_state.level])
    st.session_state.start_time = time.time()

# --- MATH PROBLEM ---
num1, num2 = st.session_state.problem
correct_answer = num1 + num2

st.title(f"📚 Level {st.session_state.level}")
st.subheader(f"{num1} + {num2} = ?")
st.write(f"⏳ You have {TIME_LIMIT} seconds!")

# --- USER INPUT ---
user_answer = st.text_input("Enter your answer:", key="answer", max_chars=2)
st.markdown(f"Press **Enter** to submit!")

# --- CHECK ANSWER ---
if user_answer:
    try:
        user_answer = int(user_answer)
        if user_answer == correct_answer:
            st.session_state.score += 1
            st.success(f"✅ Correct! {num1} + {num2} = {correct_answer}")
        else:
            st.session_state.score -= 1
            st.warning(f"❌ Incorrect. {random.choice(ENCOURAGING_MESSAGES)}")

        # --- CHECK GAME STATUS ---
        if st.session_state.score == POINTS_TO_LEVEL_UP:
            st.session_state.level += 1
            st.session_state.score = 0
            st.session_state.problem = None
            st.success(f"🎉 Level Up! Welcome to Level {st.session_state.level}!")

        elif st.session_state.score < 0:
            st.session_state.score = 0
            st.warning("🔁 You dropped below zero! Restarting this level...")
            time.sleep(1)  # Pause before restarting

        st.session_state.problem = None  # Generate new problem
        st.experimental_rerun()

    except ValueError:
        st.warning("⚠️ Please enter a valid number!")

# --- PROGRESS BAR ---
progress = st.session_state.score / POINTS_TO_LEVEL_UP
st.progress(progress)

# --- WIN SCREEN ---
if st.session_state.level > 13:
    st.balloons()
    st.success("🎊 Congratulations! You mastered all math facts! 🎊")
    if st.button("Play Again?"):
        st.session_state.level = 1
        st.session_state.score = 0
        st.session_state.problem = None
        st.session_state.theme = None
        st.session_state.avatar = None
        st.experimental_rerun()
