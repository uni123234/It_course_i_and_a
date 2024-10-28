FROM node:16

WORKDIR /app

COPY package*.json .
RUN npm install --force
RUN npm i --save-dev @types/react-facebook-login --force

COPY . .

RUN mkdir -p /app/node_modules && chown -R node:node /app

USER node

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host"]
