FROM node:20-bookworm-slim

WORKDIR /app/

USER root

COPY package*.json ./
RUN npm install

COPY . .

EXPOSE 3000
CMD ["npm", "run", "dev"]