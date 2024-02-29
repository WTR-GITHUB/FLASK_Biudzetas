# start by pulling the python image
FROM python:3.11.8-alpine

# copy the requirements file into the image
COPY ./requrements.txt /app/requrements.txt

# switch working directory
WORKDIR /app

# install the dependencies and packages in the requirements file
RUN pip install -r requrements.txt

# copy every content from the local file to the image
COPY . /app

# configure the container to run in an executed manner
ENTRYPOINT [ "python" ]

CMD ["run.py" ]