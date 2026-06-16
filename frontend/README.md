# CBC Todo Frontend

React frontend for the CBC Todo prototype.

## Local Development

From the repository root:

```bash
docker compose up --build frontend
```

Or run it directly:

```bash
cd frontend
npm install
cp .env.example .env
npm start
```

The app listens on `http://localhost:3000` and expects the API at `VITE_API_URL`, defaulting to `http://localhost:8000`.
