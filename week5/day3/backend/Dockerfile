FROM node:20-alpine

WORKDIR /week5-day3-app

# Install curl
RUN apk add --no-cache curl

COPY package*.json ./
RUN npm install

COPY . .

EXPOSE 3000

CMD [ "npm", "start" ]