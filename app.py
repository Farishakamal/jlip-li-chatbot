import os
import datetime
import time
from dotenv import load_dotenv
import streamlit as st
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from google import genai
from google.genai import types

# --- 1. SETUP CONFIG & CORE ---
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

st.set_page_config(
    page_title="Sistem Sokongan LI PKKA - JLIP", 
    page_icon="🏛️", 
    layout="centered"
)

# Initialize Google GenAI Client
client = genai.Client(api_key=api_key)

# --- 2. CUSTOM CSS ---
custom_css = """
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<style>
    /* Sembunyikan footer asal Streamlit */
    footer {visibility: hidden;}
    
    .streamlit-expanderHeader {
        font-weight: 600; 
    }
    
    .corporate-header {
        text-align: center;
        padding: 20px 0 10px 0;
        margin-bottom: 20px;
        border-bottom: 2px solid #b38600; /* Jalur Emas UTHM */
    }
    .corporate-header h2 {
        color: #002147; /* Navy Blue UTHM */
        font-weight: 700;
        margin-bottom: 5px;
    }
    .corporate-header .unit-title {
        color: #b38600; /* Gold Accent */
        font-size: 1.1rem;
        font-weight: 600;
        margin: 0 0 5px 0;
    }
    .corporate-header p {
        color: var(--faded-text-color);
        font-size: 0.90rem;
        margin: 0;
    }
    
    .fa-phone, .fa-envelope, .fa-map-location-dot, .fa-circle-info {
        color: #002147; 
        width: 20px; 
        text-align: center;
        margin-right: 5px;
    }
    
    .contact-link {
        color: #0066cc;
        text-decoration: none;
        font-weight: 500;
    }
    .contact-link:hover {
        text-decoration: underline;
    }
    
    .stButton>button {
        margin-bottom: 5px;
        border: 1px solid #002147 !important;
        color: #002147 !important;
    }
    .stButton>button:hover {
        background-color: #002147 !important;
        color: white !important;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# --- 3. CHAT BUBBLES ---
def paparkan_mesej(peranan, teks, masa):
    if peranan == "user":
        html = f"""
        <div style='display: flex; justify-content: flex-end; margin-bottom: 20px; align-items: flex-start;'>
            <div style='background-color: #002147; color: white; padding: 12px 18px; border-radius: 12px 0px 12px 12px; max-width: 80%; font-size: 0.95rem; box-shadow: 0 2px 5px rgba(0,0,0,0.1);'>
                <p style='margin:0; line-height: 1.5;'>{teks}</p>
                <div style='font-size: 0.7rem; color: rgba(255,255,255,0.7); text-align: right; margin-top: 8px;'>{masa}</div>
            </div>
            <div style='margin-left: 10px; background-color: #002147; color: white; border-radius: 50%; width: 40px; height: 40px; display: flex; align-items: center; justify-content: center; font-size: 1.1rem; flex-shrink: 0; box-shadow: 0 2px 4px rgba(0,0,0,0.15); border: 2px solid #b38600;'>
                <i class="fa-solid fa-user"></i>
            </div>
        </div>
        """
    else:
        # ICON ROBOT 
        html = f"""
        <div style='display: flex; justify-content: flex-start; margin-bottom: 20px; align-items: flex-start;'>
            <div style='margin-right: 10px; background-color: var(--secondary-background-color); border-radius: 50%; width: 40px; height: 40px; display: flex; align-items: center; justify-content: center; font-size: 1.2rem; flex-shrink: 0; box-shadow: 0 2px 4px rgba(0,0,0,0.15); border: 2px solid #002147;'>
                <i class="fa-solid fa-robot" style="color: rgb(2, 45, 78);"></i>
            </div>
            <div style='background-color: var(--secondary-background-color); color: var(--text-color); padding: 12px 18px; border-radius: 0px 12px 12px 12px; max-width: 80%; font-size: 0.95rem; box-shadow: 0 2px 5px rgba(0,0,0,0.05);'>
                <strong style='font-size: 0.75rem; color: #b38600; display:block; margin-bottom: 6px; text-transform: uppercase; letter-spacing: 0.5px;'>JLIP Assistant</strong>
                <div style='margin:0; line-height: 1.5;'>{teks}</div>
                <div style='font-size: 0.7rem; color: var(--faded-text-color); text-align: right; margin-top: 8px;'>{masa}</div>
            </div>
        </div>
        """
    st.markdown(html, unsafe_allow_html=True)

# --- 4. LOAD VECTOR STORE (FAISS LOKAL) ---
@st.cache_resource
def load_vector_store():
    vector_dir = "vectorstore"
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    if os.path.exists(vector_dir):
        return FAISS.load_local(vector_dir, embeddings, allow_dangerous_deserialization=True)
    else:
        st.error("❌ Pangkalan data 'vectorstore' tidak dijumpai!")
        return None

db = load_vector_store()

# --- 5. SIDEBAR  ---
with st.sidebar:
    # Logo UTHM di bahagian paling atas sidebar
    logo_url = "https://www.uthm.edu.my/en/downloads/uthm-official-logo/26-logo-rasmi-uthm/file"
    
    col_logo1, col_logo2, col_logo3 = st.columns([1, 5, 1])
    with col_logo2:
        # Ditambah margin_bottom pada HTML/CSS utama atau menggunakan div spacer di bawah
        st.image(logo_url, use_container_width=True)
        
    # --- SPACER ---
    st.markdown("<div style='margin-bottom: 25px;'></div>", unsafe_allow_html=True)
    
    st.markdown("**<i class='fa-solid fa-circle-info'></i> Unit JLIP**", unsafe_allow_html=True)
    st.write("Chatbot FAQ Latihan Industri yang menyediakan maklumat dan menjawab pertanyaan berkaitan Latihan Industri berdasarkan Garis Panduan Latihan Industri UTHM.")
    
    st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)
    
    st.markdown("**Direktori Perhubungan**")
    st.markdown("<i class='fa-solid fa-map-location-dot'></i> Blok D15, PKKA UTHM, 86400 Parit Raja.", unsafe_allow_html=True)
    
    with st.expander("Talian Pejabat & E-mel"):
        st.markdown("""
        <div style='font-size: 0.85rem; line-height: 1.6;'>
        <b>Latihan Industri (Outbound):</b><br>
        <i class="fa-solid fa-phone"></i> <a class="contact-link" href="tel:074537457">07-453 7457</a><br>
        <i class="fa-regular fa-envelope"></i> <a class="contact-link" href="mailto:li@uthm.edu.my">li@uthm.edu.my</a><br><br>
        
        <b>Latihan Industri (Inbound):</b><br>
        <i class="fa-solid fa-phone"></i> <a class="contact-link" href="tel:074537043">07-453 7043</a><br>
        <i class="fa-regular fa-envelope"></i> <a class="contact-link" href="mailto:inboundli@uthm.edu.my">inboundli@uthm.edu.my</a>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("Clear Chat", icon=":material/delete:", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# --- 6. HEADER UTAMA KORPORAT ---
st.markdown("""
    <div class='corporate-header'>
        <h2>UTHM Industrial Training Assistant</h2>
        <div class='unit-title'>Student Industrial Training Department (JLIP)</div>
        <p>Pusat Kemajuan Kerjaya dan Alumni (PKKA)</p>
    </div>
""", unsafe_allow_html=True)

current_time = datetime.datetime.now().strftime("%I:%M %p")

# --- 7. INITIALIZE SESSION STATE FOR CHAT ---
if "messages" not in st.session_state or len(st.session_state.messages) == 0:
    st.session_state.messages = [
        {
            "role": "assistant", 
            "content": "👋 Selamat datang! Saya sedia membantu menjawab pertanyaan anda berkaitan Latihan Industri. Sila masukkan soalan anda, dan saya akan memberikan jawapan berdasarkan Garis Panduan Latihan Industri UTHM.", 
            "time": current_time
        }
    ]

# Papar sejarah sembang
for message in st.session_state.messages:
    paparkan_mesej(message["role"], message["content"], message.get("time", ""))


# --- 8. INPUT PENGGUNA & PEMPROSESAN RAG ---

# untuk mengelakkan NameError
question_to_process = None 

user_input = st.chat_input("Masukkan pertanyaan anda di sini...")

if user_input:
    question_to_process = user_input

# Baris yang keluar ralat tadi akan membaca variable di atas dengan selamat
if question_to_process:
    time_now = datetime.datetime.now().strftime("%I:%M %p")
    # Simpan soalan user
    st.session_state.messages.append({"role": "user", "content": question_to_process, "time": time_now})
    
    # animasi spinner semasa memproses data RAG
    with st.spinner("Carian sedang dimuatkan..."):
        if db:
            try:
                # Cari dokumen padanan dari FAISS
                docs = db.similarity_search(question_to_process, k=3)
                konteks_dokumen = "\n\n".join([doc.page_content for doc in docs])
                
                system_instruction = (
                    "Anda adalah sistem kecerdasan buatan (AI) rasmi bagi chatbot pengurusan Latihan Industri di bawah unit Student Industrial Training Department (JLIP), PKKA UTHM. "
                    "Tugas anda adalah membantu menjawab kemusykilan pelajar berkaitan urusan Latihan Industri dengan ringkas, jelas, dan profesional berdasarkan dokumen yang diberikan. "
                    "Gunakan bahasa Melayu yang mudah difahami oleh seorang mahasiswa. Elakkan menggunakan istilah teknikal pentadbiran seperti 'pemurnian' atau 'garis panduan' secara berulang-ulang. "
                    "Jika maklumat tiada dalam dokumen, jawab dengan mesra: 'Maaf, maklumat spesifik tersebut tiada dalam rekod data semasa saya. Sila hubungi urus setia PKKA UTHM atau pensyarah penilai untuk semakan lanjut ya.'"
                )
                
                full_prompt = f"Konteks Dokumen:\n{konteks_dokumen}\n\nSoalan Pelajar: {question_to_process}"
                
                # jawapan AI
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=full_prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=system_instruction,
                        temperature=0.25
                    )
                )
                
                time_reply = datetime.datetime.now().strftime("%I:%M %p")
                st.session_state.messages.append({"role": "assistant", "content": response.text, "time": time_reply})
                
            except Exception as e:
                st.error(f"Ralat rangkaian AI: {e}")
                
    st.rerun()
    
    
    