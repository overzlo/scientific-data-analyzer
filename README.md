# scientific-data-analyzer

Небольшой Python-модуль для анализа и визуализации научных данных (например, температурных измерений).
Он загружает CSV-файл, вычисляет базовые статистические показатели (среднее, минимум, максимум, стандартное отклонение) и строит график.

## Возможности
- Загрузка данных из CSV с помощью pandas
- Вычисление статистик (mean/min/max/std) по выбранному столбцу
- Построение линейного графика и сохранение его в файл (PNG)

## Установка
Требуется Python 3.11.

```bash
pip install -r requirements.txt
```

## Использование
```python
from src.analyzer import load_data, compute_stats, plot_series

# 1) Загрузка данных
df = load_data("data.csv")

# 2) Статистика по столбцу (например, "temperature")
stats = compute_stats(df, "temperature")
print(stats)  # {'mean': ..., 'min': ..., 'max': ..., 'std': ...}

# 3) Построение графика
plot_path = plot_series(df, "temperature", output_path="plot.png", title="Temperature")
print(f"График сохранён в: {plot_path}")
```

## Структура проекта
```
scientific-data-analyzer/
├── src/
│   ├── __init__.py
│   └── analyzer.py
├── tests/
│   └── test_analyzer.py
├── .github/
│   └── workflows/
│       └── ci.yml
├── README.md
├── LICENSE
├── requirements.txt
└── data.csv
```

## Тестирование
```bash
pytest -q
```

## CI/CD
Проект настроен на запуск тестов в GitHub Actions при каждом push и pull request (Python 3.11).

## Лицензия
MIT. См. файл LICENSE.
