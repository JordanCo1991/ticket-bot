# IT Ticket Automation Bot — Frontend
FROM nginx:alpine

LABEL maintainer="Jordan Cohen"
LABEL description="IT Ticket Bot — Frontend Dashboard"

# Remove default Nginx config
RUN rm /etc/nginx/conf.d/default.conf

# Copy custom config and HTML
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY index.html /usr/share/nginx/html/index.html

EXPOSE 80
