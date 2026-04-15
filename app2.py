import streamlit as st
from datetime import datetime

st.set_page_config(page_title="CareNova", page_icon="🛡️", layout="wide")

# --- INIT SESSION STATE ---
if "users" not in st.session_state:
    st.session_state.users = {}
if "current_user" not in st.session_state:
    st.session_state.current_user = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = {}

# --- CSS ---
st.markdown("""
<style>
.title {text-align:center; font-size:42px; color:#5c2d38; font-weight:bold; font-family:'Times New Roman', serif;}
.subtitle {text-align:center; color:#6b4d58; margin-bottom:20px;}
.call-btn a button {
    width:100%; height:80px; font-size:18px; font-weight:bold;
    background-color:#dc2626; color:white; border-radius:12px; border:none; margin:5px 0;
}
.sos-btn > button {
    width:100%; height:100px; font-size:24px; font-weight:bold;
    background-color:#b30000; color:white; border-radius:15px; border:3px solid #7f0000;
}
</style>
""", unsafe_allow_html=True)

# --- LOGIN SCREEN ---
if st.session_state.current_user is None:
    st.markdown('<div class="title">🛡️ CareNova</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Personal Safety & Health Helpline • Hackathon 2026</div>', unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["Login", "Create Account"])

    with tab1:
        user = st.text_input("Username")
        pwd = st.text_input("Password", type="password")
        if st.button("Login", use_container_width=True):
            if user in st.session_state.users and st.session_state.users[user]["pwd"] == pwd:
                st.session_state.current_user = user
                if user not in st.session_state.chat_history:
                    st.session_state.chat_history[user] = []
                st.rerun()
            else:
                st.error("Wrong username or password")

    with tab2:
        new_user = st.text_input("New Username")
        new_pwd = st.text_input("New Password", type="password")
        name = st.text_input("Your Full Name")
        phone = st.text_input("Your Phone Number")
        age = st.number_input("Age", 1, 120, 25)
        bg = st.selectbox("Blood Group", ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-", "Unknown"])
        contact1 = st.text_input("Emergency Contact 1: Name - Number")

        if st.button("Create Account", use_container_width=True):
            if new_user in st.session_state.users:
                st.error("Username taken")
            elif all([new_user, new_pwd, name, phone]):
                st.session_state.users[new_user] = {
                    "pwd": new_pwd,
                    "name": name,
                    "phone": phone,
                    "age": age,
                    "contacts": [contact1] if contact1 else [],
                    "incidents": [],
                    "vitals": {"bp": "120/80", "hr": 72, "sugar": 90, "bg": bg, "weight": 60, "height": 165},
                    "meds": []
                }
                st.session_state.chat_history[new_user] = []
                st.success("Account created! Go to Login tab")
            else:
                st.warning("Fill username, password, name, phone")
    st.stop()

# --- MAIN APP ---
u = st.session_state.users[st.session_state.current_user]

# Header + Logout
h1, h2 = st.columns([4,1])
h1.markdown(f'<div class="title">🛡️ CareNova</div>', unsafe_allow_html=True)
h1.markdown(f'<div class="subtitle">Welcome, {u["name"]}</div>', unsafe_allow_html=True)
if h2.button("Logout"):
    st.session_state.current_user = None
    st.rerun()

menu = st.sidebar.radio("Menu", ["Home", "Health Tracker", "AI Assistant", "Helplines", "My Contacts", "SOS Log", "Dashboard"])

# --- HOME ---
if menu == "Home":
    st.header(f"Hi {u['name']}, you are safe with CareNova")
    st.write("One-tap emergency calling + personal health tracking for you.")

    st.subheader("🚨 Emergency One-Tap Dial")
    st.markdown("**Tap to call immediately on mobile**")
    c1, c2 = st.columns(2)

    with c1:
        st.markdown('<div class="call-btn"><a href="tel:100"><button>🚔 POLICE<br>100</button></a></div>', unsafe_allow_html=True)
        st.markdown('<div class="call-btn"><a href="tel:101"><button>🚒 FIRE<br>101</button></a></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="call-btn"><a href="tel:108"><button>🚑 AMBULANCE<br>108</button></a></div>', unsafe_allow_html=True)
        st.markdown('<div class="call-btn"><a href="tel:1091"><button>👩 WOMEN HELPLINE<br>1091</button></a></div>', unsafe_allow_html=True)

    st.divider()
    st.markdown('<div class="sos-btn">', unsafe_allow_html=True)
    if st.button("🆘 SEND SOS ALERT"):
        timestamp = datetime.now().strftime("%d %b %Y, %I:%M %p")
        u["incidents"].append(f"SOS triggered at {timestamp}")
        st.error(f"SOS SENT for {u['name']} at {timestamp}")
        st.balloons()
        st.info("In real app: SMS sent to your emergency contacts with live location")
    st.markdown('</div>', unsafe_allow_html=True)

# --- HEALTH TRACKER ---
elif menu == "Health Tracker":
    st.header("💊 Your Personal Health Tracker")

    st.subheader("Update Your Vitals")
    col1, col2, col3 = st.columns(3)
    u["vitals"]["bp"] = col1.text_input("Blood Pressure", value=u["vitals"]["bp"])
    u["vitals"]["hr"] = col1.number_input("Heart Rate bpm", 30, 200, value=int(u["vitals"]["hr"]))
    u["vitals"]["sugar"] = col2.number_input("Blood Sugar mg/dL", 50, 500, value=int(u["vitals"]["sugar"]))
    u["vitals"]["weight"] = col2.number_input("Weight kg", 20, 200, value=int(u["vitals"]["weight"]))
    u["vitals"]["height"] = col3.number_input("Height cm", 100, 220, value=int(u["vitals"]["height"]))
    u["vitals"]["bg"] = col3.selectbox("Blood Group", ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-", "Unknown"],
                                       index=["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-", "Unknown"].index(u["vitals"]["bg"]))

    if st.button("Save Vitals", use_container_width=True):
        st.success("Vitals saved to your profile!")
        st.rerun()

    st.divider()
    with st.expander("Add Medicine Reminder"):
        med_name = st.text_input("Medicine Name")
        med_time = st.time_input("Time")
        if st.button("Add Reminder"):
            u["meds"].append(f"{med_name} at {med_time.strftime('%I:%M %p')}")
            st.success(f"{med_name} reminder added")
            st.rerun()

    st.subheader("Your Medicine Reminders")
    if u["meds"]:
        for med in u["meds"]: st.write(f"• {med}")
    else: st.info("No reminders yet")

# --- AI ASSISTANT ---
elif menu == "AI Assistant":
    st.header("🤖 CareNova AI Assistant")
    st.write("Ask me about health, safety, or emergencies. I remember your profile.")

    # Display chat history for current user
    for sender, msg in st.session_state.chat_history[st.session_state.current_user]:
        with st.chat_message("user" if sender == "You" else "assistant"):
            st.write(msg)

    # Chat input
    if prompt := st.chat_input(f"Ask me anything, {u['name']}"):
        st.session_state.chat_history[st.session_state.current_user].append(("You", prompt))
        with st.chat_message("user"):
            st.write(prompt)

        # Simple rule-based AI using user's data
        response = ""
        prompt_lower = prompt.lower()
        if "sos" in prompt_lower or "emergency" in prompt_lower or "help" in prompt_lower:
            response = f"Stay calm, {u['name']}. For immediate danger: 1. Go to Home tab and hit SOS. 2. Or call Police: 100. I’ve logged your last SOS: {u['incidents'][-1] if u['incidents'] else 'None yet'}."
        elif "medicine" in prompt_lower or "med" in prompt_lower:
            med_list = ", ".join(u['meds']) if u['meds'] else "no medicines added"
            response = f"Your current reminders: {med_list}. Add more in Health Tracker. Remember to take them on time!"
        elif "blood pressure" in prompt_lower or "bp" in prompt_lower:
            response = f"Your last recorded BP is {u['vitals']['bp']}. Normal is around 120/80. If you feel dizzy, sit down and call 108 if needed. Update it in Health Tracker."
        elif "heart rate" in prompt_lower:
            response = f"Your heart rate is {u['vitals']['hr']} bpm. Normal resting is 60-100 bpm. High after exercise is okay."
        elif "blood group" in prompt_lower:
            response = f"Your blood group is {u['vitals']['bg']}. This is important for emergencies. It’s saved in your Profile."
        elif "hello" in prompt_lower or "hi" in prompt_lower:
            response = f"Hi {u['name']}! I’m your CareNova assistant. I can help with emergencies, check your vitals, or remind you about medicines. What do you need?"
        else:
            response = f"I'm here to help with safety & health, {u['name']}. For emergencies use the Home tab. For vitals use Health Tracker. You can ask me about 'blood pressure', 'medicine', or say 'sos' for help."

        st.session_state.chat_history[st.session_state.current_user].append(("Bot", response))
        with st.chat_message("assistant"):
            st.write(response)

# --- HELPLINES ---
elif menu == "Helplines":
    st.header("📞 All India Helplines - Tap to Call")
    helplines = {
        "Police": "100", "Fire": "101", "Ambulance": "108", "Women Helpline": "1091",
        "Child Helpline": "1098", "Cyber Crime": "1930", "Senior Citizen": "14567", "Disaster Management": "1078"
    }
    cols = st.columns(2)
    for i, (name, num) in enumerate(helplines.items()):
        with cols[i % 2]:
            st.markdown(f'<a href="tel:{num}"><button style="width:100%;padding:15px;margin:5px 0;background:#1e40af;color:white;border:none;border-radius:8px;font-size:16px;">{name}<br>{num}</button></a>', unsafe_allow_html=True)

# --- MY CONTACTS ---
elif menu == "My Contacts":
    st.header("👥 Your Emergency Contacts")
    new_contact = st.text_input("Add: Name - 10 digit number")
    if st.button("Add Contact"):
        if new_contact and any(char.isdigit() for char in new_contact):
            u["contacts"].append(new_contact)
            st.success("Contact added")
            st.rerun()
        else:
            st.warning("Include name and number")

    st.divider()
    if u["contacts"]:
        for i, contact in enumerate(u["contacts"]):
            col1, col2 = st.columns([3,1])
            col1.write(f"{i+1}. {contact}")
            num = ''.join(filter(str.isdigit, contact))
            if len(num) >= 10:
                col2.markdown(f'<a href="tel:{num}"><button>Call</button></a>', unsafe_allow_html=True)
    else:
        st.info("Add family/friends so you can call them fast in emergency.")

# --- SOS LOG ---
elif menu == "SOS Log":
    st.header("📋 Your SOS History")
    if u["incidents"]:
        for incident in reversed(u["incidents"]): st.warning(incident)
    else: st.success("No SOS alerts triggered. Stay safe!")

# --- DASHBOARD ---
elif menu == "Dashboard":
    st.header("📊 Your Personal Dashboard")
    v = u["vitals"]

    st.subheader("Your Vitals")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Blood Pressure", v["bp"])
    c2.metric("Heart Rate", f"{v['hr']} bpm")
    c3.metric("Blood Sugar", f"{v['sugar']} mg/dL")
    c4.metric("Weight", f"{v['weight']} kg")

    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Profile Summary")
        st.info(f"**Name:** {u['name']}\n\n**Age:** {u['age']}\n\n**Blood Group:** {v['bg']}\n\n**Height:** {v['height']} cm")
    with col2:
        st.subheader("Active Reminders")
        if u["meds"]:
            for med in u["meds"][:4]: st.warning(f"💊 {med}")
        else: st.info("No medicine reminders")

st.sidebar.markdown("---")
st.sidebar.caption(f"Logged in: {u['name']}")
st.sidebar.caption("© 2026 CareNova | Team: [Your Team Name]")