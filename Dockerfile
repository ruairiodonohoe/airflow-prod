FROM astrocrpublic.azurecr.io/runtime:3.2-4

ADD requirements.txt .
RUN pip install uv
RUN uv pip install --system -r requirements.txt