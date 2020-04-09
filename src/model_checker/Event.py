class Event:
    def __init__(self, name: str, src, des, on_event=None):
        self._on_event_callback = on_event
        self.name = name
        self.src = src
        self.des = des

    def on_event(self, model):
        if self._on_event_callback is not None:
            self._on_event_callback(model)

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

    def __str__(self):
        return self.name
