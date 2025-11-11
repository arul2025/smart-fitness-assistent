import streamlit as st
import google.generativeai as genai
import pandas as pd

# ----------------------------
# CONFIGURE GEMINI 1.5 API
# ----------------------------
st.set_page_config(page_title="CoachBot A - Smart Fitness Assistant", page_icon="💪")

st.title("💪 CoachBot A - Smart Fitness Assistant")
st.markdown("#### Personalized AI Coaching for Young Athletes")

# Load Gemini API key (stored securely in Streamlit Secrets)
# Add this in Streamlit Cloud -> Settings -> Secrets -> GCP_API_KEY = "your_api_key_here"
api_key = st.secrets[GCP_API_KEY]
genai.configure(api_key=api_key)

# ----------------------------
# SIDEBAR USER INPUTS
# ----------------------------
with st.sidebar:
    st.header("🏋️‍♂️ Athlete Profile")
    sport = st.selectbox("Select your sport:", ["Football", "Cricket", "Basketball", "Athletics", "Hockey"])
    position = st.text_input("Player position (e.g., striker, bowler, midfielder):")
    injury = st.text_area("Injury history or risk zones:", placeholder="e.g., recovering from knee strain")
    intensity = st.slider("Training intensity level", 1, 10, 5)
    diet = st.selectbox("Diet type:", ["Vegetarian", "Non-Vegetarian", "Vegan"])
    calorie_goal = st.number_input("Calorie goal per day (kcal):", min_value=1500, max_value=4000, value=2500)
    allergies = st.text_input("Allergies (if any):", placeholder="e.g., peanuts, lactose")
    goal = st.text_area("Desired goal:", placeholder="e.g., build stamina, recover from injury, tactical improvement")
    temperature = st.slider("Creativity (Temperature)", 0.1, 1.0, 0.5)

# ----------------------------
# BUILD PROMPT
# ----------------------------
prompt = f"""
You are CoachBot A, an expert AI sports coach for youth athletes.

Generate a detailed personalized fitness plan considering the following profile:

Sport: {sport}
Position: {position}
Injury history: {injury}
Training intensity: {intensity}/10
Diet type: {diet}
Calorie goal: {calorie_goal}
Allergies: {allergies}
Goal: {goal}

Provide a structured response including:
1. Warm-up and cooldown routines
2. Main workout plan (safe for injury)
3. Tactical or skill development advice
4. Nutrition and hydration recommendations
5. Motivation tip for the athlete

Keep the tone encouraging and youth-friendly.
"""

# ----------------------------
# CALL GEMINI 1.5
# ----------------------------
if st.button("Generate My Fitness Plan 🧠"):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt, generation_config={"temperature": temperature})

        st.subheader("🏆 Your Personalized Fitness Plan")
        st.write(response.text)

        # ----------------------------
        # OPTIONAL: Display Summary Table
        # ----------------------------
        st.subheader("📅 Example Weekly Schedule")
        data = {
            "Day": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
            "Focus": [
                "Strength & Flexibility",
                "Cardio & Endurance",
                "Skill Training",
                "Tactical Practice",
                "Recovery + Mobility",
                "Speed Drills",
                "Rest & Nutrition",
            ],
        }
        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True)

    except Exception as e:
        st.error(f"Error: {e}")
        st.info("Make sure your Gemini API key is set in Streamlit Secrets.")
else:
    st.info("Enter your details in the sidebar and click **Generate My Fitness Plan**.")

st.markdown("---")
st.caption("🚀 Powered by Gemini 1.5 · Built with Streamlit")
