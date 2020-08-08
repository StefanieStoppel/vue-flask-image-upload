FROM node:slim as FRONTEND_BUILD
WORKDIR /client

# Copy frontend sources
COPY client ./

RUN yarn install
RUN yarn build


FROM python:3.7-slim
ENV UPLOAD_PATH="/app/data"

# Create /app/server directory
WORKDIR /app/server

# Install app dependencies
COPY server/requirements.txt ./
RUN pip install -r requirements.txt

# Bundle app source
COPY server ./
COPY --from=FRONTEND_BUILD /server/static ./static

EXPOSE 5000

CMD [ "/bin/bash", "-c", "python app.py --upload_path ${UPLOAD_PATH}" ]