class Event:
    def __init__(self, name: str, src, des, on_event=None, args=None):
        if args is None:
            self.args = {}
        else:
            self.args = args
        self._on_event_callback = on_event
        self.name = name
        self.src = src
        self.des = des

    def on_event(self):
        if self._on_event_callback is not None:
            self._on_event_callback(*self.args)

    def __dict__(self):
        return {
            'name': self.name,
            'src': self.src,
            'des': self.des
        }

    def __getitem__(self, item):
        return getattr(self, item)

    def keys(self):
        return 'name', 'src', 'des'
