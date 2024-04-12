FROM --platform=linux/amd64 python:3.10-slim

# install requirements
COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

# Set the working directory to the component folder
WORKDIR /load_faction_websites/load_nva_component/src

# Copy over src-files and spec of the component
COPY src/ .

ENTRYPOINT ["fondant", "execute", "main"]