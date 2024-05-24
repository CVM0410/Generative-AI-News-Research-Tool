# Generative AI News Research Tool

## Overview
The Generative AI News Research Tool is a sophisticated application designed for equity research analysts focusing on financial markets. By leveraging OpenAI's API, LangChain, and Streamlit, this tool facilitates deep analysis of news articles, enabling users to extract actionable insights with ease.

## Key Features
- **Dynamic URL Input**: Users can input multiple URLs of news articles they wish to analyze.
- **Interactive Query System**: Users can ask specific questions and receive insights derived from the analyzed articles, particularly useful in the financial domain.
- **Real-Time Interaction**: Powered by Streamlit, the tool offers a dynamic and responsive user interface.
- **Advanced NLP Capabilities**: Utilizes LangChain for robust natural language processing tasks.

## Technology Stack
- **OpenAI API**: Uses AI models for generating and interpreting text.
- **LangChain**: Manages complex chains of text processing tasks.
- **Streamlit**: Facilitates the frontend interface for user interactions.
- **FAISS**: Handles efficient similarity searches and clustering of dense vectors.
- **Python**: Primary programming language.

## Processing Architecture
### Document Handling and Query Processing
The tool processes documents through a series of steps to prepare them for interaction:

1. **Document Loading**: Documents are loaded into the system using the `UnstructuredURLLoader`.
2. **Text Splitting**: The documents are then split into manageable chunks using the `RecursiveTextSplitter`.

### Vector Database and Retrieval
Once the documents are split, the following steps are undertaken:

1. **Vectorization**: Each chunk is converted into vector form using LangChain's embedding capabilities.
2. **Vector DB Storage**: These vectors are stored in a `FAISS` database for efficient retrieval.

### Query and Retrieval
The retrieval process is as follows:

1. **Query Processing**: The system processes the user's query to find relevant chunks from the vector database.
2. **Chunk Retrieval**: Based on the query, relevant chunks are retrieved for further processing.

### Answer Generation
Using the retrieved chunks, the system generates an answer:

1. **Map-Reduce Method**: Each chunk is processed through individual LLMs to extract the most relevant information. The outputs are then combined and summarized.
2. **Final Response**: The final LLM generates the answer from the summarized chunks.

## Setup Instructions
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/CVM0410/Generative-AI-News-Research-Tool.git
   cd Generative-AI-News-Research-Tool
   ```
2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the Application**:
   ```bash
   streamlit run app.py
   ```

## Usage
After launching the tool:
1. **Input the OpenAI API Key**: Enter your OpenAI API key in the designated sidebar field.
2. **Enter Article URLs**: Add URLs for analysis.
3. **Process URLs**: Start the analysis by processing the URLs.
4. **Ask Questions**: Input questions to receive targeted insights based on the processed articles.

## Contributing
Contributions are welcome! Please read our contribution guidelines for more information on how to contribute to the project.

## License
This project is licensed under the MIT License. See [LICENSE.md](LICENSE.md) for details.
