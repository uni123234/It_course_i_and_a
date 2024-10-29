FROM node:16 AS build

WORKDIR /app

COPY package*.json .

RUN npm install --force && \
    npm i --save-dev @types/react-facebook-login --force

COPY . .

RUN chown -R node:node /app/node_modules

RUN mkdir -p /app/node_modules

USER node

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host"]
