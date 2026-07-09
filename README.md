# Setting up
```
cd backend_service
uv sync
```

```
cd frontend_service
npm install
```

To start the project, run this on two terminal instances. (We should probably run these concurrently in one terminal instance.)
```
cd backend_service
uv run fastapi dev
```

```
cd frontend_service
npm run dev
```
