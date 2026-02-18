import streamlit as st
import random
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ==========================================
# 1. APP CONFIGURATION
# ==========================================
st.set_page_config(page_title="Airport Screening Simulation", layout="centered")

# ==========================================
# 2. SESSION STATE
# ==========================================
if 'score' not in st.session_state: st.session_state.score = 0
if 'rounds' not in st.session_state: st.session_state.rounds = 0
if 'history' not in st.session_state: st.session_state.history = []
if 'simulation_active' not in st.session_state: st.session_state.simulation_active = False
if 'mode' not in st.session_state: st.session_state.mode = "Manual"
if 'verification_result' not in st.session_state: st.session_state.verification_result = None

# ==========================================
# 3. ASSETS
# ==========================================
SAFE_ITEMS = ['👕','👖','👗','👟','🎩','💻','📷','📚','🧸','🥪','🕶️']
THREAT_ITEMS = ['🔫','🔪','💣','🧨','🩸','☠️']

# ==========================================
# 4. CORE FUNCTIONS
# ==========================================

def generate_bag():
    items = random.sample(SAFE_ITEMS, k=random.randint(4, 8))
    threat = False
    if random.random() < 0.50:
        items.append(random.choice(THREAT_ITEMS))
        threat = True
    random.shuffle(items)
    return items, threat


def simulated_officer_decision(mode, has_threat):
    """
    Contained simulated decision agent.
    Manual mode: 70% accuracy.
    AI-Assisted mode: 85% black-box reliability.
    """
    if mode == "Manual":
        if random.random() < 0.70:
            return has_threat
        else:
            return not has_threat

    elif mode == "AI_Assist":
        ai_prediction = has_threat
        if random.random() > 0.85:
            ai_prediction = not ai_prediction
        return ai_prediction


def run_simulation(mode):
    history = []
    score = 0

    for round_num in range(1, 11):
        bag, has_threat = generate_bag()

        decision = simulated_officer_decision(mode, has_threat)

        # Synthetic reaction time (no human involved)
        reaction_time = round(random.uniform(0.4, 2.5), 3)

        correct = (decision == has_threat)
        if correct:
            score += 10

        history.append({
            "Round": round_num,
            "Mode": mode,
            "Threat_Present": has_threat,
            "System_Decision": decision,
            "Correct": correct,
            "Reaction_Time": reaction_time,
            "Bag_Contents": " ".join(bag)
        })

    return pd.DataFrame(history), score


def run_system_verification():
    logs = []
    for i in range(10000):
        is_threat = random.random() < 0.50
        prediction = is_threat
        if random.random() > 0.85:
            prediction = not prediction

        logs.append({
            "Ground_Truth": is_threat,
            "AI_Prediction": prediction,
            "Correct": prediction == is_threat
        })

    return pd.DataFrame(logs)


# ==========================================
# 5. UI
# ==========================================

st.title("Airport Baggage Screening Simulation")
st.markdown("### Contained Black-Box AI Decision-Support Model")

st.info("""
This system simulates airport baggage screening under two configurations:
• Baseline Manual Decision Agent
• AI-Assisted Black-Box Classifier (85% reliability)

All decisions and reaction times are synthetically generated.
No human participant interaction is required.
""")

st.markdown("#### Target Threat Items")
threat_html = " ".join([f"<span style='font-size:40px;'>{x}</span>" for x in THREAT_ITEMS])
st.markdown(f"<div style='text-align:center'>{threat_html}</div>", unsafe_allow_html=True)

st.divider()

col1, col2 = st.columns(2)

with col1:
    if st.button("Run Baseline Simulation"):
        df, score = run_simulation("Manual")
        st.session_state.histo_
