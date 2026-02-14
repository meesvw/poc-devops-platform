FROM alpine:3.23

# Install updates
RUN apk update

# Install required packages
RUN apk add --no-cache nginx

# Expose port 80 of the container image
EXPOSE 80 443

# Set image start command
CMD ["nginx", "-g", "daemon off;"]
