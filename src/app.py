import os
import requests
import streamlit as st
from streamlit_chat import message
from rag import RAGFramework
from bs4 import BeautifulSoup

st.set_page_config(page_title="Blog RAG Assistant")

BLOG_URLS = [
    "https://www.addcomposites.com/post/peek-carbon-fiber-laminate-bonding-with-high-performance-polymer-processed-by-fff-3d-printing",
    "https://www.addcomposites.com/post/how-screw-speed-influences-composite-durability-in-large-format-additive-manufacturing",
    "https://www.addcomposites.com/post/advanced-composite-utilization-techniques-for-better-hydrogen-storage",
    "https://www.addcomposites.com/post/advanced-print-head-technologies-transform-additive-manufacturing",
    "https://www.addcomposites.com/post/layer-by-layer-automated-composite-curing-and-deposition-snap-curing-thermoset-prepreg",
    "https://www.addcomposites.com/post/in-situ-infrared-annealing-breakthrough-with-automated-fiber-placement-for-cf-peek-thermoplastic-com",
    "https://www.addcomposites.com/post/autonomous-llm-agents-streamline-automated-fiber-composite-manufacturing",
    "https://www.addcomposites.com/post/optimizing-flexural-properties-of-3d-printed-polymer-components-with-strategic-fiber-placement",
    "https://www.addcomposites.com/post/continuous-fiber-composites-materials-in-automobile-overview",
    "https://www.addcomposites.com/post/3d-robotic-filament-winding-for-high-performance-composite-materials-a-novel-path-planning-approach"
]


def fetch_article(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error on bad status
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None


def save_article(content, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(content)


def retrieve_articles(urls):
    texts = []
    if not os.path.exists('data/articles'):
        os.makedirs('data/articles')
    for i, url in enumerate(urls, 1):
        print(f"Downloading article {i} from {url}")
        html_content = fetch_article(url)
        if html_content:
            soup = BeautifulSoup(html_content, 'html.parser')
            # Assuming articles are within <article> tags
            article_content = soup.find('article').text if soup.find('article') else "No article content found"
            save_article(article_content, f'data/articles/article_{i}.txt')
        texts.append(article_content)
    return texts


def display_messages():
    st.subheader("Chat")
    for i, (msg, is_user) in enumerate(st.session_state["messages"]):
        message(msg, is_user=is_user, key=str(i))
    st.session_state["thinking_spinner"] = st.empty()


def process_input():
    if st.session_state["user_input"] and len(st.session_state["user_input"].strip()) > 0:
        user_text = st.session_state["user_input"].strip()
        with st.session_state["thinking_spinner"], st.spinner(f"Thinking"):
            agent_text = st.session_state["rag_framework"].ask(user_text)

        st.session_state["messages"].append((user_text, True))
        st.session_state["messages"].append((agent_text, False))


def page():
    if len(st.session_state) == 0:
        st.session_state["messages"] = []
        st.session_state["rag_framework"] = RAGFramework()
        st.session_state["texts"] = retrieve_articles(BLOG_URLS)
        st.session_state["rag_framework"].load_documents()

    st.header("Blog RAG Assistant")

    display_messages()
    st.text_input("Ask a question about the blogs", key="user_input", on_change=process_input)


if __name__ == "__main__":
    page()
