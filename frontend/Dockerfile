FROM node:lts-buster

WORKDIR /usr/src/app

USER root

COPY frontend/package*.json /usr/src/app/
RUN npm install --no-optional --quiet 1>/dev/null

COPY .git/hooks/ .git/hooks/
RUN npm run prepare
COPY frontend/ ./

ENV POSTGRES_HOST=$DATABASE
ENV PORT=3000
EXPOSE $PORT
CMD ["npm", "run", "dev"]