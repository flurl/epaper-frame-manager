# pull official base image
FROM python:3.12-slim-bookworm
# set work directory
WORKDIR /usr/src/epaper_converter

# install system dependencies
RUN apt-get update && apt-get install -y imagemagick --no-install-recommends

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy entrypoint.sh
COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /usr/src/epaper_converter/entrypoint.sh
RUN chmod +x /usr/src/epaper_converter/entrypoint.sh

# copy project
COPY . .

# run entrypoint.sh
ENTRYPOINT ["/usr/src/epaper_converter/entrypoint.sh"]