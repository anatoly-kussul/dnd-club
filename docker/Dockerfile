FROM python:3.6

# Python requirements
WORKDIR /
COPY python_requirements.txt .
RUN pip install -r python_requirements.txt
RUN rm python_requirements.txt

# Folder to mount your app code
RUN mkdir /app
WORKDIR /app
