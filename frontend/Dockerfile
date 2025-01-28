# Use Node.js as base image
FROM node:18

# Set the working directory in the container
WORKDIR /app

# Copy package.json and install dependencies
COPY /app/package.json .
RUN npm cache clean --force
RUN npm install -g @angular/cli
RUN npm install

# Copy the application files
COPY . /app/
EXPOSE 3000

# Command to run the application
RUN chmod +x start.sh
CMD ["npm", "start"]