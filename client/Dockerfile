FROM node:18-alpine
WORKDIR /app

RUN mkdir node_modules
COPY package.json .
RUN npm install

COPY . .

CMD ["npm", "run", "dev"]

