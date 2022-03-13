# simple_blockchain_api

Реализован API для взаимодействия с контрактом стандарта ERC-721 (NFT) в блокчейне Ethereum. 

(адрес контракта: https://rinkeby.etherscan.io/address/0x92e098def0ca9577bd50ca61b90b9a46ec1f2040)

Используемые технологии: FastAPI (pydantic, swagger), PonyORM, Postgresql, Web3, Docker, Docker-Compose.

эндпоинты:
* POST: /tokens/create: (необходимые данные - body: {"media_url": str, "owner": str}) - создание уникального токена в блокчейне с последующей записью в БД.
* GET: /tokens/total_supply - получение текущего значения totalSupply смарт контракта.
* GET: /tokens/list - получение всех объектов токенов, имеющихся в БД.

**Примечания:**
* Проект живет на localhost:8000.
* Перед сборкой докер контейнера (перед запуском проекта) необходимо внести информацию о URL блокчейн провайдера, секретном ключе кошелька в .env файл 
(параметры: provider_url и private_key соответственно).
* Также при необходимости можно изменить параметры contract_address (по умолчанию это 0x92e098deF0CA9577BD50ca61B90b9A46EC1F2040) в .env файле.
При изменении contract_address следует также изменить ABI контракта, который находится в src/contract/abi.json (по умолчанию там лежит ABI, 
соответствующий упомянутому выше контракту).
* Если запуск производится напрямую на локальной машине (без Docker), следует заменить db_host="db" на db_host="localhost" в .env файле. Если при этом
операционной системой является Windows, то в дополнение к вышесказанному в этом пункте следует раскомментировать 39 строчку в requirements.txt (#pywin32==303).

**Руководство по запуску:**
* Склонировать данный репозиторий (команда: git clone https://github.com/fl1p3mth3b1rd/simple_blockchain_api).
* Перейти в корень проекта.
* Заменить значения параметров provider_url и private_key в .env файле на свои.
* Собрать Docker-compose контейнеры (команда: docker-compose build).
* Запустить контейнеры (команда: docker-compose up).
* В браузере перейти по адресу localhost:8000/docs (страница Swagger API)
