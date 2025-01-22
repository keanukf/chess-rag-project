# Local Chess Chatbot Web Application

This is a local chess chatbot web application designed to answer questions about chess.com games. The application employs a Retrieval-Augmented Generation (RAG) approach using a LangChain agent to translate user queries into SQL queries for retrieving relevant data.

![Chatbot Demo](assets/chatbot_demo.png)

## Project Structure

The project consists of two main components:

1. **Backend**: The backend is responsible for handling the logic of translating user queries into SQL queries and retrieving relevant data from the database. It uses a LangChain agent and various tools to achieve this.

2. **Frontend**: The frontend is built using Next.js and provides a user interface for interacting with the chatbot. Users can input their queries and receive responses from the chatbot.

### Repository Structure Overview

The repository is organized into two main components: the **Backend** and the **Frontend**. Each component has its own directory and is responsible for different parts of the application.

#### 1. **Backend**
- **Purpose**: The backend handles the logic of translating user queries into SQL queries and retrieving relevant data from the database. It uses a LangChain agent and various tools to achieve this.
- **Key Files**:
  - `langchain_sql_agent.py`: This is likely the main script that runs the backend server and handles the query translation and data retrieval.
  - `requirements.txt`: Contains the list of Python dependencies needed for the backend.

#### 2. **Frontend**
- **Purpose**: The frontend is built using Next.js and provides a user interface for interacting with the chatbot. Users can input their queries and receive responses from the chatbot.
- **Key Files**:
  - `package.json`: Manages the dependencies and scripts for the frontend.
  - `.next/`: This directory is typically used by Next.js to store build artifacts and other runtime data.
  - `node_modules/`: Contains all the npm packages required for the frontend.

### Additional Files and Directories

- **Docker Configuration**: The repository uses Docker Compose to manage and run both the backend and frontend services. This is indicated by the instructions in the `README.md` for using Docker Compose to build and start the services.

- **.gitignore Files**: There are `.gitignore` files in both the root and frontend directories to exclude certain files and directories from being tracked by Git. For example, `node_modules/` and `.env` files are ignored.

- **Documentation and Licenses**: The repository includes various documentation files and licenses, such as the `LICENSE` file, which contains the Apache License 2.0, and other documentation files related to dependencies and tools used in the project.

### Folder Structure

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

### Running Backend and Frontend Separately

#### Backend

1. Navigate to the backend directory:
    ```bash
    cd backend
    ```

2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Run the backend server:
    ```bash
    python langchain_sql_agent.py
    ```

#### Frontend

1. Navigate to the frontend directory:
    ```bash
    cd frontend
    ```

2. Install the required dependencies:
    ```bash
    npm install
    # or
    yarn install
    # or
    pnpm install
    # or
    bun install
    ```

3. Run the development server:
    ```bash
    npm run dev
    # or
    yarn dev
    # or
    pnpm dev
    # or
    bun dev
    ```

4. Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

## Learn More

To learn more about the technologies used in this project, take a look at the following resources:

- [Next.js Documentation](https://nextjs.org/docs) - learn about Next.js features and API.
- [LangChain Documentation](https://langchain.com/docs) - learn about LangChain and its capabilities.
- [Docker Documentation](https://docs.docker.com/) - learn about Docker and Docker Compose.

## Deploy on Vercel

The easiest way to deploy your Next.js app is to use the [Vercel Platform](https://vercel.com/new?utm_medium=default-template&filter=next.js&utm_source=create-next-app&utm_campaign=create-next-app-readme) from the creators of Next.js.

Check out our [Next.js deployment documentation](https://nextjs.org/docs/app/building-your-application/deploying) for more details.
