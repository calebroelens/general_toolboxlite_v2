from contextlib import contextmanager
from uvicorn import Server
from threading import Thread
from time import sleep


class WindowedServer(Server):
    """
    Special Server Class
    Can run in both window and non-windowed mode at the same time.
    """

    def install_signal_handlers(self) -> None:
        pass

    @contextmanager
    def run_in_thread(self):
        thread = Thread(target=self.run)
        thread.start()
        try:
            while not self.started:
                sleep(1e-3)
            yield
        finally:
            self.should_exit = True
            thread.join()
