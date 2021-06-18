FROM python:3.7.9
RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
VOLUME [ "/opt" ]
WORKDIR /opt
COPY requirements.txt requirements.txt
RUN pip3 install -i https://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com --upgrade pip && pip3 install -i https://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com -r requirements.txt
CMD ["python3"]
