# Use Node.js as base image
FROM node:18

# Set the working directory in the container
WORKDIR /app

# Copy package.json and install dependencies
COPY package.json .
RUN npm install

# Copy the application files
COPY . .
# Build the React app
RUN npm run build

RUN npm install -g serve
EXPOSE 3000

# Command to run the application
CMD ["serve", "-s", "build", "-l", "3000"]