from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from  llm_call import * 
import streamlit as st

#Title
st.markdown(
    "<h1 style='text-align:center;'>AI-Powered Research Paper Summarizer & Insight Extractor</h1>",
    unsafe_allow_html=True
)

#Small Description
st.markdown(
    "<p style='text-align:center;color:white'>Ask questions and get Ai-powered insights from research papers.</p>",
    unsafe_allow_html=True
)

# Custom CSS for input box
st.markdown(
    """
    <style>
    .stTextInput input {
        background-color:#000000;
        border: 1px solid #ccc;
        border-radius: 5px;
        padding: 10px;
        width: 100%;
        font-size: 16px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

@st.cache_resource
def load_vector_db():
    # load embedding model 
    embeddings = HuggingFaceEmbeddings(
        model_name = "sentence-transformers/all-MiniLM-L6-v2"
    )


    # load FAISS vector store 

    vector_db = FAISS.load_local(
        "research_papers_faiss",
        embeddings,
        allow_dangerous_deserialization= True
    )

    return vector_db

vector_db=load_vector_db()




#show total papers in the vector db
st.write(f"Total Research Papers in Database: {vector_db.index.ntotal}")

# user query 
user_query= st.text_input("Enter your research question here:")


# Search button
if st.button("Search") and user_query:

    results = vector_db.similarity_search(user_query, k=3)

    content=""

    for idx, doc in enumerate(results, 1):
        title = doc.metadata.get("title", f"Paper {idx}")
        content += f"""
        Paper Title: {title}
        Paper Content: {doc.page_content}
        """

    with st.spinner("Generating insights from research papers..."):
        response = ask_gemini(content, user_query)

    # Parse Gemini output
    answer=""
    paper_title=[]

    if "Research Paper:" in response:

        parts = response.split("Research Paper:")
        answer = parts[0].replace("Answer:", "").strip()
        paper_text = parts[1].strip()

        paper_title = [p.strip() for p in paper_text.split(",")]

    else:
        answer = response.strip()

    st.subheader("AI Generated Insights")
    st.write(answer)

    if paper_title and "none" not in [p.lower() for p in paper_title]:

        st.subheader("Relevant Research Papers")

        for doc in results:
            title = doc.metadata.get("title","")

            for p in paper_title:
                if title.lower() == p.lower():

                    with st.expander(title):
                        st.write(doc.page_content)

    else:
        st.warning("No relevant research papers found.")