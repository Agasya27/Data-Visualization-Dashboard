# Build stage
FROM node:18-alpine AS build
WORKDIR /app

# Install deps
COPY package.json package-lock.json* pnpm-lock.yaml* yarn.lock* ./
RUN npm ci || npm install

# Copy source and build; allow API URL override at build time
COPY . .
ARG VITE_API_URL
ENV VITE_API_URL=${VITE_API_URL}
RUN npm run build

# Serve stage
FROM nginx:alpine
WORKDIR /usr/share/nginx/html
COPY --from=build /app/dist .
# Basic SPA fallback and gzip
COPY ./nginx.conf /etc/nginx/conf.d/default.conf
# Ensure Nginx listens on $PORT provided by Railway
ENV PORT=80
EXPOSE 80
CMD ["sh", "-c", "sed -i \"s/__PORT__/${PORT:-80}/\" /etc/nginx/conf.d/default.conf && nginx -g 'daemon off;' "]
