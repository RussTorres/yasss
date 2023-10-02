FROM continuumio/miniconda3


COPY . .

RUN pip install -r requirements.txt
RUN pip install uvicorn


CMD ["python", "-m", "uvicorn", "yasss.app.yasss:yasss_app", "--host", "0.0.0.0", "--port", "80"]