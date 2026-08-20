# 🚀 SQLPilot

### AI-Powered Natural Language Database Query Assistant

SQLPilot is a full-stack application that allows users to interact with databases using plain English.

Instead of manually writing SQL queries, users can connect a database and ask questions such as:

> Show all customers who have placed an order

SQLPilot uses Google's Gemini AI to generate SQL, validates the generated query for safety, executes it on the connected database, and displays the results along with a simple explanation.

Currently, SQLPilot supports:

- MySQL
- PostgreSQL
- SQLite

---

## ✨ Features

### 🤖 Natural Language to SQL

Ask questions in plain English, and SQLPilot generates the corresponding SQL query.

Example:

```text
Show customer names and their order amounts
```

Example generated SQL:

```sql
SELECT c.name, o.total_amount
FROM customers c
JOIN orders o ON c.id = o.customer_id
```

---

### 🗄️ Multi-Database Support

SQLPilot supports multiple database systems:

- MySQL
- PostgreSQL
- SQLite

Users can connect, disconnect, and switch between supported databases.

---

### 🔌 Database Connection Management

SQLPilot provides database connection features including:

- Connect to a database
- Save database connections
- Reconnect previously saved connections
- Delete saved connections
- Disconnect the currently active database
- Check the current database connection status

---

### 🔒 Safe SQL Execution

SQLPilot is designed to allow only read-only database operations.

Only `SELECT` queries are allowed.

Write or destructive operations such as the following are blocked:

```text
INSERT
UPDATE
DELETE
DROP
ALTER
TRUNCATE
CREATE
GRANT
REVOKE
```

If a user requests an unsafe operation, SQLPilot returns an error instead of executing the query.

---

### 🧠 Schema-Aware SQL Generation

Before generating SQL, SQLPilot uses the schema of the connected database.

The AI is instructed to:

- Use only existing tables
- Use only existing columns
- Respect primary key relationships
- Respect foreign key relationships
- Avoid guessing table names
- Avoid guessing column names

This helps improve the reliability of generated SQL.

---

### ⚠️ Invalid Table and Column Handling

SQLPilot handles invalid requests such as:

```text
Show all employees
```

when an `employees` table does not exist.

It also handles requests for columns that do not exist.

Instead of executing invalid SQL, SQLPilot returns meaningful error messages.

---

### 📊 Dynamic Query Results

After successful execution, SQLPilot displays:

- Generated SQL
- SQL explanation
- Number of rows returned
- Dynamic result columns
- Query results in a table

If a query executes successfully but returns no records, SQLPilot displays a dedicated **No records found** state.

---

### 💡 SQL Explanation

After generating and executing SQL, SQLPilot uses AI to provide a simple explanation of what the generated query does.

For example:

> This query retrieves the names of customers along with their corresponding order amounts by combining the customers and orders tables using a JOIN.

This makes the application more useful for users who may not be familiar with SQL.

---

### 📜 Query History

SQLPilot stores successfully executed queries.

Each history entry includes:

- User question
- Generated SQL
- Query execution context

Query history is isolated based on the connected database.

For example:

- MySQL queries do not appear in PostgreSQL history
- PostgreSQL queries do not appear in SQLite history
- SQLite queries do not appear in MySQL history

Users can also reuse a previous question using the **Use Query** feature.

---

### 🔄 Multi-Database Switching

SQLPilot correctly switches the active:

- Database engine
- Database schema
- Connection ID
- Connection status
- Query history context

This allows users to move between MySQL, PostgreSQL, and SQLite databases during the same application session.

---

## 🛠️ Tech Stack

### Frontend

- Next.js
- React
- TypeScript
- Tailwind CSS
- Axios

### Backend

- Python
- FastAPI
- Pydantic
- SQLAlchemy

### AI

- Google Gemini API

### Supported Databases

- MySQL
- PostgreSQL
- SQLite

---

## ⚙️ How It Works

The SQLPilot query flow is:

```text
User Question
      ↓
Database Schema
      ↓
Gemini AI
      ↓
Generated SQL
      ↓
SQL Safety Validation
      ↓
Database Execution
      ↓
Query Results
      ↓
AI SQL Explanation
      ↓
Query History
```

### Detailed Flow

1. The user connects a supported database.
2. SQLPilot retrieves and stores the database schema.
3. The user asks a question in plain English.
4. The schema and user question are sent to Gemini.
5. Gemini generates SQL based on the available schema.
6. SQLPilot checks the generated SQL for safety.
7. Only valid read-only queries are allowed to execute.
8. SQLAlchemy executes the query on the active database.
9. Results are returned to the frontend.
10. Gemini generates a simple explanation of the SQL.
11. The successful query is saved to the history of the active database.

