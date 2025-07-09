import streamlit as st
from fetch_papers.arxiv_fetcher import fetch_arxiv_papers
from llm.summarizer import summarize_papers, generate_takeaways_and_tips

# --- Page Setup ---
st.set_page_config(page_title="🧠 Psych Research AI Agent", layout="wide")
st.title("🔍 Psych Research AI Agent")
st.caption("Powered by Ollama + arXiv")

# --- Input ---
query = st.text_input("📥 Enter a research topic:", placeholder="e.g. sports stress management")

# --- Start Pipeline ---
if st.button("🚀 Fetch & Analyze"):
    if not query:
        st.warning("⚠️ Please enter a research topic.")
    else:
        with st.spinner("📚 Fetching academic papers..."):
            papers = fetch_arxiv_papers(query, max_results=5)

        if not papers:
            st.error("❌ No papers found. Try a different query.")
        else:
            with st.spinner("📝 Summarizing research papers..."):
                summaries = summarize_papers(papers)

            with st.spinner("🧠 Generating insights..."):
                insights = generate_takeaways_and_tips(summaries)

            # --- Section 1: Paper Summaries ---
            st.markdown("## 📄 Research Paper Summaries")
            for s in summaries:
                with st.expander(f"🔎 {s['title']}"):
                    st.markdown(f"[🔗 View on arXiv]({s['url']})", unsafe_allow_html=True)
                    st.markdown(s["summary"])

            # --- Section 2: Takeaways & Recommendations ---
            st.markdown("---")
            st.markdown("## 📌 Insights Summary")

            takeaways = []
            recommendations = []

            # 🛠️ Use headings to split cleanly
            if "recommendations" in insights.lower():
                try:
                    parts = insights.split("Training Recommendations:")
                    takeaway_block = parts[0].replace("Key Takeaways:", "").strip()
                    recommendation_block = parts[1].strip()

                    takeaways = [line.strip("-• ").strip() for line in takeaway_block.split("\n") if line.strip()]
                    recommendations = [line.strip("-• ").strip() for line in recommendation_block.split("\n") if
                                       line.strip()]
                except Exception as e:
                    st.error("❌ Failed to parse insights. Here's the raw output:")
                    st.markdown(insights)
            else:
                st.warning("⚠️ Unable to detect takeaways/recommendations in output. Showing raw:")
                st.markdown(insights)

            # ✅ Display nicely in columns if extracted
            if takeaways and recommendations:
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("### ✅ Key Takeaways")
                    for t in takeaways:
                        st.markdown(f"- {t}")
                with col2:
                    st.markdown("### 🎯 Training Recommendations")
                    for r in recommendations:
                        st.markdown(f"- {r}")
# --- Optional Footer ---
st.markdown("---")
st.caption("🧪 Built by your AI research assistant using Ollama + Streamlit + arXiv")