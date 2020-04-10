FROM python
COPY . /
RUN pip install pipenv -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN pipenv install
RUN pipenv run python3 Main.py