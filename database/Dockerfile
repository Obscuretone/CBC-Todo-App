# Database Dockerfile (MariaDB)
FROM mariadb:latest

# Set environment variables (for local development)
ENV MYSQL_ROOT_PASSWORD=root
ENV MYSQL_DATABASE=cbc_todo
ENV MYSQL_USER=todo_user
ENV MYSQL_PASSWORD=todo_pass

# Copy init SQL file for seeding the database
COPY init.sql /docker-entrypoint-initdb.d/