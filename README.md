Цель проекта — вывести готовую модель для оценки цен на недвижимость в продакшен. 

# Инструкции по запуску микросервиса

Каждая инструкция выполняется из директории репозитория mle-sprint3-completed
Если необходимо перейти в поддиректорию, напишите соотвесвтующую команду

## 1. FastAPI микросервис в виртуальном окружение
```python
#установка env
sudo apt-get update
sudo apt-get install python3.10-venv
python3.10 -m venv .venv_mle_project_sprint_3
source .venv_mle_project_sprint_3/bin/activate

# установка библиотек
pip3 install -r requirements.txt


# команда перехода в директорию
cd services
# команда запуска сервиса с помощью uvicorn
uvicorn ml_service.main:app --host 0.0.0.0 --port 8080

```

### Пример curl-запроса к микросервису

```bash

curl -X POST "http://localhost:8080/predict/123" \
     -H "Content-Type: application/json" \
     -d '{"id":91587,"building_id":10448,"floor":6,"kitchen_area":5.8,"living_area":43.0,"rooms":3,"is_apartment":"false","studio":"false","total_area":58.2,"build_year":1973,"building_type_int":4,"latitude":55.7171363831,"longitude":37.4607810974,"ceiling_height":2.4800000191,"flats_count":143,"floors_total":9,"has_elevator":"true"}'


```


## 2. FastAPI микросервис в Docker-контейнере

```bash
# команда перехода в нужную директорию
cd services

docker build -t my_app -f Dockerfile_ml_service .
docker container run --publish 1702:1702 --env-file .env --volume=./models:/services/models  my_app

```

### Пример curl-запроса к микросервису

```bash
curl -X POST "http://localhost:1702/predict/123" \
     -H "Content-Type: application/json" \
     -d '{"id":91587,"building_id":10448,"floor":6,"kitchen_area":5.8,"living_area":43.0,"rooms":3,"is_apartment":"false","studio":"false","total_area":58.2,"build_year":1973,"building_type_int":4,"latitude":55.7171363831,"longitude":37.4607810974,"ceiling_height":2.4800000191,"flats_count":143,"floors_total":9,"has_elevator":"true"}'
```

## 3. Docker compose для микросервиса и системы моониторинга

```bash
# команда перехода в нужную директорию
cd services
# команда для запуска микросервиса в режиме docker compose
docker compose up --build

#yandex_app address
localhost:1702

#prometeus address
localhost:9090

#метрики
localhost:1702/metrics

#grafana address:
localhost:3000

```

### Пример curl-запроса к микросервису

```bash
curl -X 'POST' \
  'http://localhost:
```

## 4. Скрипт симуляции нагрузки
Скрипт генерирует 5 запросов. По запросу раз в 10 секунд 

```
# команды необходимые для запуска скрипта
python make_requestions.py
```

Адреса сервисов:
- микросервис: http://localhost:1702
- Prometheus: http://localhost:9000
- Grafana: http://localhost:3000

Выбранные метрики:
     1. Количество предсказаний по бакетам. Помогает оценить рынок цен плюс отслеживать есть ли изменения в работе модели.
     2. Количество предсказаний выше среднего по выборке обучения - 11000000
Поможет нам увидеть, если модель начнет завышать оценки или наоборот занижать
     3. Доля обработанных запросов, поможет увидеть есть ли какие-то проблемы с доступностью сервиса
     4. CPU usage - помогает обнаружить скачки нагрузки
     5. Средняя цена с течением времени. Помогает отслеживать работу модели.

