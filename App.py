import streamlit as st

st.set_page_config(page_title="TBP 1.0", page_icon="⏱️", layout="centered")

st.title("TBP 1.0 (Time-Band Profiler)")
st.caption("See it now or carry it later.")

st.write("Answer honestly. This gives a clear read on how sustainable your current pace is.")

# ---------- Inputs ----------
st.subheader("Time")
hours_obligated = st.selectbox(
    "How many hours per week are taken up by work, obligations, or survival tasks?",
    ["Under 30", "30–40", "41–55", "56–70", "70+"],
)

free_time = st.selectbox(
    "Outside of work and obligations, how much free time do you have in a typical week?",
    ["Almost none", "A few hours", "A moderate amount", "Plenty"],
)

st.subheader("Stress")
rushed = st.slider(
    "How often do you feel rushed, even when nothing urgent is happening?",
    1, 5, 3,
    help="1 = Sustainable / 5 = Unsustainable"
)

after_hours_stress = st.slider(
    "How often does stress follow you after the day ends?",
    1, 5, 3,
    help="1 = Never / 5 = Always"
)

burnout = st.selectbox(
    "How close do you feel to burnout right now?",
    ["Not close", "A little close", "Very close", "I’m already there"],
)

st.subheader("Tolerance + Agency")
one_more = st.selectbox(
    "If one more major stressor hit your life right now, what would happen?",
    ["I’d adapt", "I’d struggle", "I’d break", "I’m already breaking"],
)

control = st.selectbox(
    "How much control do you feel you have over your schedule?",
    ["Full control", "Some control", "Very little control", "No control"],
)

say_no = st.selectbox(
    "Can you say no to demands on your time without negative consequences?",
    ["Yes", "Sometimes", "Rarely", "Never"],
)

# ---------- Scoring ----------
def map_choice(choice, mapping):
    return mapping[choice]

score = 0

score += map_choice(hours_obligated, {
    "Under 30": 1, "30–40": 2, "41–55": 3, "56–70": 4, "70+": 5
})

score += map_choice(free_time, {
    "Almost none": 5, "A few hours": 4, "A moderate amount": 2, "Plenty": 1
})

# sliders already 1..5
score += rushed
score += after_hours_stress

score += map_choice(burnout, {
    "Not close": 1, "A little close": 3, "Very close": 4, "I’m already there": 5
})

score += map_choice(one_more, {
    "I’d adapt": 1, "I’d struggle": 3, "I’d break": 4, "I’m already breaking": 5
})

score += map_choice(control, {
    "Full control": 1, "Some control": 3, "Very little control": 4, "No control": 5
})

score += map_choice(say_no, {
    "Yes": 1, "Sometimes": 3, "Rarely": 4, "Never": 5
})

# ---------- Bands ----------
# Total possible: 8 questions mapped to 1..5 -> min 8, max 40
def band_from_score(s):
    if s <= 16:
        return "GREEN", "Sustainable"
    if s <= 24:
        return "YELLOW", "Strained"
    if s <= 32:
        return "RED", "Unsustainable"
    return "BLACK", "Critical"

band, label = band_from_score(score)

st.divider()

if st.button("Get my Time Band"):
    st.subheader(f"Result: {band} — {label}")
    st.write(f"**Score:** {score} / 40")

    if band == "GREEN":
        st.success("Your pace is mostly sustainable. Protect your recovery and keep your boundaries intact.")
    elif band == "YELLOW":
        st.warning("You’re running strained. You can function, but you’re burning more tolerance than you think.")
    elif band == "RED":
        st.error("Your current pace is unsustainable. You’re operating on tolerance, not capacity.")
    else:
        st.error("Critical. Something has to change—rest, load, obligations, support—or the system forces a stop.")

    st.caption("This is descriptive, not judgment. It’s a read on constraint, not your worth.")
