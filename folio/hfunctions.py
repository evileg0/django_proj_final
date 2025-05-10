import requests
import json
from datetime import datetime
from .models import MoexIndexData


def getimoexindex():
    try:
        resp = requests.get('https://iss.moex.com/iss/statistics/engines/stock/markets/index/analytics/IMOEX.json?iss.meta=off&limit=100')
        data = resp.json()
        result = data
    except Exception as error:
        print("Ошибка загрузки индекса")
        print(error)
        return False
    return result

def save_moex_data_from_json(data_json):
    rows = data_json.get('analytics', {}).get('data', [])
    if not rows:
        print("Нет данных для сохранения")
        return

    MoexIndexData.objects.all().delete()
    for row in rows:
        try:
            index_id = row[0]
            trade_date = datetime.strptime(row[1], '%Y-%m-%d').date()
            ticker = row[2]
            short_name = row[3]
            sec_id = row[4]
            weight = float(row[5])
            trading_session = int(row[6])


            MoexIndexData.objects.create(
                index_id=index_id,
                trade_date=trade_date,
                ticker=ticker,
                short_name=short_name,
                sec_id=sec_id,
                weight=weight,
                trading_session=trading_session
            )
        except Exception as e:
            print(f"Ошибка при обработке строки {row}: {e}")