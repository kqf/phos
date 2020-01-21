FROM akqf/root-python3

ADD . /phos
WORKDIR /phos/analysis

RUN pip install -r requirements.txt
