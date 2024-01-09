from typing import Generator, Iterator
import requests
import json
from datetime import datetime, timezone
import queue
import threading
from concurrent.futures import ThreadPoolExecutor

user_agent_key = "User-Agent"
user_agent_value = "Mozilla/5.0"
headers = {user_agent_key: user_agent_value}


def get_ticker(file: str = 'ticker.txt') -> Generator[str, None, None]:
    with open(file) as file:
        for line in file:
            ticker = line.strip()
            yield ticker


def get_history_data(ticker: str,
                     start_date: str = '01.01.20',
                     end_date: str = '09.01.24',
                     interval: str = "1wk") -> Iterator[str, str, str, str, str, str, str]:
    """
    Получает исторические данные для указанного тикера актива.

    :param ticker: str, тикер актива.
    :param start_date: str, дата начала периода в формате 'дд.мм.гг'.
    :param end_date: str, дата окончания периода в формате 'дд.мм.гг'.
    :param interval: str, интервал времени (неделя, день и т.д.) (необязательный, по умолчанию '1wk' - одна неделя).
    :return: str, JSON-строка с историческими данными.
    """
    per2 = int(datetime.strptime(end_date, '%d.%m.%y').replace(tzinfo=timezone.utc).timestamp())
    per1 = int(datetime.strptime(start_date, '%d.%m.%y').replace(tzinfo=timezone.utc).timestamp())
    params = {"period1": str(per1), "period2": str(per2),
              "interval": interval, "includeAdjustedClose": "true"}
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
    response = requests.get(url, headers=headers, params=params)
    result = response.json()

    timestamp_list = result['chart']['result'][0]['timestamp']
    open_list = result['chart']['result'][0]['indicators']['quote'][0]['open']
    close_list = result['chart']['result'][0]['indicators']['quote'][0]['close']
    volume_list = result['chart']['result'][0]['indicators']['quote'][0]['volume']
    high_list = result['chart']['result'][0]['indicators']['quote'][0]['high']
    low_list = result['chart']['result'][0]['indicators']['quote'][0]['low']
    adjclose_list = result['chart']['result'][0]['indicators']['adjclose'][0]['adjclose']

    return zip(timestamp_list, open_list, close_list, volume_list,
               high_list, low_list, adjclose_list)

if __name__ == '__main__':
    pass


