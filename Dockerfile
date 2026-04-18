FROM python:3.10-slim

# Install Poetry
ENV POETRY_VERSION "1.8.3"
RUN pip install poetry==${POETRY_VERSION}
RUN poetry config virtualenvs.create false

WORKDIR /opt/server

# Install dependencies:
COPY pyproject.toml poetry.lock ./
RUN poetry install

COPY server/ ./

ENV FLAGS_DATABASE=/var/destructivefarm/flags.sqlite 
ENV FLASK_APP=standalone
ENV PYTHONPATH=/opt/server

VOLUME [ "/var/destructivefarm" ]
EXPOSE 5000

# Run the application:
ENTRYPOINT ["/bin/sh", "-c", "chmod +x ./start_server.sh && ./start_server.sh"]
