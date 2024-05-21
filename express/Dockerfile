FROM node:18-alpine

WORKDIR /app

COPY package*.json /app
COPY .env /app

RUN chown -R node:node /app

USER node

RUN npm install

COPY --chown=node:node . /app


CMD [ "node", "index.js" ]
