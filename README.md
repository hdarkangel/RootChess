<h1>RootChess</h1>
Здесь в ближайшем времени появится инструкция <br>
*RootChess* - это шахматный движок с открытым исходным кодом, написанный на Python с использованием Pygame. Проект создан в рамках индивидуального проекта по информатике.

## Особенности
- Уникальные пиксельные фигуры
- Встроенные темы
- История всех ходов на боковой панели
- Код полностью открыт для изучения

Чтобы собрать из этого приложение, сохраните все файлы в одну папку и в терминале введите: 
python -m PyInstaller --noconfirm --onefile --windowed
--icon="иконка.ico" --add-data "images;images" --add-data "images1;images1"
--add-data "images2;images2" --add-data "images3;images3"
--add-data "images4;images4" --add-data "шрифт.ttf;."
--add-data "иконка.ico;." --add-data "меню0.png;."
--add-data "меню1.png;." --add-data "меню2.png;."
--name "RootChess" code.py

*Автор:* [hdarkangel](https://github.com/hdarkangel)  
*Абсолютное авторство принадлежит создателю. Лицензия MIT.*
