FROM node:16-bookworm

WORKDIR /app/

USER root

ARG PDT_WEB_PORT=3000
COPY package*.json ./
RUN npm ci --no-optional --quiet 1>/dev/null

COPY . .

ENV POSTGRES_HOST=$DATABASE
ENV PORT=$PDT_WEB_PORT
EXPOSE $PORT
CMD ["npm", "run", "dev"]