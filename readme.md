# Добро пожаловать на кейс "Предиктивная оценка возникновения лесных пожаров"!
***
### Описание обучающего датасета:

Обучающий датасет состоит из следующих файлов и папок:
- папки ```00``` - ```20``` - папки, в которых представлены 20 территорий в виде многослойных ```.tiff``` - файлов. Распределение по слоям: (r, g, b, ik, mask), где r, g, b - каналы изображения, ik - канал ИК изображения, mask - бинарный канал маски). Также, представлены выгрузки погодных условий для указанной территории.
- файл ```Реестр пожаров 2015-2021.xlsx``` - Excel-файл, содержащий данные о пожарах на территориях, представленных в датасете.
- файл ```tiff_open.py```   - скрипт-пример для открытия ```.tiff```-файлов в многоканальном режиме и их визуализации.
- файл ```api.py```   - скрипт-шаблон для получения дополнительной информации из открытых источников. Процедура взаимодействия: получите доступ к выбранному вами API для получения дополнительной информации, напишите обращение к нему в коде, предполагая, что на вход будут подаваться координаты (в формате ```lat/lng```) и дата (референс будет в коде), а на выход получается файл с названием вашей команды и ответом от выбранного API (одного или нескольких)


***
### Описание тестового датасета:

Тестовый датасет состоит из следующих файлов и папок:
- файл ```test.tiff``` - файл с целевой территорией.
- файл ```sample.csv```   - файл примера сабмита с ориентировочным результатом по метрике ~0,01 .
- файл ```readme.md```   - файл-описание тестового датасета 


#### По возникающим вопросам пишите в телеграм - @p0v4r

***

Участникам требуется разработать модель, которая, используя космические снимки высокого разрешения, метеоданные и любые дополнительные открытые данные, позволит выделять на заданной территории участки с высоким риском возникновения пожаров в ближайший месяц. Ожидается, что разработанное программное обеспечение будет эффективно сегментировать территории на космических снимках, выделяя участки с высоким риском пожара. Этот инструмент автоматизирует работу сотрудников, занимающихся охраной лесов, и поможет в борьбе с лесными пожарами, обеспечивая более точное и своевременное прогнозирование.

Желаем удачи и не забывайте задавать вопросы на отраслевых сессиях!

