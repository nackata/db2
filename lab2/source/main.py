from  emulator import emulator

from source.Entities.MainController import MainController
from source.Entities.user import UsrController

if __name__ == "__main__":
    choosing = MainController.makeChoosing(["Main", "Emulator"], "Program ui")
    if choosing == 0:
        UsrController()
    elif choosing == 1:
        emulator()
