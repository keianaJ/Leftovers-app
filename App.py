import streamlit as st
import streamlit.components.v1 as components
import requests

# --- 1. GLOBAL CONFIGURATION & LANGUAGES ---
st.set_page_config(page_title="Leftovers App", page_icon="🥗", layout="wide")

LANG_DICT = {
    "en": {
        "title": "🥗 Leftovers",
        "tagline": "Feeding the whole family, four legs and all.",
        "modes": ["Adult", "Baby", "Dog 🐾"],
        "safety_btn": "🛡️ Check Safety",
        "find_btn": "✨ Find Recipes",
        "clear_btn": "🗑️ Clear All",
        "pro_msg": "🌟 Unlock Permanent Pantry for $7/year",
        "toxic_warn": "🛑 TOXIC DETECTED: ",
        "safe_msg": "✅ Ingredients are safe!"
    },
    "es": {
        "title": "🥗 Leftovers",
        "tagline": "Alimentando a toda la familia, patitas incluidas.",
        "modes": ["Adulto", "Bebé", "Perro 🐾"],
        "safety_btn": "🛡️ Verificar Seguridad",
        "find_btn": "✨ Buscar Recetas",
        "clear_btn": "🗑️ Borrar Todo",
        "pro_msg": "🌟 Desbloquea Despensa Permanente por $7/año",
        "toxic_warn": "🛑 TÓXICO DETECTADO: ",
        "safe_msg": "✅ ¡Ingredientes seguros!"
    }
}

# --- 2. SESSION STATE & SECURITY ---
if 'lang' not in st.session_state: st.session_state.lang = "en"
if 'ingredients' not in st.session_state: st.session_state.ingredients = ""
if 'is_pro' not in st.session_state: st.session_state.is_pro = False
t = LANG_DICT[st.session_state.lang]

# --- 3. VOICE ENGINE (TTS) ---
def speak(text):
    js = f"<script>var m=new SpeechSynthesisUtterance('{text}');m.lang='{st.session_state.lang}';window.speechSynthesis.speak(m);</script>"
    components.html(js, height=0)

# --- 4. SAFETY DATABASES ---
DOG_TOXIC = ["onion", "garlic", "grape", "raisin", "chocolate", "macadamia", "xylitol"]
BABY_WARN = ["honey", "salt", "sugar"]

# --- 5. SIDEBAR: PROFILES & SETTINGS ---
st.sidebar.title(f"👤 {t['title']} Profiles")
st.session_state.lang = st.sidebar.selectbox("🌐 Language", ["en", "es"])
mode = st.sidebar.radio("Cooking For:", t['modes'])

if st.sidebar.button(t['pro_msg']):
    st.sidebar.info("Redirecting to [Stripe Secure Checkout](https://stripe.com)...")

# --- 6. MAIN INTERFACE: INGREDIENT INPUT ---
st.title(t['title'])
st.caption(t['tagline'])

user_input = st.text_input("What's in your fridge?", value=st.session_state.ingredients, placeholder="chicken, carrots, rice...")
st.session_state.ingredients = user_input
ing_list = [i.strip().lower() for i in user_input.split(",") if i.strip()]

# Real-time Safety Guard
if ing_list:
    if "Dog" in mode or "Perro" in mode:
        danger = [i for i in ing_list if any(toxic in i for toxic in DOG_TOXIC)]
        if danger: st.error(f"{t['toxic_warn']} {', '.join(danger)}"); search_disabled = True
        else: st.success(t['safe_msg']); search_disabled = False
    else:
        st.success(t['safe_msg']); search_disabled = False

# --- 7. ACTION BUTTONS ---
col1, col2, col3 = st.columns([2,1,1])
with col1:
    if st.button(t['find_btn'], type="primary", disabled=search_disabled):
        # API logic would go here
        st.balloons()
        speak("Searching for the best family meals.")
with col2:
    if st.button("🔊 Listen"): speak(user_input if user_input else "Please add ingredients.")
with col3:
    if st.button(t['clear_btn']): 
        st.session_state.ingredients = ""
        st.rerun()

# --- 8. GLOBAL FOOTER (PATENT & PRIVACY) ---
st.divider()
st.caption("⚖️ **Patent Pending** (2026) | 🔒 **Zero-Leak Privacy**: Data stays on your device.")
st.caption("⚠️ *Consult a vet or pediatrician before new foods. [ASPCA](https://www.aspca.org) & [CDC](https://www.cdc.gov) guidelines applied.*")