---

## 🔒 Safety Features

SQLPilot includes multiple layers of protection.

### AI-Level Restrictions

Gemini is instructed to:

- Generate SQL only
- Use only tables from the connected schema
- Use only existing columns
- Respect database relationships
- Allow only `SELECT` queries
- Return specific responses for invalid tables and columns
- Reject unsafe write or destructive requests

### Application-Level SQL Validation

Generated SQL is validated before execution.

Unsafe queries are blocked before reaching the database.

### Database Context Validation

SQLPilot ensures that a database connection and active connection ID exist before executing a query.

---

## 🧪 Tested Functionality

The following features were tested during development.

### Database Functionality

- [x] MySQL connection
- [x] PostgreSQL connection
- [x] SQLite connection
- [x] Database status
- [x] Disconnect
- [x] Saved connections
- [x] Reconnect saved connections
- [x] Delete saved connections
- [x] Multi-database switching

### Query Functionality

- [x] Simple SELECT queries
- [x] JOIN queries
- [x] Aggregate queries
- [x] No-result queries
- [x] Invalid table handling
- [x] Invalid column handling
- [x] Unsafe query blocking

### AI Features

- [x] Natural language to SQL generation
- [x] Schema-aware SQL generation
- [x] SQL explanation

### Query History

- [x] Save successful queries
- [x] Database-specific history isolation
- [x] Use previous query
- [x] Show all queries

### User Interface

- [x] Responsive testing
- [x] Dynamic query results table
- [x] Error states
- [x] No records found state

---

## 📸 Screenshots

### Home Page

> Add a screenshot of the SQLPilot home page here.

### Connect Database

> Add a screenshot showing MySQL, PostgreSQL, and SQLite connection options here.

### Query Workspace

> Add a screenshot showing generated SQL, explanation, and query results here.

### Query History

> Add a screenshot showing saved queries and the Use Query feature here.

---

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd sqlpilot
```

---

### 2. Backend Setup

Navigate to the backend directory:

```bash
cd backend
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment.

#### Windows

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```env
GEMINI_API_KEY=your_gemini_api_key
```

Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

The backend will run on:

```text
http://127.0.0.1:8000
```

---

### 3. Frontend Setup

Open another terminal and navigate to the frontend directory:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

Open:

```text
http://localhost:3000
```

---

## 🔑 Environment Variables

Create a `.env` file inside the backend directory:

```env
GEMINI_API_KEY=your_gemini_api_key
```

**Important:** Never commit your `.env` file or API key to GitHub.

---

## 🌐 API Overview

### Database APIs

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/database/connect` | Connect to a database |
| `GET` | `/api/database/saved` | Get saved connections |
| `DELETE` | `/api/database/saved/{connection_id}` | Delete a saved connection |
| `POST` | `/api/database/reconnect/{connection_id}` | Reconnect a saved database |
| `POST` | `/api/database/disconnect` | Disconnect the active database |
| `GET` | `/api/database/status` | Get active connection status |

### Query APIs

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/query/generate` | Generate and execute SQL from a natural language question |

### History APIs

SQLPilot also provides APIs for retrieving database-specific query history.

---

## 🎯 Example Usage

### User Question

```text
Show all customers
```

### Generated SQL

```sql
SELECT id, name, email FROM customers
```

---

### User Question

```text
Show customer names and their order amounts
```

### Generated SQL

```sql
SELECT c.name, o.total_amount
FROM customers c
JOIN orders o ON c.id = o.customer_id
```

---

### User Question

```text
Show the total amount of all orders
```

SQLPilot generates an aggregate query and displays the result.

---

## 🔮 Future Improvements

Possible future enhancements include:

- User authentication
- Role-based access control
- Support for additional databases
- Query export to CSV
- Downloadable query history
- Advanced SQL query visualization
- Database schema visualization
- Conversation-based query context
- Query optimization suggestions
- Production deployment
- Docker support

---

## 👨‍💻 Author

**Keerthan Poojari**

Built as a full-stack project for learning and demonstrating:

- Full-stack development
- REST API development
- Database connectivity
- Multi-database support
- Generative AI integration
- SQL validation and safety
- Query execution
- Responsive UI development

---

## ⭐ Project Summary

SQLPilot demonstrates how Generative AI can simplify database interaction by allowing users to query structured databases using natural language.

The application combines:

**AI + Database Connectivity + SQL Validation + Multi-Database Support + Full-Stack Development**

to provide a safe and user-friendly database querying experience.