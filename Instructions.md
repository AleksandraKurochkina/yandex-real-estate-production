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
cd services/ml_service/
# команда запуска сервиса с помощью uvicorn
uvicorn main:app --host 0.0.0.0 --port 8080

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

# команда для запуска микросервиса в режиме docker compose
```

### Пример curl-запроса к микросервису

```bash
curl -X 'POST' \
  'http://localhost:...' \
```

## 3. Docker compose для микросервиса и системы моониторинга

```bash
# команда перехода в нужную директорию

# команда для запуска микросервиса в режиме docker compose

```

### Пример curl-запроса к микросервису

```bash
curl -X 'POST' \
  'http://localhost:
```

## 4. Скрипт симуляции нагрузки
Скрипт генерирует <...> запросов в течение <...> секунд ...

```
# команды необходимые для запуска скрипта
...
```

Адреса сервисов:
- микросервис: http://localhost:<port>
- Prometheus: ...
- Grafana: ...