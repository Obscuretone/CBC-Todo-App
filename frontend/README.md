# CBC Todo Frontend

React frontend for the CBC Todo prototype.

## Local Development

From the repository root:

```bash
cp frontend/.env.example frontend/.env
docker compose up --build frontend
```

Or run it directly:

```bash
cd frontend
npm install
cp .env.example .env
npm start
```

The app listens on `http://localhost:3000`.

## Notes

This frontend currently uses Azure/MSAL for login. The backend auth flow still expects app-issued JWTs, so auth needs a follow-up pass before the app is fully usable end to end.
