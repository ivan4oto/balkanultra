FROM nikolaik/python-nodejs:latest

WORKDIR /code

COPY requirements.txt /code/

RUN pip install --no-cache-dir -r requirements.txt

COPY package.json /code/

RUN npm install

COPY . /code/


