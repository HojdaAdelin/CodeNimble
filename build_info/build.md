pyinstaller --noconfirm --onefile -w --onedir --windowed -i "images/logo.ico" --add-data "images/logo.ico;images/" --add-data "images/run.png;images/" --add-data "[Path to customtkinter library];
--add-data "Themes/dark.json;Themes/" --add-data "Themes/light.json;Themes/"
customtkinter/" --name "CodeNimble" src/main.py