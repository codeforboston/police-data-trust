#Copied from Original Dockerfile

FROM node:20-bookworm-slim

WORKDIR /app/

USER root

ARG NPDI_WEB_PORT=3000
COPY package*.json ./
RUN npm ci --no-optional --quiet 1>/dev/null

COPY . .

# ENV POSTGRES_HOST=$DATABASE
ENV PORT=$NPDI_WEB_PORT
EXPOSE $PORT
CMD ["npm", "run", "dev"]