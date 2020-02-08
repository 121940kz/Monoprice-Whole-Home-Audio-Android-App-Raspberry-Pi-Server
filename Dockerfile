FROM python:3
ADD MonopriceAudioPythonServer.py /
RUN pip install 'pySerial>=2.0,<=2.9999'
EXPOSE 4999
CMD [ "python", "./MonopriceAudioPythonServer.py" ]
