# python 3.13
#
# Ephemeral Dialog Definition
# 
import log
import visual
from screen_settings import DisplayParams
from pygame import Vector2
from os.path import join

class ESpec:
    def __init__(self, specfile):
        self.elements = []
        self.size = Vector2(720, 640)
        try:
            for line in specfile:
                l = line.split(" ")
                kw = l[0]
                match kw:
                    case "text":
                        self.elements.append(visual.create_text(l[1], Vector2(l[2], l[3]), l[4], visual.Colors.color_dict[l[5]]))
                    case "button":
                        self.elements.append(visual.create_button(l[1], Vector2(l[2], l[3])))
                    case "image":
                        self.elements.append(visual.create_image(l[1], Vector2(l[2], l[3]), Vector2(l[4], l[5]), None))
                    case "bg":
                        if l[1] == "image":
                            self.bg = visual.create_image(l[2], Vector2(0, 0), self.size, True)
                        elif l[1] == "color":
                            self.bg = visual.create_surface(visual.Colors.color_dict[l[2]], Vector2(0, 0), self.size, True)
                    case "size":
                        self.size = Vector2(l[2], l[3])
                    case None:
                        break
        except IndexError:
            log.log("Invalid Element Spec", log.LogLevel.Error)
            raise ValueError("Unexpected Element Spec Value")

def load_espec(name):
    fullname = join("dialogs", name)
    try:
        with open(fullname, "r") as file:
            return ESpec(file)
    except OSError as e:
        print(f"Error writing to file {fullname}: {e}")

class Dialog:
    def __init__(self, espec):
        pass