FROM node:18-alpine

RUN mkdir /app
WORKDIR /app

COPY package.json .
COPY package-lock.json .
COPY index.js .

# RUN chown -R node:node .
#
# USER node

RUN npm install
RUN ls

CMD [ "node", "index.js" ]
