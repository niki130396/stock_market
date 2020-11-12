FROM python:3.8
ENV PYTHONUNBUFFERED=1
RUN mkdir /stock_market
WORKDIR /stock_market
COPY requirements.txt /stock_market/
RUN pip3 install -r requirements.txt
COPY . /stock_market/

