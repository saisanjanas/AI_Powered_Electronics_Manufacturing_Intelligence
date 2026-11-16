# 🤖 AI Intelligence Manufacturing

> AI-powered intelligence platform for electronics manufacturing, production analysis, quality monitoring, maintenance insights, and manufacturing troubleshooting.

## 🚀 Overview

**AI Intelligence Manufacturing** is a Python-based AI platform designed to help engineers and manufacturing teams analyze production data and solve electronics manufacturing problems.

The system combines:

- Large Language Models (LLMs)
- Machine Learning
- Retrieval-Augmented Generation (RAG)
- Manufacturing datasets
- Technical documentation
- Data analytics

The goal is to provide a centralized intelligent assistant capable of answering manufacturing questions and generating actionable insights from production, quality, maintenance, sensor, and shift data.

---

## 🎯 Objectives

- Build an AI assistant specialized in electronics manufacturing
- Analyze production performance
- Monitor production targets
- Analyze machine sensor data
- Analyze manufacturing quality
- Identify production problems
- Analyze maintenance records
- Compare shift-wise performance
- Detect production anomalies
- Provide manufacturing troubleshooting recommendations
- Build a manufacturing knowledge base
- Use RAG for context-aware responses
- Support data-driven manufacturing decisions

---

## 🧠 AI Manufacturing Assistant

Users can interact with the system using natural language.

### Example Queries

```text
Why did production decrease during the night shift?

Which machines had the highest maintenance downtime?

Are we meeting today's production target?

Which production line has the highest defect rate?

What caused the increase in defective products?

What could be causing repeated machine failures?

Are abnormal sensor readings affecting production?
```

---

## 🏗️ Project Structure

```text
AI_Powered_Electronics_Manufacturing_Intelligence/
│
├── backend/
│   ├── src/
│   ├── .env.example
│   └── package.json
│
├── manufacturing-intelligence/
│   ├── src/
│   ├── .env.example
│   ├── package.json
│   └── vite.config.js
│
├── database/
│   ├── schema.sql
│   └── auth_tables.sql
│
├── electronics_manufacturing_db.sql
│
└── README.md
```

---

## 🛠️ Technologies Used

### Frontend
- React.js
- Vite
- React Router
- Recharts
- Lucide React
- Tailwind CSS

### Backend
- Node.js
- Express.js
- MySQL
- JWT Authentication
- bcryptjs

### AI and Machine Learning
- Python
- Machine Learning
- Large Language Models (LLMs)
- Retrieval-Augmented Generation (RAG)

### Development Environment
- Git and GitHub
- GitHub Codespaces
- MySQL Server

---

# ⚙️ Installation and Setup

Follow these steps to run the project after cloning the repository.

## 1. Clone the Repository

```bash
git clone https://github.com/saisanjanas/AI_Powered_Electronics_Manufacturing_Intelligence.git
```

Navigate into the project:

```bash
cd AI_Powered_Electronics_Manufacturing_Intelligence
```

You can also open the repository directly in GitHub Codespaces.

## 2. Install MySQL Server

For GitHub Codespaces running Ubuntu:

```bash
sudo apt update
sudo apt install mysql-server -y
```

Start the MySQL service:

```bash
sudo service mysql start
```

Verify that MySQL is running:

```bash
sudo mysql -e "SELECT VERSION();"
```

## 3. Create the Database

Create the manufacturing database:

```bash
sudo mysql -e "CREATE DATABASE electronics_manufacturing_db CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;"
```

## 4. Import the Manufacturing Dataset

Import the provided SQL dump:

```bash
sudo mysql electronics_manufacturing_db < electronics_manufacturing_db.sql
```

Verify the imported tables:

```bash
sudo mysql electronics_manufacturing_db -e "SHOW TABLES;"
```

The database contains manufacturing information such as:

- Production
- Production targets
- Quality
- Sensors
- Downtime
- Maintenance
- Machines
- Employees
- Inventory
- Suppliers
- Shifts

## 5. Create the Authentication Tables

The authentication system requires two additional tables:

- `users`
- `user_preferences`

Apply the authentication SQL file:

```bash
sudo mysql electronics_manufacturing_db < database/auth_tables.sql
```

Verify the tables:

```bash
sudo mysql electronics_manufacturing_db -e "SHOW TABLES;"
```

## 6. Create a MySQL Application User

Create a dedicated MySQL user for the backend instead of using the root account.

Open MySQL:

```bash
sudo mysql
```

