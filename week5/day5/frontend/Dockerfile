#building stage
FROM node:20-alpine AS builder

WORKDIR /todo-frontend

COPY package*.json ./
RUN npm install

COPY . .

RUN npm run build

#production stage
FROM node:20-alpine

WORKDIR /todo-frontend

COPY --from=builder /todo-frontend ./

EXPOSE 3000

CMD ["npm", "start"]