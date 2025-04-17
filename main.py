from agents.search_agent import SearchAgent
from agents.analysis_agent import AnalysisAgent
from agents.report_agent import ReportAgent

def main():
    user_query = input("Enter your research query: ")

    search_agent = SearchAgent()
    analysis_agent = AnalysisAgent()
    report_agent = ReportAgent()

    # Step 1: Search
    results = search_agent.search(user_query)

    # Step 2: Analyze
    analysis = analysis_agent.analyze(results, user_query)

    # Step 3: Generate Report
    final_report = report_agent.generate_report(analysis, user_query)

    # Output the report
    with open("final_report.md", "w", encoding="utf-8") as f:
        f.write(final_report)

    print("\n✅ Research report saved to final_report.md")

if __name__ == "__main__":
    main()
