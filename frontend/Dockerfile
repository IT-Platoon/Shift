FROM node:18

WORKDIR /frontend

ENV PATH /frontend/node_modules/.bin:$PATH

COPY package*.json ./

RUN npm install
RUN npm install @vue/cli@latest -g

COPY . .