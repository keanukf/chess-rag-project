# Local Chess Chatbot Web Application

This is a local chess chatbot web application designed to answer questions about chess.com games. The application employs a Retrieval-Augmented Generation (RAG) approach using a LangChain agent and a VertexAI LLM engine to translate user queries into SQL queries for retrieving relevant data.

![Chatbot Demo](assets/chatbot_demo.png)

## Application Architecture

The project is a local chess chatbot web application with a multi-tier architecture comprising a frontend, a backend, and a cloud inference layer. 

- **Frontend**: Developed using Next.js, it provides a user-friendly interface for interacting with the chatbot. Users can input queries and receive responses, facilitating seamless communication with the backend.

- **Backend**: Built using a Flask application, it leverages LangChain for query processing and translates these queries into SQL commands to interact with a local SQLite database, which stores chess data. The backend also integrates with Google VertexAI to enhance query processing with advanced AI capabilities.

- **Cloud Inference Layer**: Utilizes Google VertexAI as a cloud inference provider to process and enhance user queries with sophisticated AI models.

This architecture allows for efficient data retrieval and processing, combining local and cloud resources to deliver a robust chatbot experience.

![Application Architecture](assets/application_architecture.svg)

### 1. **Backend**

- **Purpose**: The backend handles the logic of translating user queries into SQL queries and retrieving relevant data from the database. It uses a LangChain agent and various tools to achieve this.
- **Key Files**:
  - `data/chesscom_data_extraction.py`: This file contains the code for extracting data from chess.com. It is included in the repository for reference and can be used to extract data from chess.com.
  - `data/chess_data_processor.py`: This file contains the code for processing the extracted data. Also included in the repository for reference and can be used to process and prepare the extracted data.
  - `data/chess_rag.db`: This file contains the SQLite database for storing the processed data.
  - `langchain_sql_agent.py`: This is likely the main script that runs the backend server and handles the query translation and data retrieval.
  
### 2. **Frontend**

- **Purpose**: The frontend is built using Next.js and provides a user interface for interacting with the chatbot. Users can input their queries and receive responses from the chatbot.
- **Key Files**:
  - `/components/Chat.tsx`: This is the main component that handles the chat interface and interaction with the backend.
  - `/components/Message.tsx`: This component represents a single message in the chat interface.
  - `/components/GMBar.tsx`: This component represents the game mode bar in the chat interface.

## Folder Structure

Here is a comprehensive tree of the folder structure with short descriptions:

```
/chess-rag-project
│
├── backend
│   ├── Dockerfile                   # Dockerfile for building the backend
│   ├── environment.yml              # Environment file for Conda
│   ├── data
│   │   ├── chess_data_processor.py      # Script for processing chess data
│   │   ├── chess_games_raw.csv          # Raw chess data extracted from chess.com
│   │   ├── chess_games_simple.csv       # Processed chess data for simpler queries
│   │   ├── chess_rag.db                 # SQLite database for storing chess data
│   │   └── chesscom_data_extraction.py  # Script for extracting data from chess.com
│   │
│   ├── langchain_sql_agent.py           # Main backend script for query translation and data retrieval
│   ├── main.py                          # Main backend script for query translation and data retrieval
│   └── requirements.txt                 # Python dependencies for the backend
│
├── frontend
│   ├── app/                           # Application code for the frontend
│   ├── components/                    # Reusable UI components
│   ├── lib/                           # Library code for the frontend
│   ├── public/                        # Static assets for the frontend
│   ├── tailwind.config.js             # Tailwind CSS configuration
│   └── tsconfig.json                  # TypeScript configuration
│
├── assets
│   └── chatbot_demo.png               # Preview image of the chatbot demo
│
├── docker-compose.yml          # Docker Compose configuration for managing services
├── .gitignore                  # Git ignore rules for the root directory
└── LICENSE                     # License information for the project
```

## Getting Started

### Running the Application

You can start the backend and frontend components separately or at once using Docker Compose.

### Using Docker Compose

To start both the backend and frontend at once, use Docker Compose. Ensure you have Docker and Docker Compose installed on your machine.

1. Build and start the services:
    ```bash
    docker-compose up --build
    ```

2. Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

### Running Backend and Frontend Separately without Docker

#### Backend

1. Navigate to the backend directory:
    ```bash
    cd backend
    ```

2. Create a new Conda environment using the `environment.yml` file:
    ```bash
    conda env create -f environment.yml
    ```

3. Activate the Conda environment:
    ```bash
    conda activate chessbot
    ```

4. Run the backend server:
    ```bash
    python -m main
    ```

#### Frontend

1. Navigate to the frontend directory:
    ```bash
    cd frontend
    ```

## Google Cloud Credentials Setup

To enable the backend to interact with Google VertexAI, you need to create and embed a Google Cloud JSON credential file with the minimum required permissions.

### Steps to Create and Embed Google Cloud Credentials

1. **Create a Google Cloud Project**:
   - Go to the [Google Cloud Console](https://console.cloud.google.com/).
   - Create a new project or select an existing project.

2. **Enable Vertex AI API**:
   - In the Google Cloud Console, navigate to the "APIs & Services" dashboard.
   - Click on "Enable APIs and Services" and search for "Vertex AI".
   - Enable the Vertex AI API for your project.

3. **Create a Service Account**:
   - Go to the "IAM & Admin" section in the Google Cloud Console.
   - Click on "Service Accounts" and then "Create Service Account".
   - Provide a name and description for the service account.

4. **Assign Permissions**:
   - After creating the service account, click on it to open its details.
   - Go to the "Permissions" tab and click "Add Member".
   - Assign the role `Vertex AI User` (roles/aiplatform.user) to the service account.

5. **Create and Download JSON Key**:
   - In the service account details, go to the "Keys" tab.
   - Click "Add Key" and select "JSON" to create and download the key file.
   - Save this JSON file securely, as it contains sensitive information.

6. **Embed the Credential in Your Application**:
   - Place the JSON key file in a secure location within your project directory.
   - Set the `GOOGLE_APPLICATION_CREDENTIALS` environment variable to the path of the JSON key file. This can be done by adding the following line to your environment setup script or terminal session:
     ```bash
     export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service-account-file.json"
     ```

By following these steps, you will have set up the necessary credentials to allow your application to interact with Google VertexAI securely.