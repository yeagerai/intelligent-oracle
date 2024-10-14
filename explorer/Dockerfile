FROM node:21.7.3-alpine3.20 AS base

WORKDIR /app
COPY package.json package-lock.json ./
RUN --mount=type=cache,target=/root/.npm npm ci
COPY . .

ENTRYPOINT ["npm", "run", "dev", "--", "--host", "--debug"]
