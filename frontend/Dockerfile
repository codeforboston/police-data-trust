FROM node:16.12.0-buster

WORKDIR /app/

USER root

COPY package*.json ./
RUN npm ci --no-optional --quiet 1>/dev/null

COPY . .

ENV POSTGRES_HOST=$DATABASE
ENV PORT=3000
EXPOSE $PORT
CMD ["npm", "run", "dev"]