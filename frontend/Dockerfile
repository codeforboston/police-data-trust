FROM node:20-bookworm-slim

WORKDIR /app/

USER root

ARG NPDI_WEB_PORT=3000

COPY package*.json ./
RUN npm ci --no-optional --quiet 1>/dev/null

COPY . .

ENV NPDI_WEB_PORT=$NPDI_WEB_PORT
EXPOSE $NPDI_WEB_PORT
CMD ["npm", "run", "dev"]