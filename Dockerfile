# This is a multi-stage Docker build for the Trancendos Ecosystem.

# The first stage builds the frontend application.
FROM node:18-alpine AS frontend-builder
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm ci --only=production
COPY frontend/ .
RUN npm run build

# The second stage builds the Java backend application.
FROM openjdk:11-jre-slim AS java-builder
WORKDIR /app/backend/java
COPY backend/java/target/*.jar app.jar

# The third stage builds the Python backend application.
FROM python:3.9-slim AS python-builder
WORKDIR /app/backend/python
COPY backend/python/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/python/ .

# The final stage creates the production image.
FROM nginx:alpine
# Copy the built frontend application from the frontend-builder stage.
COPY --from=frontend-builder /app/frontend/build /usr/share/nginx/html
# Copy the Nginx configuration file.
COPY nginx/nginx.conf /etc/nginx/nginx.conf
# Expose port 80 to the outside world.
EXpose 80
# Start Nginx when the container starts.
CMD ["nginx", "-g", "daemon off;"]
