

**Multi-AI Agent: Intelligent Question Answering**

**What it does:** This application answers user questions by combining web search and database querying. It utilizes a multi-agent system powered by the Qwen2.5 language model (via Ollama) to understand the user's intent, search the web for relevant information, and query databases using SQL.

**How it works:**

* **User Input:** The user asks a question.
* **Language Model (Qwen2.5):** The model interprets the question and determines the best course of action (web search or database query).
* **Web Search (Tavily API):** If necessary, the agent uses the Tavily Search API to find relevant information online.
* **Text-to-SQL:** If a database query is required, the agent translates the user's question into SQL.
* **Response Generation:** The agent compiles the results from the web search and/or database query and generates a clear, concise answer for the user.
* **Technology:** This system is built using LangGraph for agent orchestration, Streamlit for the user interface, and LangSmith for monitoring and evaluation.

**Key Features:**

* Combines web search and database querying for comprehensive answers.
* Uses the powerful Qwen2.5 language model for natural language understanding.
* Provides a user-friendly interface with Streamlit.
* Utilizes LangGraph to create a multi agent workflow.
* Uses Ollama to locally run the Qwen2.5 model.


WebSearch Agent
![Screenshot 2025-02-26 210720](https://github.com/user-attachments/assets/44a1be8b-bd87-4766-8bf9-db60ca41c0ba)

Text-To-SQL Agent
![Screenshot 2025-02-26 000104](https://github.com/user-attachments/assets/302ce9ac-6991-424c-a45e-4b043b84082e)

LangFuse Dashboard
![Screenshot 2025-03-04 021030](https://github.com/user-attachments/assets/86c63953-0966-4837-9411-d93a6b648971)