Execute the following SQL commands:

```sql
CREATE USER 'bel_app'@'localhost' IDENTIFIED BY 'YOUR_STRONG_PASSWORD';

GRANT ALL PRIVILEGES ON electronics_manufacturing_db.* TO 'bel_app'@'localhost';

FLUSH PRIVILEGES;

EXIT;
```

Replace `YOUR_STRONG_PASSWORD` with your own secure password.

## 7. Configure the Backend

Navigate to the backend directory:

```bash
cd backend
```

Create your environment file:

```bash
cp .env.example .env
```

Open `backend/.env` and configure your database credentials:

```env
PORT=4000

DB_HOST=localhost
DB_PORT=3306
DB_USER=bel_app
DB_PASSWORD=YOUR_STRONG_PASSWORD
DB_NAME=electronics_manufacturing_db

DB_CONNECTION_LIMIT=10

JWT_SECRET=YOUR_LONG_RANDOM_SECRET
JWT_EXPIRES_IN=12h
BCRYPT_SALT_ROUNDS=10

ML_SERVICE_URL=http://localhost:8000
ML_SERVICE_TIMEOUT_MS=5000

CORS_ORIGINS=http://localhost:5173
```

Generate a secure JWT secret using:

```bash
openssl rand -hex 32
```

Copy the generated value into `JWT_SECRET`.

Install backend dependencies:

```bash
npm install
```

Start the backend:

```bash
npm run dev
```

The backend API runs on:

```text
http://localhost:4000
```

Keep this terminal running.

## 8. Configure the Frontend

Open a second terminal and navigate to the frontend directory from the repository root:

```bash
cd manufacturing-intelligence
```

Create the frontend environment file:

```bash
cp .env.example .env
```

Configure the frontend environment:

```env
VITE_API_BASE_URL=/api
VITE_USE_MOCKS=false
VITE_GRAFANA_BASE_URL=http://localhost:3000
```

Install frontend dependencies:

```bash
npm install
```

Start the frontend:

```bash
npm run dev
```

The frontend runs on:

```text
http://localhost:5173
```

In GitHub Codespaces, open the forwarded port **5173** to access the application in your browser.

The Vite development server forwards `/api` requests to the backend running on port 4000.

## 9. Access the Application

Once both servers are running:

1. Open the frontend URL in your browser.
2. Register a user account.
3. Log in using your registered credentials.
4. Explore the manufacturing dashboard and available features.

---

## 🔐 Authentication

The application uses JWT-based authentication.

- User registration
- User login
- Password hashing using bcryptjs
- Token-based authentication
- Protected API routes
- User preferences

User passwords are stored as hashes rather than plain text.

---

## 📊 Database Configuration

The application uses MySQL to store manufacturing and authentication data.

| Configuration | Value |
|---|---|
| Database | `electronics_manufacturing_db` |
| Database host | `localhost` |
| Database port | `3306` |
| Backend port | `4000` |
| Frontend port | `5173` |

The database is populated using the provided SQL dump and the additional authentication schema.

---

## 🧪 Troubleshooting

### MySQL Connection Refused

Make sure the MySQL service is running:

```bash
sudo service mysql start
```

### MySQL Access Denied

Check the database username and password in `backend/.env`.

Verify that the application user has privileges on `electronics_manufacturing_db`.

### Table Does Not Exist: users

Apply the authentication schema:

```bash
sudo mysql electronics_manufacturing_db < database/auth_tables.sql
```

### Frontend Cannot Connect to Backend

Check that:

- The backend is running on port `4000`.
- The frontend is running on port `5173`.
- `VITE_API_BASE_URL` is set to `/api`.
- The Vite proxy configuration is present in `manufacturing-intelligence/vite.config.js`.

### Internal Server Error

Check the backend terminal for the error message and verify the database connection and environment variables.

---

## 🔒 Security Notes

- Never commit `.env` files.
- Never expose database passwords or JWT secrets.
- Use `.env.example` as a configuration template.
- Generate your own JWT secret.
- Use a dedicated database user instead of the MySQL root account.
- Do not share database credentials publicly.

---

## ▶️ Running the Project

For normal development, keep two terminals open.

**Terminal 1 — Backend**

```bash
cd backend
npm run dev
```

**Terminal 2 — Frontend**

```bash
cd manufacturing-intelligence
npm run dev
```

Both applications should be running for the complete frontend and backend experience.

---

## 👩‍💻 Contributors

Developed as an AI-powered electronics manufacturing intelligence project.
