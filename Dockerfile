FROM python:3.8-slim

WORKDIR ./
COPY . ./

RUN pip install tabulate
RUN pip install dicttoxml
RUN pip install xmltodict
RUN pip install --upgrade google-api-python-client
RUN pip install grpcio-tools
RUN pip install avro
RUN pip install pyyaml
RUN pip install ormsgpack

RUN python3 -m grpc_tools.protoc -I=./ --python_out=./ ./scheme.proto

ENTRYPOINT ["python", "main.py"]
