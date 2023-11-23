# Archive Binge Recoded

[![Pytest (API)](https://github.com/Respheal/ab-api-poc/actions/workflows/python-app.yml/badge.svg)](https://github.com/Respheal/ab-api-poc/actions/workflows/python-app.yml) [![Playwright (Frontend)](https://github.com/Respheal/ab-api-poc/actions/workflows/playwright.yml/badge.svg)](https://github.com/Respheal/ab-api-poc/actions/workflows/playwright.yml) [![codecov (API)](https://codecov.io/gh/Respheal/ab-api-poc/graph/badge.svg?token=ITKPPU0K2A)](https://codecov.io/gh/Respheal/ab-api-poc)

## API

The API is a FastAPI application. In production, it uses PostgreSQL and Celery to process requests and store data. In local development, the database is replaced with SQLite.

### Getting Started

Launch the API locally by installing all dependencies and running uvicorn:

````bash
cd api
poetry install
uvicorn api.app.main:app --reload```

### Learn More

-   [FastAPI](https://fastapi.tiangolo.com/)

## Frontend

This is a [Next.js](https://nextjs.org/) project bootstrapped with [`create-next-app`](https://github.com/vercel/next.js/tree/canary/packages/create-next-app).

### Getting Started

Install dependencies and run the development server:

```bash
npm install
npm run dev
````

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result. Pages and components live in frontend/src/app.

### Learn More

To learn more about the packages used, take a look at the following resources:

-   [Next.js Documentation](https://nextjs.org/docs)
-   [Learn Next.js](https://nextjs.org/learn)
-   [React Bootstrap](https://react-bootstrap.github.io/docs/getting-started/introduction)
-   [Axios](https://axios-http.com/docs/intro)

### Deploy

Check out our [Next.js deployment documentation](https://nextjs.org/docs/deployment) for more details.

### Notes:

-   Have poetry installed (via pipx)
-   cd api, poetry install
-   cd frontend, npm install
-   install Playwright browsers:
    -- npx playwright install chromium firefox webkit // I had a hiccup at this step, not convinced playwright fully installed?
