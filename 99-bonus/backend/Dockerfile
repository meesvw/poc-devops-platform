FROM python:3.9

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "app.py"]


#############################
# What I fixed in this file #
#############################
# 1. Copy was not on its own line
# 2. Added some whitespaces for readability
# 3. Change pip install to use requirements.txt instead of hardcoded values
#
