# scientific-data-analyzer

Небольшой Python-модуль для анализа и визуализации научных данных (например, температурных измерений).
Он загружает CSV-файл, вычисляет базовые статистические показатели (среднее, минимум, максимум, стандартное отклонение) и строит графики.

## Как посмотреть на работу?
- По умолчанию графики сохраняются в файлы в текущей директории:
  - Линейный график — в plot.png (или в путь, который вы зададите).
  - Гистограмма — в hist.png (если вы её попросите построить).
- Можно также открыть окно с графиком, передав параметр show=True в коде или ключ --show в CLI (см. ниже).

Примеры запуска:

1) Через Python-код
```python
from src.analyzer import load_data, compute_stats, plot_series, plot_histogram

# 1) Загрузка данных
df = load_data("data.csv")

# 2) Статистика по столбцу (например, "temperature")
stats = compute_stats(df, "temperature")
print(stats)  # {'mean': ..., 'min': ..., 'max': ..., 'std': ...}

# 3) Линейный график (с сохранением в файл)
plot_path = plot_series(df, "temperature", output_path="plot.png", title="Temperature")
print(f"График сохранён в: {plot_path}")

# 4) Линейный график с усреднением (скользящее среднее по 3 точкам) и показом окна
plot_series(df, "temperature", output_path="plot_ma.png", ma_window=3, show=True)

# 5) Гистограмма распределения значений
hist_path = plot_histogram(df, "temperature", bins=15, output_path="hist.png")
print(f"Гистограмма сохранена в: {hist_path}")
```

2) Через CLI (командную строку)
Теперь можно запустить модуль как приложение:
```bash
python -m src data.csv temperature --output plot.png --show --ma-window 3 --hist --hist-bins 15 --hist-output hist.png
```
- Где будет график? Линейный график будет сохранён в файл plot.png (или другой путь, который вы укажете ключом --output). Гистограмма — в hist.png (или --hist-output).
- Ключ --show откроет окно с графиком(ами) поверх сохранения в файл.
- Параметр ma_window в plot_series позволяет наложить скользящее среднее (например, ma_window=3).
- Ключ --hist создаёт гистограмму по выбранному столбцу (есть опция --hist-bins для выбора числа корзин).
- Параметр show=True (или ключ --show) включает интерактивный показ графиков.
- Небольшой визуальный стиль 'ggplot' используется по умолчанию для более приятного вида графиков.

## Установка
Требуется Python 3.11.

```bash
pip install -r requirements.txt
```

## Структура проекта
```
scientific-data-analyzer/
├── src/
│   ├── __init__.py
│   ├── __main__.py
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
