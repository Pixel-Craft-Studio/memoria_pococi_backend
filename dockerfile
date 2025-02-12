FROM python:3.8-slim-bullseye

WORKDIR /app

COPY ./app .

# Instalar dependencias necesarias
RUN apt-get update && apt-get install -y \
    curl \
    gnupg2 \
    unixodbc \
    unixodbc-dev

# Agregar el repositorio de Microsoft y la clave GPG
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list

# Instalar el driver ODBC 17
RUN apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql17 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Instalar los requerimientos de Python
RUN pip install --no-cache-dir -r ./requirements.txt

EXPOSE 8001