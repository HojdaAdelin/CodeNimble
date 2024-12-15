import json

def save_session(file_manager):
    folder_name = file_manager.get_opened_foldername()
    file_name = file_manager.get_opened_filename()
    with open('config.json', 'r', encoding="utf-8") as f:
        data = json.load(f)
    data['session']['opened_folder'] = folder_name
    data['session']['opened_file'] = file_name

    with open('config.json', 'w', encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def reset_session():
    with open('config.json', 'r', encoding="utf-8") as f:
        data = json.load(f)
    data['session']['opened_folder'] = "None"
    data['session']['opened_file'] = "None"

    with open('config.json', 'w', encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    
def session_engine(win):
    with open('config.json', 'r', encoding="utf-8") as f:
        data = json.load(f)
    if data['session']['opened_folder'] != "None" and data['session']['opened_folder']:
        win.file_manager.open_folder(win.tree_view, win, data['session']['opened_folder'])
    if data['session']['opened_file'] != "None" and data['session']['opened_file']:
        win.file_manager.open_file(win.editor, win.tab_bar, data['session']['opened_file'])
