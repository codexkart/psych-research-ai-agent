from llm.ollama_client import query_ollama

def summarize_papers(papers, model="mistral:7b-instruct-q3_K_S"):
    summaries = []
    for paper in papers:
        prompt = f"Summarize the following abstract in 2-3 bullet points:\n\n{paper['summary']}"
        summary = query_ollama(prompt, model)
        summaries.append({
            "title": paper["title"],
            "url": paper["url"],
            "summary": summary.strip()
        })
    return summaries

def generate_takeaways_and_tips(summaries, model="mistral:7b-instruct-q3_K_S"):
    combined = "\n\n".join([s["summary"] for s in summaries])
    prompt = f"""
You are an expert research assistant. Based on the following summarized papers:

{combined}

Please return:
1. Three key takeaways (bullet points)
2. Three actionable training recommendations (bullet points)
Write the headings along with their bullet points. There should be exactly 3 bullet points for each heading.
"""
    return query_ollama(prompt, model).strip()
