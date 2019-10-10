# compose zoo+kafka+producer+consumer

Поднимает кластер из 3х нод apache-kafka и по одному zookeeper,producer,consumer

## Getting Started

Запуск и установка полностью автоматизированы, см. раздел "Installing"

### Prerequisites

Тестировалось и разрабатовалось на centos 7, для других ОС необходимо ставить пакеты вручную и убрать строки с yum из файла start.sh Если на системе не использует firewalld, так же необходимо удалить строки с ним из скрипта start.sh и вручную открыть порты 9092-9094

Крайне рекомендуется, для удобства тестирования, запускать в screen
Запускать из под root

### Особенности
consumer загружает все сообщения из kafka и продолает полочуать новые в реалтайме. consumer и producer в контейнерах загружаются раньше кластера kafka, что бы предотвратить завершение контейнеров
используется цикл с обработкой исключения. скрипты будут ждать кластер пока не подключатся

Топис my-topic в котором ходят сообщения, создается автоматически с 5 партициями
Если потребуется увеличить количество партиций можно:
#### 1 расширить используя оригинальную kafka, скачав ее с оф сайта
```
kafka-topics.sh --bootstrap-server localhost:9092 --alter --topic my-topic --partitions 5
```
#### 2 установить перед первым стартом переменные
в файле docker-compose.yml:
````
      KAFKA_NUM_PARTITIONS: 5
      KAFKA_TOPIC_PARTITION_COUNT_MAP: "my-topic: 5"
````

### Installing

Для запуска автоматической настройки хоста, сборки образов и запуска запустить файл start.sh

не забыть сделать его исполняемым

```
chmod +x start.sh
./start.sh
```


## Running the tests

После завершения сборки, старта и загрузки кластера можно проверить что сообщения проходят
Для корректной работы как в контейнерах, так и на хостовой системе обязательно должны быть поределены переменные окружения:
```
$KAFKA_SRVS
$DOCKER_HOST_IP
```

Они должны указывать на ip докер интерфейса или реальный ип машины, но не 127.0.0.1 иначе в контейнере скрипт
будет пытаться подключиться на внутренний локалхост, где kafka нет

Окружение определяет скрипт start.sh если переменные не определены можно выполнить вручную до запуска start.sh:
```
export KAFKA_SRVS=$(ip -4 addr show docker0 | grep -Po 'inet \K[\d.]+'):9092
export DOCKER_HOST_IP=$(ip -4 addr show docker0 | grep -Po 'inet \K[\d.]+')
```

### В docker
ВАЖНО! Producer выполняет отправку 100 сообщений, по 1 в секунду, и завершается

Что бы проверить, что сообщения ходят надо
1 Найти нужный ид контейнера:
```
docker ps -a
```
2 прочиттать лог внутри контейнера используя id контейнера из предыдущего шага
Логи расположены в /tmp т.к. этот путь самый короткий.
/tmp/producer.log
/tmp/consumer.log

пример:
```
docker exec <container_id> tail -fn 50 /tmp/consumer.log
```
### Запуск скриптов на хостовой системе

Проверить, что переменные окружения из начала главы определены и выполнить запуск
producer или consumer
пример:

```
python3 producer/producer.py
```

результат будет виден в stdout и в логах /tmp/producer.log или /tmp/consumer.log

###Проверить настройки топика
Можно проверить количество партиций, и реплик для топика, необходимо скачать оригинальную kafka с оф сайта и выполнить:

```
kafka-topics.sh --bootstrap-server localhost:9092  --topic my-topic --describe
```

## Задействовано

* [Моуль kafka-python](https://kafka-python.readthedocs.io/en/master/usage.html)
* [kafka compose](https://github.com/simplesteph/kafka-stack-docker-compose) - Готовая сборка kafka
* [kafka compose](https://docs.confluent.io/3.0.1/cp-docker-images/docs/configuration.html) - Документация к готовой сборке kafka
* [kafka](https://kafka.apache.org/downloads) - Чистая  kafka на оф сайте
* [kafka](https://svn.apache.org/repos/asf/kafka/trunk/config/server.properties) - Документация  kafka
