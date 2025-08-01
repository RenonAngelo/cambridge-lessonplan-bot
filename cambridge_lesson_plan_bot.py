# Chatbot Version of Cambridge Lesson Plan Generator
import openai
import streamlit as st

st.set_page_config(page_title="Cambridge Lesson Plan Chatbot", layout="wide")

st.title("🤖 Cambridge Lesson Plan Chatbot")
st.markdown("Welcome to the **Cambridge Lesson Plan Generator Chatbot** for Vinschool Times City. Ask the bot to generate a lesson plan for any Cambridge subject by entering the details below.")

# Chat Interface
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.chat_message("assistant").markdown("Hello! 👋 I can help you generate detailed Cambridge lesson plans. Please enter your subject, grade, duration, topic, and learning objectives.")

user_input = st.chat_input("Type your message here...")

def extract_details(message):
    # A simple mock parser to extract key info (could be replaced with a proper NLP tool)
    return {
        "subject": st.session_state.get("subject"),
        "grade_level": st.session_state.get("grade_level"),
        "duration": st.session_state.get("duration"),
        "topic": st.session_state.get("topic"),
        "learning_objectives": st.session_state.get("learning_objectives")
    }

def generate_lesson_plan(subject, grade_level, duration, topic, learning_objectives):
    prompt = f'''
You are a Cambridge curriculum lesson planning assistant. Based on the following inputs, generate a full lesson plan suitable for the subject and grade level. Include the following components:

WALT (We Are Learning To...)
WILF (What I'm Looking For...)
Introduction / Warm-Up (10 min)
Main Activity (25 min)
Supported Practice (15 min)
Individual Practice (10 min)
Differentiation
D.I.R.T (5 min)
Assessment (10 min)
Key Terms / Vocabulary
Digital Device Utilization (10 min)
HOMEWORK
Student / Lesson Observation Notes
Intervention

Input:
Subject: {subject}
Grade/Year Level: {grade_level}
Lesson Duration: {duration}
Lesson Topic: {topic}
Learning Objectives: {learning_objectives}

Generate the lesson plan with clear and concise formatting.
'''

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an expert Cambridge curriculum lesson planner."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=2000
    )

    return response['choices'][0]['message']['content']

if user_input:
    st.chat_message("user").markdown(user_input)
    st.session_state.chat_history.append(("user", user_input))

    if "generate" in user_input.lower():
        with st.chat_message("assistant"):
            subject = st.text_input("Subject", key="subject")
            grade_level = st.text_input("Grade/Year Level", key="grade_level")
            duration = st.text_input("Lesson Duration", key="duration")
            topic = st.text_input("Lesson Topic", key="topic")
            learning_objectives = st.text_area("Learning Objectives", key="learning_objectives")

            submit = st.button("Generate Lesson Plan")

            if submit:
                if all([subject, grade_level, duration, topic, learning_objectives]):
                    with st.spinner("Generating lesson plan..."):
                        result = generate_lesson_plan(subject, grade_level, duration, topic, learning_objectives)
                        st.markdown("### 📄 Generated Lesson Plan")
                        st.code(result)
                else:
                    st.warning("🚨 Please complete all fields.")
    else:
        with st.chat_message("assistant"):
            st.markdown("Please type **generate** to start creating a lesson plan.")
