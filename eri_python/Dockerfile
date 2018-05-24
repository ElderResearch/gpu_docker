FROM lambdastack:latest

# installing a ton of python shiz. "hard" stuff via apt, stuff we want to
# be relatively fresh via pip3
RUN apt install --no-install-recommends --yes python3-setuptools
RUN apt install --no-install-recommends --yes python3-matplotlib
RUN apt install --no-install-recommends --yes python3-pip
RUN apt install --no-install-recommends --yes python3-wheel
RUN apt install --no-install-recommends --yes python3-tk
RUN pip3 install boto3 \
                 cssselect \
                 jupyter \
                 lxml \
                 neo4j-driver \
                 networkx \
                 nltk \
                 plotly \
                 psycopg2 \
                 requests \
                 seaborn \
                 sqlalchemy \
                 tables \
                 tqdm \
                 xlrd
