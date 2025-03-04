import streamlit as st
import requests
import os

API_URL = "http://127.0.0.1:8000/research"

st.set_page_config(page_title="AI Research Agent", layout="wide")

st.title("🔍 AI-Powered Research Agent")

query = st.text_input("Enter your research topic:", "")

if st.button("Generate Research"):
    if query.strip():
        with st.spinner("Fetching research..."):
            response = requests.post(API_URL, json={"query": query})

            if response.status_code == 200:
                research_result = response.json().get("response", "No data found.")
                st.markdown("### 📌 Research Summary")
                st.write(research_result)

                # Save response as Markdown
                file_path = f"responses/{query.replace(' ', '_')}.md"
                os.makedirs("responses", exist_ok=True)
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(research_result)

                st.success("✅ Research completed!")

                # Provide a download option
                st.download_button("📥 Download Summary", data=research_result, file_name=f"{query}.md", mime="text/markdown")
            else:
                st.error("❌ Error fetching research.")
    else:
        st.warning("Please enter a topic.")
