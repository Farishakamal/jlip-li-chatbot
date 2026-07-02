# JLIP FAQ Chatbot 🤖
An automated 24/7 online knowledge retrieval chatbot assistant engineered for the Students Industrial Training Department (JLIP), Centre of Career Advancement and Alumni (PKKA), Universiti Tun Hussein Onn Malaysia (UTHM).

## 🚀 Live Application
Access the production environment here: [Open Live Chatbot](https://jlip-li-chatbot-xciv4vrrjdjez2hzw42gz3.streamlit.app/)

---

## 📌 Project Overview
* **Problem:** Core administrative staff operational hours are consistently bottlenecked by high volumes of repetitive student inquiries regarding internship forms, rules, and placement deadlines.
* **Objective:** To build an automated online assistant that delivers accurate, instant, and context-aware answers to students based strictly on official department documentation.

---

## 🛠️ System Architecture & Stack
This chatbot is designed using a **Retrieval-Augmented Generation (RAG)** framework:
* **Frontend/Interface:** Python & Streamlit Framework
* **Vector Database:** FAISS (Facebook AI Similarity Search) to store and parse official PDF/text guidelines.
* **AI Core Engine:** Gemini 1.5-Flash API for natural, safe, and conversational response processing in Malay.

---

## 📁 Repository Structure
* `app.py` - The primary production source code handling the Streamlit user interface and AI chatbot logic.
* `build_vector.py` - The script responsible for reading, chunking, embedding, and saving official documents into the FAISS database.
* `requirements.txt` - Python dependency manifest containing required library versions for deployment alignment.

---

## 🔐 System Maintenance & API Rollover
The application runs on cloud environment tokens. If the bot stops responding, the daily transaction quota has expired. 

To replace the token:
1. Log into **Streamlit Community Cloud**.
2. Navigate to **App Settings -> Secrets**.
3. Replace the old key string using this exact key-value mapping:
   ```text
   GOOGLE_API_KEY = "AIzaSyB-Your_New_API_Key_Here"