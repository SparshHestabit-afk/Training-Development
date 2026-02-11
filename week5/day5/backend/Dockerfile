FROM node:20-alpine

WORKDIR /todo-backend

COPY package*.json ./
RUN npm install

COPY . .

EXPOSE 5000

CMD ["npm", "start"]