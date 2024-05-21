
# AI-Blog-Query-Responder
A Retrieval-Augmented Generation (RAG) framework utilizing Large Language Models to answer queries based on blog articles. 
<img width="835" alt="image" src="https://github.com/remisharoon/LLM-Blog-Answer-Generator/assets/8828470/e95ccece-a2f4-4874-90f7-2b72d1f6ab30">

## Setup
1. Install Ollama:
   ```bash
   https://ollama.com/download
   ollama pull mistral
   ```   
2. Install the required packages:
   ```bash
   git clone https://github.com/remisharoon/LLM-Blog-Answer-Generator.git
   cd LLM-Blog-Answer-Generator
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   streamlit run src/app.py
   ```

## Key Components
- **Ollama with 'mistral' model**: The main conversational model used for generating responses based on the retrieved context.
- **Chroma Vector Store**: Used for efficient storage and retrieval of document embeddings.
- **Document Processing**: Involves downloading articles, parsing content using BeautifulSoup, and saving them for subsequent processing.

## Data Preparation
Articles are downloaded from specified URLs, parsed for content, and saved to disk. This content is then loaded, split into chunks, 
and stored in the Chroma vector store for quick retrieval.

## Usage
- **Starting the Application**: Launch the Streamlit interface by running the main script. This will allow you to interact with the RAG model through a web interface.
- **Interacting with the Model**: Enter your queries related to the blog articles in the input field, and the model will respond with answers based on the retrieved content.

## Example Prompts
Here are some example prompts you can use to test the capabilities of the AI Blog Query Responder:

1. What are the advantages of using high-performance polymers in bonding carbon fiber laminates?
2. How does screw speed affect the durability of composites in large format additive manufacturing?
3. Can you explain the techniques used for better hydrogen storage in advanced composites?
4. What are the latest advancements in print head technologies for additive manufacturing?
5. How does the layer-by-layer automated composite curing and deposition process work?
6. What breakthroughs have been made in in-situ infrared annealing with automated fiber placement for thermoplastics?
7. How do autonomous LLM agents enhance the efficiency of automated fiber composite manufacturing?
8. What strategies are used to optimize the flexural properties of 3D printed polymer components?
9. What are the main considerations for using continuous fiber composites in automobiles?
10. Could you describe the novel path-planning approach for 3D robotic filament winding in composite materials?

These prompts are designed to query the system about specific topics related to the blog articles from the provided URLs.
