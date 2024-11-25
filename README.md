# Chess RAG Project

This project is a Flask-based application designed to answer questions using a language model and a SQL database.

## Prerequisites

- Python 3.8+
- Docker (optional, if using Docker for deployment)

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/yourusername/chess-rag-project.git
   cd chess-rag-project
   ```

2. **Create a virtual environment**:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

## Configuration

1. **Set up environment variables**:

   Create a `.env` file in the root directory and add necessary environment variables, such as database credentials and API keys.

2. **Database setup**:

   Ensure your database is running and accessible. Update the database connection string in your configuration.

## Running the Application

1. **Start the Flask app**:

   ```bash
   python app/main.py
   ```

   The application will start on `http://localhost:8080` by default.

2. **Using Docker (optional)**:

   If you prefer to use Docker, build and run the Docker container:

   ```bash
   docker build -t chess-rag-app .
   docker run -p 8080:8080 chess-rag-app
   ```

## Testing the Application

1. **Health Check**:

   Verify the application is running by accessing the health check endpoint:

   ```bash
   curl http://localhost:8080/health
   ```

   You should receive a response indicating the application is healthy.

2. **Query Endpoint**:

   Test the query functionality by sending a POST request:

   ```bash
   curl -X POST http://localhost:8080/query \
   -H "Content-Type: application/json" \
   -d '{"query": "What is the capital of France?"}'
   ```

   You should receive a JSON response with the answer.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## Repository Structure

```
chess-rag-project/
│
├── app/                    # Main application directory
│   ├── __init__.py         # Initializes the Flask app
│   ├── main.py             # Entry point for the Flask application
│   └── langchain_rag.py    # Script for using Langchain to answer questions
│
├── data/                   # Directory for data processing scripts and raw data
│   ├── chess_data_processor.py  # Script for processing chess data
│   └── chesscom_data_extraction.py  # Script for extracting data from Chess.com
│   ├── chess_games_raw.csv  # Raw data from Chess.com
│   ├── chess_games_simple.csv  # Processed data from Chess.com
│
├── tests/                  # Directory for test cases
│   └── test_gc_mysql.py  # Tests for the connection to the MySQL database
│
├── Dockerfile              # Docker configuration for containerizing the app
├── environment.yml         # Conda environment configuration file
├── .env.example            # Example environment variables file (to be implemented)
├── .gitignore              # Git ignore file
├── .gcloudignore           # Google Cloud ignore file
└── README.md               # Project documentation
```

## License

This project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for details.
