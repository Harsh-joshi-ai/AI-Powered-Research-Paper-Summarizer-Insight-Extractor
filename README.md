# AI-Powered Research Paper Summarizer & Insight Extractor

A Streamlit-based web application that enables users to ask questions and get AI-powered insights from research papers using RAG (Retrieval-Augmented Generation) and Knowledge Graph technologies.

## Features

### 1. Research Paper QA (RAG System)
- Upload and index research papers in a FAISS vector database
- Ask natural language questions about research content
- Get AI-generated answers with citations to source papers
- Powered by HuggingFace embeddings and Gemini/Groq LLMs

### 2. Knowledge Graph Explorer
- Visualize relationships between papers, authors, methods, and domains
- Interactive graph visualization using pyvis
- Filter by research domain
- Export data to Excel

## Project Structure

```
.
├── main_2.py                 # Main Streamlit application
├── ask_db.py                 # Alternative QA interface
├── llm_call.py              # LLM integration (Gemini & Groq)
├── Data_extraction_pdf_refined.py  # PDF text extraction & parsing
├── summary_and_insights.py  # T5 summarization & insight extraction
├── arxiv_data_injest.py     # ArXiv paper data ingestion
├── pubmedd.py               # PubMed paper data ingestion
├── neo4j_upload_data.py     # Upload data to Neo4j graph database
├── upload_on_RAG.py         # RAG pipeline utilities
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables (API keys)
├── data/                    # Input PDF research papers
├── research_papers_faiss/   # FAISS vector database
├── parsed_output/           # Extracted JSON metadata
└── graph.html               # Knowledge graph visualization
```

## Installation

### Prerequisites
- Python 3.8+
- Neo4j database (for Knowledge Graph features)
- API keys for Gemini and Groq

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd "Infosys Final submission"
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # Linux/Mac
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Download spaCy model**
   ```bash
   python -m spacy download en_core_web_sm
   ```

5. **Configure environment variables**

   Create a `.env` file with your API keys:
   ```
   GEMINI_API_KEY=your_gemini_api_key
   GROQ_API_KEY=your_groq_api_key
   ```

6. **Setup Neo4j Database** (for Knowledge Graph features)
   - Install Neo4j Desktop or use Neo4j Aura
   - Create a database with username `neo4j` and update password in `main_2.py`
   - Run `neo4j_upload_data.py` to populate the graph

## Usage

### Running the Application

```bash
streamlit run main_2.py
```

The application will open in your default browser at `http://localhost:8501`

### Adding Research Papers

1. Place PDF files in the `data/` directory
2. Run the data extraction script:
   ```bash
   python Data_extraction_pdf_refined.py
   ```
3. Upload to vector database using `upload_on_RAG.py`

### Ingesting from External Sources

- **ArXiv papers**: Run `python arxiv_data_injest.py`
- **PubMed papers**: Run `python pubmedd.py`

## Core Components

### LLM Integration (`llm_call.py`)
- **Gemini API**: Primary LLM for answering questions
- **Groq API**: Fallback LLM with Llama models
- Implements prompt engineering for research-focused responses

### PDF Data Extraction (`Data_extraction_pdf_refined.py`)
- Extracts title, authors, abstract, and content
- Cleans and structures text using regex patterns
- Outputs structured JSON with metadata

### Summarization (`summary_and_insights.py`)
- T5 model for abstractive summarization
- Groq-based insight extraction for structured data:
  - Domain classification
  - Research problems
  - Methods and datasets
  - Key findings and limitations

### Vector Database
- **FAISS** for similarity search
- **HuggingFace Embeddings** (all-MiniLM-L6-v2)
- Supports semantic search across papers

## API Endpoints & Models

| Component | Model/Service | Purpose |
|-----------|---------------|---------|
| Embeddings | sentence-transformers/all-MiniLM-L6-v2 | Text vectorization |
| Primary LLM | gemini-2.5-flash | Question answering |
| Fallback LLM | groq-1.5-flash / llama-3.1-8b-instant | Backup & insights |
| Summarization | T5 | Abstract summarization |

## Output Formats

### Research Paper QA
- AI-generated answers with citations
- Links to relevant paper sections

### Knowledge Graph
- Interactive HTML visualization
- Excel export with paper/author/method data

### Structured Insights (JSON)
```json
{
  "domain": [],
  "research_problem": "",
  "methods": [],
  "datasets": [],
  "metrics": [],
  "key_findings": "",
  "limitations": "",
  "future_directions": ""
}
```

## Dependencies

Key packages:
- `streamlit` - Web UI framework
- `langchain` - RAG orchestration
- `faiss-cpu` - Vector similarity search
- `neo4j` - Graph database
- `pyvis` - Network visualization
- `transformers` - T5 summarization
- `pymupdf` - PDF text extraction
- `google-genai`, `groq` - LLM APIs

## Configuration

Update these values in `main_2.py` as needed:
- Neo4j connection credentials (line 175)
- FAISS database path (line 60)
- Embedding model (line 56)

## Known Limitations

- Requires internet connection for LLM API calls
- Neo4j must be running locally on port 7687
- PDF extraction works best with well-structured academic papers

## License

This project is for educational purposes.

## Acknowledgments

- Gemini API by Google
- Groq Cloud for LLM inference
- HuggingFace for open-source models
- LangChain community
