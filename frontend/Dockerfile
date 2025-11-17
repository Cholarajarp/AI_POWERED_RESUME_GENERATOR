FROM node:20-alpine
WORKDIR /app
COPY package.json package-lock.json* ./
ARG CACHE_BUSTER=1
RUN npm install
COPY . .
CMD ["./node_modules/.bin/vite", "--host"]
