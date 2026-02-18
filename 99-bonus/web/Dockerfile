FROM alpine:3.23

# Install updates
RUN apk update

# Install required packages
RUN apk add --no-cache nginx curl

# Create rootless user and group
RUN addgroup -S rootless-nginx-group && adduser -S rootless-nginx -G rootless-nginx-group

# Set file owner for the rootless group and user
RUN chown -R rootless-nginx:rootless-nginx-group /var/lib/nginx /var/log/nginx /run/nginx

# Switch to rootless user
USER rootless-nginx

# Expose port 80 of the container image
EXPOSE 80

# Set image start command
CMD ["nginx", "-g", "daemon off;"]
