FROM condaforge/miniforge3:latest

RUN conda install python=3.9 -y

COPY . .

RUN python -m pip install -e .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--timeout-keep-alive", "300"]
