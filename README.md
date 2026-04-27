# Currency Converter

## Author
**Варламов Глеб** 

## Description
Currency Converter - это GUI-приложение для конвертации валют с использованием актуальных курсов из внешнего API. Приложение сохраняет историю конвертаций и позволяет загружать её при следующем запуске.

## Features
- Конвертация между 15 основными валютами
- Получение актуальных курсов через API
- Сохранение истории конвертаций в JSON
- Загрузка истории из файла
- Очистка истории
- Валидация ввода (только положительные числа)
- Красивый графический интерфейс на tkinter

## How to Get API Key

1. Перейдите на сайт [ExchangeRate-API](https://www.exchangerate-api.com/)
2. Нажмите "Get Free API Key"
3. Зарегистрируйтесь (email + пароль)
4. После регистрации вы получите бесплатный API ключ на email
5. Бесплатный тариф позволяет 1500 запросов в месяц

**Альтернативные API:**
- [OpenExchangeRates](https://openexchangerates.org/) - требует регистрации
- [Frankfurter](https://www.frankfurter.app/) - бесплатный, без ключа

## Installation

### 1. Clone repository
```bash
git clone https://github.com/yourusername/currency-converter.git
cd currency-converter
