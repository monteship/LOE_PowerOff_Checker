import platform
from win10toast import ToastNotifier


class Notify:
    def __init__(self, text):
        self.text = text
        self.__run()

    def __run(self):
        system = platform.system()
        match system:
            case 'Windows':
                self.send_windows_toast(self.text)
            case 'Linux':
                pass

    @staticmethod
    def send_windows_toast(text):
        try:
            toaster = ToastNotifier()
            toaster.show_toast(title="",
                               msg=text,
                               duration=15)
        except TypeError:
            """
            Non interfering bug
            *******************
            WNDPROC return value cannot be converted to LRESULT
            TypeError: WPARAM is simple, so must be an int object (got NoneType)
            """
            pass


if __name__ == '__main__':
    Notify('Hello')
