# Guru gRPC Server Tests

Тестирование gRPC сервера Niffler Currency с использованием Python, pytest и pbreflect.

## 📋 Содержание

- [Требования](#требования)
- [Установка](#установка)
- [Структура проекта](#структура-проекта)
- [Генерация gRPC клиента](#генерация-grpc-клиента)
- [Запуск тестов](#запуск-тестов)
- [WireMock для моков](#wiremock-для-моков)
- [Отчеты Allure](#отчеты-allure)

## 🔧 Требования

- Python 3.10+
- Docker и Docker Compose (для WireMock)
- Запущенный Niffler Currency gRPC сервер на `localhost:8092`

## 📦 Установка

### Используя pip:

```bash
pip install pbreflect pytest allure-pytest pydantic-settings
```

### Используя poetry:

```bash
poetry install
```

## 📁 Структура проекта

```
.
├── internal/
│   ├── grpc/
│   │   └── interceptors/      # Перехватчики для логирования и Allure
│   │       ├── allure.py      # Отчеты Allure
│   │       └── logging.py     # Консольное логирование
│   └── pb/                    # Сгенерированный gRPC код (не коммитится)
├── protos/                    # Proto-файлы (скачиваются с сервера)
├── settings/
│   └── settings.py            # Конфигурация (хосты сервисов)
├── tests/
│   ├── conftest.py            # Фикстуры pytest
│   ├── test_get_all_currencies.py
│   └── test_calculate_rate.py
├── wiremock/
│   └── grpc/
│       └── mappings/          # Стабы для WireMock
├── docker-compose.mock.yml    # Docker Compose для WireMock
├── pyproject.toml             # Зависимости проекта
└── README.md
```

## 🔨 Генерация gRPC клиента

### 1. Запустите Niffler Currency сервер

Убедитесь, что сервер запущен на `localhost:8092`.

### 2. Скачайте proto-файлы с сервера

```bash
pbreflect get-protos -h localhost:8092 -o ./protos
```

Это скачает все proto-файлы через gRPC Reflection API.

### 3. Сгенерируйте Python клиент

```bash
pbreflect generate --proto-dir ./protos --output-dir ./internal/pb --gen-type pbreflect
```

Это создаст:
- `niffler_currency_pb2.py` - Protobuf сообщения
- `niffler_currency_pb2.pyi` - Тайп-хинты для IDE
- `niffler_currency_pb2_pbreflect.py` - Strongly-typed gRPC клиент

## 🧪 Запуск тестов

### Тесты против реального сервера

```bash
pytest tests/
```

### Тесты против WireMock (моки)

```bash
# 1. Запустите WireMock
docker-compose -f docker-compose.mock.yml up -d

# 2. Запустите тесты с флагом --mock
pytest tests/ --mock

# 3. Остановите WireMock
docker-compose -f docker-compose.mock.yml down
```

### Запуск конкретного теста

```bash
pytest tests/test_get_all_currencies.py -v
pytest tests/test_calculate_rate.py::test_calculate_rate_eur_to_rub -v
```

## 🎭 WireMock для моков

WireMock позволяет тестировать без реального сервера.

### Конфигурация

- **WireMock UI**: http://localhost:8888
- **gRPC порт**: localhost:8094
- **Стабы**: `wiremock/grpc/mappings/`

### Доступные моки

#### `getAllCurrencies.json`
Возвращает список из 4 валют: RUB, KZT, EUR, USD

#### `calculateRate.json`
Поддерживает 5 сценариев:
- USD → RUB (100 → 6666.67)
- RUB → USD (100 → 1.5)
- USD → USD (100 → 100.0)
- EUR → RUB (100 → 7200.0)
- Ошибка при отсутствии desiredCurrency

## 📊 Отчеты Allure

### Генерация отчета

```bash
# 1. Запустите тесты с генерацией результатов
pytest tests/ --alluredir=./allure-results

# 2. Откройте отчет в браузере
allure serve ./allure-results
```

### Что включено в отчет

- **Шаги**: Каждый gRPC вызов - отдельный шаг
- **Request**: JSON-представление запроса
- **Response**: JSON-представление ответа
- **Логи**: Консольный вывод

## 🔍 Описание тестов

### `test_get_all_currencies.py`

**Тест**: `test_get_all_currencies`
- Проверяет, что API возвращает 4 валюты
- Валидирует наличие кода валюты и курса

### `test_calculate_rate.py`

**Тест 1**: `test_calculate_rate_eur_to_rub`
- Конвертация EUR → RUB
- 100 EUR = 7200 RUB

**Тест 2**: `test_calculate_rate_without_desired_currency`
- Проверка обработки ошибок
- Отсутствие обязательного поля должно вызвать gRPC ошибку

**Тест 3**: `test_currency_conversion` (параметризованный)
- USD → RUB
- RUB → USD
- USD → USD (та же валюта)

## ⚙️ Конфигурация

Настройки находятся в `settings/settings.py`:

```python
class Settings(BaseSettings):
    wiremock_host: str = "localhost:8094"           # WireMock
    currency_service_host: str = "localhost:8092"    # Реальный сервис
```

Можно переопределить через переменные окружения:

```bash
export CURRENCY_SERVICE_HOST=localhost:9092
export WIREMOCK_HOST=localhost:9094
pytest tests/
```

## 🏗️ Архитектурные паттерны

### Interceptor Pattern
- `LoggingInterceptor` - логирование в консоль
- `AllureInterceptor` - вложения в отчет Allure
- Применяются автоматически ко всем gRPC вызовам

### Fixture-Based Configuration
- Session-scope фикстуры для эффективности
- Флаг `--mock` для переключения между реальным сервером и моками
- Dependency injection через pytest fixtures

### Code Generation
- Proto-файлы не коммитятся (скачиваются с сервера)
- gRPC клиент генерируется автоматически
- Strongly-typed клиент для IDE autocomplete

## 📝 Домашнее задание

Задача: Реализовать тесты на gRPC сервер Niffler

### Выполнено:

✅ Создана структура проекта
✅ Настроены interceptors (logging + Allure)
✅ Написаны тесты для GetAllCurrencies
✅ Написаны тесты для CalculateRate (включая параметризованные)
✅ Настроен WireMock для моков
✅ Добавлена документация

### Как использовать:

1. **Запустите Niffler Currency сервер** в отдельном терминале
2. **Сгенерируйте клиент**: `pbreflect get-protos` + `pbreflect generate`
3. **Запустите тесты**: `pytest tests/`
4. **Сгенерируйте отчет**: `allure serve ./allure-results`

## 📚 Полезные команды

```bash
# Установка зависимостей
pip install pbreflect pytest allure-pytest pydantic-settings

# Скачать proto-файлы
pbreflect get-protos -h localhost:8092 -o ./protos

# Сгенерировать клиент
pbreflect generate --proto-dir ./protos --output-dir ./internal/pb --gen-type pbreflect

# Запуск тестов
pytest tests/                    # Против реального сервера
pytest tests/ --mock             # Против WireMock
pytest tests/ -v                 # С подробным выводом
pytest tests/ -k "test_calculate"  # Только тесты с "calculate" в имени

# Allure отчеты
pytest tests/ --alluredir=./allure-results
allure serve ./allure-results

# WireMock
docker-compose -f docker-compose.mock.yml up -d    # Запуск
docker-compose -f docker-compose.mock.yml down     # Остановка
docker-compose -f docker-compose.mock.yml logs -f  # Логи
```

## 🔗 Ссылки

- [pbreflect](https://github.com/ValeriyMenshikov/pbreflect) - Инструмент для генерации gRPC клиентов
- [WireMock gRPC](https://github.com/adven27/grpc-wiremock) - Mock-сервер для gRPC
- [Allure pytest](https://docs.qameta.io/allure/) - Фреймворк отчетности
- [Оригинальный репозиторий](https://github.com/MDN78/guru_grpc_tests) - Пример выполненной ДЗ

## 📧 Автор

Alina - guru_grpc_server_tests
