# build_vector.py
import os
from pypdf import PdfReader
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document

def proses_pdf_ke_vector():
    pdf_path = "Lampiran 1 Jadual Pemurnian Garis Panduan 2026.pdf"
    vector_dir = "vectorstore"
    
    print("🔄 Langkah 1: Membaca fail PDF menggunakan pypdf...")
    if not os.path.exists(pdf_path):
        print(f"❌ Error: Fail PDF '{pdf_path}' tidak dijumpai!")
        return

    # Membaca fail menggunakan pypdf standard (Kalis bug Python 3.14)
    reader = PdfReader(pdf_path)
    documents = []
    
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            # Tukar ke format Document yang difahami oleh FAISS
            documents.append(Document(page_content=text, metadata={"page": i + 1}))
            
    print(f"✅ Selesai membaca. Jumlah muka surat: {len(documents)}")

    print("🔄 Langkah 2: Memecahkan teks kepada chunks...")
    # Trik memecah chunks secara manual untuk elakkan import langchain_text_splitters
    chunks = []
    for doc in documents:
        text = doc.page_content
        # Pecahkan setiap ~1000 aksara
        words = text.split()
        for i in range(0, len(words), 150):  # Ambil rantaian perkataan
            chunk_text = " ".join(words[i:i+200])
            chunks.append(Document(page_content=chunk_text, metadata=doc.metadata))
            
    print(f"✅ Selesai. Terhasil {len(chunks)} chunks.")

    print("🔄 Langkah 3: Menghasilkan Embeddings menggunakan HuggingFace...")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    print("🔄 Langkah 4: Menyimpan ke dalam Vector Store (FAISS)...")
    vector_store = FAISS.from_documents(chunks, embeddings)
    vector_store.save_local(vector_dir)
    print(f"\n🎉 TAHNIAH! Vector Database berjaya dibina dan disimpan di folder '{vector_dir}'.")

if __name__ == "__main__":
    proses_pdf_ke_vector()