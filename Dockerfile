# Multi-stage Docker build for Trancendos Ecosystem
FROM node:18-alpine AS frontend-builder
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm ci --only=production
COPY frontend/ .
RUN npm run build

FROM openjdk:11-jre-slim AS java-builder
WORKDIR /app/backend/java
COPY backend/java/target/*.jar app.jar

FROM python:3.9-slim AS python-builder
WORKDIR /app/backend/python
COPY backend/python/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/python/ .

# Production image
FROM nginx:alpine
COPY --from=frontend-builder /app/frontend/build /usr/share/nginx/html
COPY nginx/nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]