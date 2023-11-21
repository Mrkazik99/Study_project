FROM node:18-alpine

EXPOSE 3000

WORKDIR /react-docker-example/

COPY public/ /web_app/public
COPY src/ /web_app/src
COPY package.json /web_app/

RUN npm install

CMD ["npm", "start"]