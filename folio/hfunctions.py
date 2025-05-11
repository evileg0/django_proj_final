import requests
import json
from datetime import datetime
from .models import MoexIndexData, SecuritiesIndexData


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
    objects_to_create = []
    for row in rows:
        try:
            index_id = row[0]
            trade_date = datetime.strptime(row[1], '%Y-%m-%d').date()
            ticker = row[2]
            short_name = row[3]
            sec_id = row[4]
            weight = float(row[5])
            trading_session = int(row[6])

            obj = MoexIndexData(
                index_id=index_id,
                trade_date=trade_date,
                ticker=ticker,
                short_name=short_name,
                sec_id=sec_id,
                weight=weight,
                trading_session=trading_session
            )
            objects_to_create.append(obj)

        except Exception as e:
            print(f"Ошибка при обработке строки {row}: {e}")

    # Массовое добавление записей
    if objects_to_create:
        MoexIndexData.objects.bulk_create(objects_to_create)
        print(f"Успешно загружено {len(objects_to_create)} записей")
    else:
        print("Не удалось обработать данные для загрузки")

def getsecuritiesindex():
    try:
        resp = requests.get(
                'https://iss.moex.com/iss/engines/stock/markets/shares/boards/TQBR/securities.json?iss.meta=off&iss'
                '.only=securities')
        data = resp.json()
        result = data
    except Exception as error:
        print("Ошибка загрузки индекса")
        print(error)
        return False
    return result

def save_securities_data_from_json(data_json):
    rows = data_json.get('securities', {}).get('data', [])

    if not rows:
        print("Нет данных для сохранения")
        return

    securities_to_update = {}
    secids_in_json = set()

    for row in rows:
        try:
            secid = row[0]
            shortname = row[2]
            prevprice = float(row[3])
            lotsize = int(row[4])

            secids_in_json.add(secid)

            securities_to_update[secid] = {
                'shortname': shortname,
                'prevprice': prevprice,
                'lotsize': lotsize,
            }

        except Exception as e:
            print(f"Ошибка при обработке строки {row}: {e}")

    created = []
    updated = []

    for secid, data in securities_to_update.items():
        obj, is_created = SecuritiesIndexData.objects.update_or_create(
            secid=secid,
            defaults=data
        )
        if is_created:
            created.append(obj)
        else:
            updated.append(obj)

    print(f"Создано: {len(created)} записей")
    print(f"Обновлено: {len(updated)} записей")

    # Очистка от записей, которых нет в json, пока уберем, может пригодится
    #SecuritiesIndexData.objects.exclude(secid__in=secids_in_json).delete()