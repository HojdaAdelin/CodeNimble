class ViewManager:
    def __init__(self, config, win):
        self.config = config
        self.win = win
    def zoom_in(self):
        size = int(self.config.get("editor_font_size"))
        if size < 50:
            self.config['editor_font_size'] = size+5
            self.win.editor.apply_settings()
    def zoom_out(self):
        size = int(self.config.get("editor_font_size"))
        if size > 15:
            self.config['editor_font_size'] = size-5
            self.win.editor.apply_settings()
    def reset_zoom(self):
        self.config['editor_font_size'] = 20
        self.win.editor.apply_settings()
    def fullscreen(self):
        if self.win.isFullScreen():
            self.win.showNormal()
        else:
            self.win.showFullScreen()
    def status_bar(self):
        if self.win.status_bar.height() == 30:
            self.win.status_bar.setFixedHeight(0)
        else:
            self.win.status_bar.setFixedHeight(30)
    def left_panel(self):
        sz = self.win.splitter.sizes()
        if sz[0] == 0:
            self.win.splitter.setSizes([250] + self.win.splitter.sizes()[1:])
        else:
            self.win.splitter.setSizes([0] + self.win.splitter.sizes()[1:])

    def right_panel(self):
        sz = self.win.splitter.sizes()
        if sz[2] == 0:
            self.win.splitter.setSizes(self.win.splitter.sizes()[:-1] + [250])
        else:
            self.win.splitter.setSizes(self.win.splitter.sizes()[:-1] + [0])

