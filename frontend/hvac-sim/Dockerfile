# Use Node.js as base image
FROM node:latest as build

# Set the working directory in the container
WORKDIR /app

# Copy package.json and install dependencies
COPY package*.json ./
#run clean install of dependencies
RUN npm ci

#RUN npm cache clean --force

RUN npm install -g @angular/cli

# Copy the application files
COPY . .

# Build the application
RUN npm run build --configuration=production

# Use Nginx as base image
FROM nginx:latest

# Copy the build output to replace the default nginx contents
COPY ./nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist/hvac-sim/browser /usr/share/nginx/html

EXPOSE 3000

# Command to run the application
#RUN chmod +x start.sh
#CMD ["ng", "serve", "--host", "0.0.0.0:8082"]

#Build: docker build -t hvac-frontend-nodejs .
#Run: docker run -d -p 8080:3000 hvac-frontend-nodejs