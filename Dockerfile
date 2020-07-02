FROM python:3.7-slim

ENV UPLOAD_PATH="/app/data"

# Create app directory
WORKDIR /app

# Install app dependencies
COPY server/requirements.txt ./

RUN pip install -r requirements.txt

# Bundle app source
COPY server /app

EXPOSE 5000

CMD [ "/bin/bash", "-c", "python app.py --upload_path ${UPLOAD_PATH}" ]