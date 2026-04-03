FROM node:20-alpine

WORKDIR /week5-app

COPY package*.json ./
RUN npm install

COPY . .

EXPOSE 3000

CMD ["node","app.js"]
