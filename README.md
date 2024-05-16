# Необходимые библиотеки

```
pip install pytest-asyncio
pip install pytest-asyncio-cooperative
pip install requests
```

Длительные тесты я вынес в отдельный набор для ассинхронного запуска

# Запуск обычных тестов

```
pytest -v test_consecutive.py
```

# Запуск ассинхронных тестов

```
pytest -v cooperative\test_dynamic_data_delay.py
```
Видео [тут](https://github.com/Artem19140/Test-task-API/blob/main/API.mp4)
