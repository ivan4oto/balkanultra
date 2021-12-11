FROM nikolaik/python-nodejs:latest

WORKDIR /code

COPY requirements.txt /code/

RUN pip install --no-cache-dir -r requirements.txt

COPY package.json /code/

RUN npm install

COPY . /code/

ADD https://github.com/stripe/stripe-cli/releases/download/v1.7.8/stripe_1.7.8_linux_amd64.deb ./

RUN apt install ./stripe_1.7.8_linux_amd64.deb \
 && rm ./stripe_1.7.8_linux_amd64.deb

