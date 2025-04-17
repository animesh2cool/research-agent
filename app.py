import streamlit as st
from agents.search_agent import SearchAgent
from agents.analysis_agent import AnalysisAgent
from agents.report_agent import ReportAgent
import datetime
from xhtml2pdf import pisa
import io

# ---------------------- PDF Helper ----------------------
def generate_pdf_from_html(html_content):
    pdf_buffer = io.BytesIO()
    pisa_status = pisa.CreatePDF(io.StringIO(html_content), dest=pdf_buffer)
    if pisa_status.err:
        return None
    return pdf_buffer.getvalue()

# ---------------------- HTML Helper ----------------------
def generate_html_file(html_content):
    return html_content.encode("utf-8")

# ---------------------- Streamlit Setup ----------------------
st.set_page_config(page_title="Open Research Analyst", layout="wide")

# ---------------------- Top Navigation Bar ----------------------
st.markdown("""
    <style>
        .top-bar {
            background-color: #f9f9f9;
            padding: 15px 30px;
            border-bottom: 1px solid #ddd;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        .top-bar h1 {
            margin: 0;
            font-size: 24px;
            color: #333;
        }
        .top-bar img {
            height: 40px;
        }
        @media (max-width: 768px) {
            .top-bar {
                flex-direction: column;
                text-align: center;
            }
            .top-bar img {
                margin-top: 10px;
            }
        }
    </style>
    <div class="top-bar">
        <h1>🧠 Open Research Analyst</h1>
        <img src="https://raw.githubusercontent.com/streamlit/branding/master/logos/mark/streamlit-mark-color.png" alt="Logo">
    </div>
""", unsafe_allow_html=True)

# ---------------------- Session State ----------------------
if "history" not in st.session_state:
    st.session_state.history = []

if "is_processing" not in st.session_state:
    st.session_state.is_processing = False

# ---------------------- Main UI ----------------------
st.markdown("### 🔍 Powered by CrewAI, DuckDuckGo & LLaMA (Ollama)")

query = st.text_input("🔎 What do you want to research?", "")

run_clicked = st.button("🚀 Run Research", disabled=st.session_state.is_processing)

# ---------------------- Main Logic ----------------------
if run_clicked and query.strip():
    st.session_state.is_processing = True
    status_placeholder = st.empty()
    timeline = []

    try:
        # Step 1: Search Agent
        status_placeholder.info("🔎 [1/3] Running Search Agent...")
        timeline.append(("🔎 Search Agent", datetime.datetime.now().strftime("%H:%M:%S")))
        with st.spinner("Collecting search results..."):
            search_agent = SearchAgent()
            search_results = search_agent.search(query)

        # Step 2: Analysis Agent
        status_placeholder.info("🧠 [2/3] Running Analysis Agent...")
        timeline.append(("🧠 Analysis Agent", datetime.datetime.now().strftime("%H:%M:%S")))
        with st.spinner("Analyzing search results..."):
            analysis_agent = AnalysisAgent()
            analysis = analysis_agent.analyze(search_results, query)

        # Step 3: Report Agent
        status_placeholder.info("📝 [3/3] Generating Final Report...")
        timeline.append(("📝 Report Agent", datetime.datetime.now().strftime("%H:%M:%S")))
        with st.spinner("Generating final report..."):
            report_agent = ReportAgent()
            final_report = report_agent.generate_report(analysis, query)

        status_placeholder.success("✅ Research Complete!")

        # Show Final Output
        st.markdown("## 📄 Final Report")
        st.markdown(final_report, unsafe_allow_html=True)
        st.download_button("📥 Download Report (Markdown)", final_report, file_name="research_report.md")

        # PDF Export
        pdf_bytes = generate_pdf_from_html(final_report)
        if pdf_bytes:
            st.download_button("📄 Export Report as PDF", pdf_bytes, file_name="research_report.pdf", mime="application/pdf")
        else:
            st.error("❌ Failed to generate PDF. Try again.")

        # HTML Export
        html_bytes = generate_html_file(final_report)
        st.download_button("🌐 Export Report as HTML", html_bytes, file_name="research_report.html", mime="text/html")

        # Timeline
        st.markdown("## ⏱️ Timeline of Agents")
        for step, timestamp in timeline:
            st.markdown(f"**{timestamp}** — {step}")

        # Sub-results
        with st.expander("🔍 View Raw Search Results"):
            st.markdown(search_results)

        with st.expander("🧠 View Analysis"):
            st.markdown(analysis)

        # Session history
        st.session_state.history.append({
            "query": query,
            "report": final_report,
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

    except Exception as e:
        st.error(f"🚨 Error: {str(e)}")

    st.session_state.is_processing = False

elif run_clicked and not query.strip():
    st.warning("⚠️ Please enter a topic before clicking Run.")

# ---------------------- Session History ----------------------
st.markdown("---")
st.markdown("## 📚 Session History")

if st.session_state.history:
    for i, item in enumerate(reversed(st.session_state.history), 1):
        with st.expander(f"{i}. {item['query']} ({item['timestamp']})"):
            st.markdown(item["report"], unsafe_allow_html=True)
else:
    st.info("No history yet. Run a query to start!")
