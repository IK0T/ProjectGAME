import json
import pygame
import random
import os
import pyautogui
import time
import keyboard
from colormap import hex2rgb


pygame.font.init()
pygame.mixer.init()


class Input:
    input_state = "main"

    record_keys = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t",
                   "u", "v", "w", "x", "y", "z",
                   "1", "2", "3", "4", "5", "6", "7", "8", "9", "0",
                   "UP", "DOWN", "LEFT", "RIGHT",
                   "SPACE", "CTRL", "SHIFT", "ALT", "RETURN", "ESCAPE", "TAB", "BACKSPACE"]

    def set_input_state(self, state):
        self.input_state = state

    def check_keys(self):
        for key in self.record_keys:
            exec("self.key_" + key + " = " + str(keyboard.is_pressed(key)))

    def __init__(self):
        self.check_keys()
        self.any_key_pressed = False

    def is_pressed(self, key, input_state=""):
        if input_state != "":
            return bool(keyboard.is_pressed(key) and pygame.mouse.get_focused() and input_state == self.input_state)
        else:
            return bool(keyboard.is_pressed(key) and pygame.mouse.get_focused())

    def is_just_pressed(self, key, input_state=""):

        exec("self.check_key = self.key_" + key)

        if input_state != "":
            return bool(self.check_key == False and keyboard.is_pressed(key) and input_state == self.input_state)
        else:
            return bool(self.check_key == False and keyboard.is_pressed(key))

    def is_any_key_pressed(self):
        return self.any_key_pressed


class Notification_Handler:
    notifications = []

    def __init__(self, game):
        self.game = game

    def send(self, title, message):
        print("[" + title + "] " + message)
        self.notifications.append({"title": title, "message": message, "time": 300})

    def render(self):
        height = 0
        last_end_y = 22

        for index, notification in enumerate(self.notifications):
            display_text = []
            current = ""
            message = notification["message"].split(" ")

            for index, word in enumerate(message):
                if current != "":
                    current += " " + word
                else:
                    current += word

                if index < len(message) - 1:
                    if len(current + message[index + 1]) > 30:
                        display_text.append(current)
                        current = ""

            display_text.append(current)

            height = 32 + (15 * len(display_text))

            pygame.draw.rect(self.game.main_surface, self.game.color_handler.get_color_rgb("notification.border"),
                             ((self.game.main_surface.get_width() - 250, last_end_y), (230, height)), False, 10)
            pygame.draw.rect(self.game.main_surface, self.game.color_handler.get_color_rgb("notification.fill"),
                             ((self.game.main_surface.get_width() - 246, last_end_y + 4), (222, height - 8)), False, 10)

            title_surface = self.game.font_handler.get_font("default_18", bold=True).render(notification["title"], True,
                                                                                            self.game.color_handler.get_color_rgb(
                                                                                                "notification.text"))
            self.game.main_surface.blit(title_surface, (self.game.main_surface.get_width() - 241, last_end_y + 2))

            for i, notif in enumerate(display_text):
                title_surface = self.game.font_handler.get_font("default_15").render(notif, True,
                                                                                     self.game.color_handler.get_color_rgb(
                                                                                         "notification.text"))
                self.game.main_surface.blit(title_surface,
                                            (self.game.main_surface.get_width() - 241, last_end_y + (i * 14) + 20))

            last_end_y = height + 20 + last_end_y

    def update(self):
        new_notif = self.notifications.copy()
        for index, notification in enumerate(self.notifications):
            self.notifications[index]["time"] -= 1
            if self.notifications[index]["time"] <= 0:
                new_notif.pop(new_notif.index(self.notifications[index]))
        self.notifications = new_notif


class Color_Handler:
    def __init__(self, game):
        self.game = game

    def get_color_hex(self, color_link):

        with open(os.path.join("src", "resources", self.game.current_assetpack, "assets", "colors.json"),
                  "r") as color_file:
            color_json = json.load(color_file)

        if color_link in color_json:
            return color_json[color_link]
        else:
            return "#00000"

    def get_color_rgb(self, color_link):

        with open(os.path.join("src", "resources", self.game.current_assetpack, "assets", "colors.json"),
                  "r") as color_file:
            color_json = json.load(color_file)

        return hex2rgb(color_json[color_link])


class Font_Handler:
    fonts = {
        "Ariel": {
            "file": pygame.font.SysFont('Ariel', 35),
            "size": 35
        }
    }

    def load_font(self, font, size, name=""):
        font_file = pygame.font.Font(
            os.path.join("src", "resources", self.game.current_assetpack, "assets", "fonts", font + ".ttf"), size)
        if name == "":
            self.fonts[font] = {
                "file": font_file,
                "size": size
            }
        else:
            self.fonts[name] = {
                "file": font_file,
                "size": size
            }

    def get_font(self, font, bold=False, italic=False, underline=False):
        if font in self.fonts:
            font_file = self.fonts[font]["file"]
            font_file.bold = bold
            font_file.italic = italic
            font_file.underline = underline
            return font_file
        else:
            return self.fonts[list(self.fonts.keys())[0]]["file"]

    def get_font_size(self, font):
        if font in self.fonts:
            return self.fonts[font]["size"]
        else:
            return self.fonts[list(self.fonts.keys())[0]]["size"]

    def __init__(self, game):
        self.game = game

        self.load_font("default", 40)
        self.load_font("default", 18, "default_18")
        self.load_font("default", 15, "default_15")


class Sound_Handler:

    sounds = {}

    def __init__(self, game):
        self.game = game

    def load_sound(self, sound_id, sound_file):
        self.sounds[sound_id] = {
            "file": pygame.mixer.Sound(os.path.join("src", "resources", self.game.current_assetpack, "assets", "sounds", sound_file + ".ogg"))
        }

    def play_sound(self, sound_id):
        self.sounds[sound_id]["file"].play()


class options:  # noqa

    def __init__(self, game):
        self.game = game

        # Открыто ли меню
        self.open = False
        # Включен ли показ FPS
        self.show_fps = False

        self.fps_module = fps(game)

        # Какой выбран модуль в меню
        self.menu_id = 0

        # Координаты подсказывающей метки
        self.marker_y = 200 + (self.menu_id * 70)
        self.marker_x = 40

        self.show_fps_text_surface = self.game.font_handler.get_font("default").render(f"Показать FPS:{self.show_fps}",
            True, (self.game.color_handler.get_color_rgb("taptap.text")))
        self.reset_save_text_surface = self.game.font_handler.get_font("default").render("Удалить Сохранение", True,
            (self.game.color_handler.get_color_rgb("taptap.text")))

        self.marker_target_width = self.show_fps_text_surface.get_width() + 20
        self.marker_width = self.marker_target_width

        self.bg_target_x = -1000
        self.bg_x = self.bg_target_x

    def update(self):
        self.bg_x += (self.bg_target_x - self.bg_x) / 10
        if self.open:
            self.bg_target_x = 5
            self.game.input.input_state = "options"
            if self.game.input.is_pressed("esc"):
                self.open = False

            self.menu_id = self.menu_id % 2

            if self.game.input.is_just_pressed("DOWN"):
                self.menu_id += 1
            if self.game.input.is_just_pressed("UP"):
                self.menu_id -= 1

            self.show_fps_text_surface = self.game.font_handler.get_font("default").render(f"Показать FPS: {str(self.show_fps)}", # noqa
                True, (self.game.color_handler.get_color_rgb("taptap.text")))

            self.marker_y += (270 + (self.menu_id * 140) - 25 - self.marker_y) / 8
            self.marker_width += (self.marker_target_width - self.marker_width) / 20

            if self.menu_id == 0:
                self.marker_target_width = self.show_fps_text_surface.get_width() + 20
            if self.menu_id == 1:
                self.marker_target_width = self.reset_save_text_surface.get_width() + 20

            if self.game.input.is_just_pressed("1") and self.game.input.is_just_pressed("ALT"):
                os.startfile(r'SecretGame.py')
                quit()

            if self.game.input.is_just_pressed("SPACE") or self.game.input.is_just_pressed("RETURN"):
                if self.menu_id == 0:
                    self.show_fps = not self.show_fps
                if self.menu_id == 1:
                    self.game.taptap.save_file = {"all_plays": []}
                    self.game.notification_handler.send('Сохранение удалено',
                                                        'Файл сохранения "TapTap"  удалён из главного меню')
        else:
            self.game.input.input_state = "game"
            self.bg_target_x = -1000

    def render(self):  # Отрисовка
        pygame.draw.rect(self.game.main_surface, self.game.color_handler.get_color_rgb("options.background"),
                         ((self.bg_x, 5), (500, self.game.display_height - 10)), False, 5)

        if self.open:
            pygame.draw.rect(self.game.main_surface, self.game.color_handler.get_color_rgb("taptap.marker"),
                             ((self.marker_x, self.marker_y), (self.marker_width, 5)), False, 5)

            self.game.main_surface.blit(self.show_fps_text_surface, (50, 200))
            self.game.main_surface.blit(self.reset_save_text_surface, (50, 340))


class result_screen:  # noqa

    def __init__(self, game):
        # avg_wmp - среднее символов в минуту
        # err - ошибки
        # wmp - символов в минуту
        self.game = game

        self.menu_id = 0

        self.marker_y = self.game.display_height - 70

        self.has_init = False

        self.wpm_target_x = self.game.display_width / 2 + 150
        self.wpm_x = self.game.display_width / 2 - 175

        self.avg_wpm_target_x = self.game.display_width / 2 + 400
        self.avg_wpm_x = self.game.display_width / 2 - 175

        self.err_target_x = self.game.display_width / 2 + 150
        self.err_x = self.game.display_width / 2 - 175

        self.time = 0

    def initialize(self):  # Инициализация
        self.has_init = True
        self.display_quote = [] # noqa
        quote = f'"{self.game.taptap.quotes[self.quote]["quote"]}"'  # noqa
        message = quote.split(" ")
        current = ""
        for index, word in enumerate(message):
            if current != "":
                current += " " + word
            else:
                current += word
            if index < len(message) - 1:
                if len(current + message[index + 1]) > 30:
                    self.display_quote.append(current)
                    current = ""

        self.display_quote.append(current)

        self.back_text_surface = self.game.font_handler.get_font("default").render("Назад", True,
                                                                                   self.game.color_handler.get_color_rgb( # noqa
                                                                                       "taptap.text"))

        self.author_text_surface = self.game.font_handler.get_font("default").render( # noqa
            "-" + self.game.taptap.quotes[self.quote]["author"], True,  # noqa
            self.game.color_handler.get_color_rgb("taptap.text"))
        self.wpm_text_surface = self.game.font_handler.get_font("default").render("С/М: " + str(int(self.net_wpm)),  # noqa
                                                                                  True,
                                                                                  self.game.color_handler.get_color_rgb(
                                                                                      "taptap.text"))
        self.err_text_surface = self.game.font_handler.get_font("default").render("Ошибки: " + str(self.errors), True,  # noqa
                                                                                  self.game.color_handler.get_color_rgb(
                                                                                      "taptap.text"))

        all_wpm_added = 0
        for score in self.game.taptap.save_file["all_plays"]:
            all_wpm_added += score["net_wpm"]

        avg_wpm = int(all_wpm_added / max(len(self.game.taptap.save_file["all_plays"]), 0.0000001)) # noqa
        self.avg_wpm_text_surface = self.game.font_handler.get_font("default").render("Ср. С/М: " + str(avg_wpm), True, # noqa
                                                                                      self.game.color_handler.get_color_rgb( # noqa
                                                                                          "taptap.text"))

        self.back_text_surface = self.game.font_handler.get_font("default").render("Назад", True, # noqa
                                                                                   self.game.color_handler.get_color_rgb( # noqa
                                                                                       "taptap.text"))

        self.polysurf = pygame.Surface((self.game.display_height - 450, self.game.display_height - 450), # noqa
                                       pygame.SRCALPHA)
        pygame.draw.rect(self.polysurf, self.game.color_handler.get_color_rgb("taptap.result_screen_front"),
                         ((0, 0), (self.game.display_height - 450, self.game.display_height - 450)), False, 40)

        self.has_init = True

        self.bg_y = 700 # noqa
        self.bg_target_y = 100 # noqa

    def reset(self):
        self.has_init = False
        self.time = 0
        self.avg_wpm_x = self.game.display_width / 2 - 175
        self.wpm_x = self.game.display_width / 2 - 175
        self.err_x = self.game.display_width / 2 - 175
        self.bg_y = -700 # noqa

    def update(self):
        # Обновление
        self.time += 1

        if not self.has_init:
            self.initialize()

        self.bg_y += (self.bg_target_y - self.bg_y) / 20

        if self.time >= 90:
            self.bg_y = self.bg_target_y # noqa
            self.wpm_x += (self.wpm_target_x - self.wpm_x) / 20
            self.avg_wpm_x += (self.avg_wpm_target_x - self.avg_wpm_x) / 20
            self.err_x += (self.err_target_x - self.err_x) / 20

        if self.game.input.is_just_pressed("SPACE", "game"):
            self.reset()
            self.game.taptap.switch_scene("main_screen")

    def render(self):
        # Рендерит все результаты на экран
        if not self.has_init:
            self.initialize()

        if self.time >= 90:
            pygame.draw.rect(self.game.main_surface,
                             self.game.color_handler.get_color_rgb("taptap.result_screen_panels"),
                             ((self.wpm_x, self.game.display_height / 4 + 25), (350, 60)), False, 5)
            self.game.main_surface.blit(self.wpm_text_surface, (self.wpm_x + 110, self.game.display_height / 4 + 25))

            pygame.draw.rect(self.game.main_surface,
                             self.game.color_handler.get_color_rgb("taptap.result_screen_panels"),
                             ((self.avg_wpm_x, self.game.display_height / 2 - 25), (350, 60)), False, 5)
            self.game.main_surface.blit(self.avg_wpm_text_surface,
                                        (self.avg_wpm_x + 55, self.game.display_height / 2 - 25))

            pygame.draw.rect(self.game.main_surface,
                             self.game.color_handler.get_color_rgb("taptap.result_screen_panels"),
                             ((self.err_x, self.game.display_height - self.game.display_height / 4 - 75), (350, 60)),
                             False, 5)
            self.game.main_surface.blit(self.err_text_surface, (
                self.err_x + 110, self.game.display_height - self.game.display_height / 4 - 75))

        self.game.main_surface.blit(pygame.transform.rotate(self.polysurf, 45),
                                    (self.game.display_width / 2 - (self.game.display_height - 200) / 2, self.bg_y))

        self.game.main_surface.blit(self.author_text_surface, (
            self.game.display_width / 2 - self.author_text_surface.get_width() / 2,
            self.game.display_height / 3 + 45 * len(self.display_quote) + 50 + self.bg_y))

        for index, line in enumerate(self.display_quote):
            quote_text_surface = self.game.font_handler.get_font("default").render(line, True,
                                                                                   self.game.color_handler.get_color_rgb( # noqa
                                                                                       "taptap.text"))
            self.game.main_surface.blit(quote_text_surface, (
                self.game.display_width / 2 - quote_text_surface.get_width() / 2,
                self.game.display_height / 3 + 45 * index + 20 + self.bg_y))

        pygame.draw.rect(self.game.main_surface, self.game.color_handler.get_color_rgb("taptap.marker"),
                         ((70, self.marker_y), (100, 5)), False, 5)

        self.game.main_surface.blit(self.back_text_surface,
                                    (70, self.game.display_height - 70 - self.back_text_surface.get_height()))


class typing_test:  # noqa

    def __init__(self, game):
        # wmp - символ в минуту
        # С остальными и так понятно
        self.game = game

        self.marker_height = 5
        self.marker_width = 25
        self.marker_target_width = 25

        self.marker_x = 0
        self.marker_y = self.game.display_height / 2 - self.marker_height + 13

        self.marker_draw_x = self.marker_x
        self.marker_draw_y = self.marker_y

        self.type_this = ""
        self.typed_text = ""

        self.typed_entries = 0

        self.errors = 0
        self.wpm = 0

        self.done = False

        self.time = 1
        # Звук ошибки
        self.game.sound_handler.load_sound("error", "error")

        self.has_started = False

        self.next_letter = self.game.font_handler.get_font("default").render("H", True,
                                                                             self.game.color_handler.get_color_rgb(
                                                                                 "taptap.text"))

        self.black_cover_surf = pygame.Surface((1, 1), pygame.SRCALPHA)
        pygame.draw.rect(self.black_cover_surf, self.game.color_handler.get_color_rgb("options.background"),
                         ((0, 0), (1, 1)))
        self.black_cover_surf.set_alpha(230)

        self.wpm = (self.typed_entries / 5) / (self.time / 60 / 60)
        self.net_wpm = self.wpm - (self.errors / max(int((self.time / 60) / 60), 1))

        self.net_wpm = max(self.net_wpm, 0)

        self.wpm_surface = self.game.font_handler.get_font("default").render("С/M: " + str(int(self.net_wpm)), True,
                                                                             self.game.color_handler.get_color_rgb(
                                                                                 "taptap.text"))

        self.text = self.game.font_handler.get_font("default").render(self.type_this, True,
                                                                      self.game.color_handler.get_color_rgb(
                                                                          "taptap.text"))
        self.typed_text_surface = self.game.font_handler.get_font("default").render(self.typed_text, True,
                                                                                    self.game.color_handler.get_color_rgb(  # noqa
                                                                                        # noqa
                                                                                        "taptap.dark_text"))

        self.y_offset_when_done = 0
        self.y_offset_when_done_target = 700

        self.game_done = False

    def reset(self):
        # Полное обновление значений
        self.has_started = False
        self.typed_text = ""

        self.typed_entries = 0

        self.errors = 0
        self.wpm = 0

        self.done = False
        self.game_done = False

        self.time = 1
        self.y_offset_when_done = 0

    def update(self):
        self.time += 1
        if self.has_started and not self.game_done:

            if self.game.input.is_any_key_pressed():
                if len(self.type_this) != len(self.typed_text):
                    if self.type_this[len(self.typed_text)].lower() == " ":
                        exec('self.tmp_key = "SPACE"')
                    else:
                        exec('self.tmp_key = "' + self.type_this[len(self.typed_text)].lower() + '"')
                    if self.game.input.is_pressed(self.tmp_key, "game"):  # noqa
                        self.game.taptap.play_key_sound()
                        self.typed_text += self.type_this[len(self.typed_text)]
                        if self.tmp_key != "SPACE":  # noqa
                            self.typed_entries += 1
                    else:
                        self.game.sound_handler.play_sound("error")
                        self.errors += 1

        else:
            if self.game.input.is_pressed(self.type_this[0]):
                self.has_started = True
                self.game.taptap.play_key_sound()
                if len(self.type_this) != len(self.typed_text):
                    self.typed_text += self.type_this[len(self.typed_text)]
                self.typed_entries += 1

        self.marker_draw_x += (self.marker_x - self.marker_draw_x) / 10
        self.marker_draw_y += (self.marker_y - self.marker_draw_y) / 10

        self.text = self.game.font_handler.get_font("default").render(self.type_this, True,
                                                                      self.game.color_handler.get_color_rgb(
                                                                          "taptap.text"))
        self.typed_text_surface = self.game.font_handler.get_font("default").render(self.typed_text, True,
                                                                                    self.game.color_handler.get_color_rgb(  # noqa
                                                                                        # noqa
                                                                                        "taptap.dark_text"))
        self.marker_x = self.game.display_width / 2 - self.text.get_width() / 2 + self.typed_text_surface.get_width()

        self.wpm_surface = self.game.font_handler.get_font("default").render("C/M: " + str(int(self.net_wpm)), True,
                                                                             self.game.color_handler.get_color_rgb(
                                                                                 "taptap.text"))

        if len(self.type_this) != len(self.typed_text):
            self.next_letter = self.game.font_handler.get_font("default").render(self.type_this[len(self.typed_text)],
                                                                                 True,
                                                                                 self.game.color_handler.get_color_rgb(
                                                                                     "taptap.text"))
        self.marker_target_width = self.next_letter.get_width()
        self.marker_width += (self.marker_target_width - self.marker_width) / 10

        if self.game_done:
            self.y_offset_when_done += (self.y_offset_when_done_target - self.y_offset_when_done) / 20

            if self.time >= 40:
                self.game.taptap.show_result_screen(self.quote, int(self.net_wpm), self.errors)  # noqa
                self.reset()

        else:
            self.wpm = (self.typed_entries / 5) / (self.time / 60 / 60)
            self.net_wpm = self.wpm - (self.errors / max(int((self.time / 60) / 60), 1))

            self.net_wpm = max(self.net_wpm, 0)

            if len(self.type_this) == len(self.typed_text):
                # Сохранение результов
                self.game.taptap.save_file['all_plays'].append({
                    "quote": self.game.taptap.quotes[self.quote]["quote"],  # noqa
                    "net_wpm": int(self.net_wpm),
                    "wpm": int(self.wpm),
                    "errors": self.errors
                })
                self.time = 0
                self.game_done = True

    def render(self):
        # Рендеринг
        self.game.main_surface.blit(self.text, (self.game.display_width / 2 - self.text.get_width() / 2,
                                                self.game.display_height / 2 - 42 + self.y_offset_when_done))
        self.game.main_surface.blit(self.typed_text_surface, (self.game.display_width / 2 - self.text.get_width() / 2,
                                                              self.game.display_height / 2 - 42 + self.y_offset_when_done))  # noqa

        if self.has_started:
            pygame.draw.rect(self.game.main_surface, self.game.color_handler.get_color_rgb("taptap.marker"), (
                (self.marker_draw_x, self.marker_draw_y + self.y_offset_when_done),
                (self.marker_width, self.marker_height)), False, 5)

        self.game.main_surface.blit(self.wpm_surface, (self.game.display_width / 2 - self.text.get_width() / 2,
                                                       self.game.display_height / 2 - 126 + self.y_offset_when_done))

        if not self.has_started:
            # Менюшка начала
            self.game.main_surface.blit(pygame.transform.scale(self.black_cover_surf, (
                self.game.main_surface.get_width(), self.game.main_surface.get_height())), (0, 0))

            letter = self.type_this[0]
            press_x_to_start = self.game.font_handler.get_font("default").render(f"Нажмите '{letter}' Чтобы начать",
                                                                                 True,
                                                                                 self.game.color_handler.get_color_rgb(
                                                                                     "taptap.text"))
            self.game.main_surface.blit(press_x_to_start,
                                        (self.game.display_width / 2 - press_x_to_start.get_width() / 2, 200))


class main_screen:  # noqa

    def __init__(self, game):
        self.game = game

        # Кнопки:
        self.play_text_surface = self.game.font_handler.get_font("default").render("Играть", True,
                                                                                   (
                                                                                       self.game.color_handler.get_color_rgb( # noqa
                                                                                           "taptap.text")))
        self.options_text_surface = self.game.font_handler.get_font("default").render("Настройки", True,
                                                                                      (
                                                                                          self.game.color_handler.get_color_rgb( # noqa
                                                                                              "taptap.text")))
        self.exit_text_surface = self.game.font_handler.get_font("default").render("Выход", True,
                                                                                   (
                                                                                       self.game.color_handler.get_color_rgb( # noqa
                                                                                           "taptap.text")))

        # Место расположениее маркера
        self.menu_id = 0
        # Его координаты
        self.marker_y = (self.game.display_height / 2) + (70 * self.menu_id) + 10

        if self.menu_id == 0:
            self.marker_target_width = self.play_text_surface.get_width()
        if self.menu_id == 1:
            self.marker_target_width = self.options_text_surface.get_width()
        if self.menu_id == 2:
            self.marker_target_width = self.exit_text_surface.get_width()

        self.marker_target_x = (self.game.display_width / 2) - (self.marker_target_width / 2) - 10
        self.marker_target_width += 20

        self.marker_width = self.marker_target_width
        self.marker_x = self.marker_target_x

        self.marker_x = self.marker_target_x

    def update(self):

        if self.game.input.is_just_pressed("UP", "game"):
            self.menu_id -= 1
        if self.game.input.is_just_pressed("DOWN", "game"):
            self.menu_id += 1

        if self.game.input.is_just_pressed("SPACE") or self.game.input.is_just_pressed("RETURN"):
            if self.menu_id == 0:
                self.game.taptap.switch_scene("pack_selection")
            if self.menu_id == 1:
                self.game.scene_options.open = True
            if self.menu_id == 2:
                self.game.stop()

        self.menu_id %= 3

        self.marker_y += ((self.game.display_height / 2) + (70 * self.menu_id) + 10 - self.marker_y) / 8

        self.marker_width += (self.marker_target_width - self.marker_width) / 10
        self.marker_x += (self.marker_target_x - self.marker_x) / 10

        self.marker_target_width = [self.play_text_surface, self.options_text_surface, self.exit_text_surface][
            self.menu_id].get_width()

        self.marker_target_x = (self.game.display_width / 2) - (self.marker_target_width / 2) - 10
        self.marker_target_width += 20

    def render(self):

        pygame.draw.rect(self.game.main_surface, (self.game.color_handler.get_color_rgb("taptap.marker")),
                         ((self.marker_x, self.marker_y), (self.marker_width, 5)), False, 5)

        self.game.main_surface.blit(self.play_text_surface, (
            self.game.display_width / 2 - self.play_text_surface.get_width() / 2,
            self.game.display_height / 2 - self.game.font_handler.get_font_size("default_42")))
        self.game.main_surface.blit(self.options_text_surface, (
            self.game.display_width / 2 - self.options_text_surface.get_width() / 2,
            self.game.display_height / 2 + self.game.font_handler.get_font_size("default_42")))
        self.game.main_surface.blit(self.exit_text_surface, (
            self.game.display_width / 2 - self.exit_text_surface.get_width() / 2,
            self.game.display_height / 2 + self.game.font_handler.get_font_size("default_42") * 3))


class pack_selection:  # noqa

    def __init__(self, game):
        self.game = game

        self.menu_id = 0
        # Все паки с опреденной папки записываются
        packs = os.listdir(os.path.join('src', 'resources', self.game.current_assetpack, 'packs'))
        self.quote_packs = []

        for i in packs:
            with open(os.path.join('src', 'resources', self.game.current_assetpack, 'packs', i),
                      encoding='utf-8') as file:
                self.quote_packs.append(json.load(file))

        self.quote_pack_target_y = []
        self.quote_pack_y = []
        for i in range(len(self.quote_packs)):
            self.quote_pack_target_y.append(self.game.display_height / 2 - ((i - self.menu_id) * 70))
            self.quote_pack_y.append(self.game.display_height / 2 - ((i - self.menu_id) * 70))

        self.marker_target_width = 0
        self.marker_width = self.marker_target_width

        self.marker_target_x = self.game.display_width / 2
        self.marker_x = self.marker_target_x
        self.marker_y = self.game.display_height / 2 + 50

    def update(self):  # Обновление положений и т.д.
        if self.game.input.is_just_pressed("UP", "game"):
            self.menu_id += 1
        if self.game.input.is_just_pressed("DOWN", "game"):
            self.menu_id -= 1

        if self.game.input.is_just_pressed("RETURN", "game") or self.game.input.is_just_pressed("SPACE", "game"):
            self.game.taptap.quotes = self.quote_packs[self.menu_id]["quotes"]
            self.game.taptap.start_quote(random.randint(0, len(self.game.taptap.quotes) - 1))

        self.menu_id %= len(self.quote_packs)

        for i in range(len(self.quote_packs)):
            self.quote_pack_target_y[i] = self.game.display_height / 2 - ((i - self.menu_id) * 70)
            self.quote_pack_y[i] += (self.quote_pack_target_y[i] - self.quote_pack_y[i]) / 10
        # Положение маркера (Как же я устал это писать)
        self.marker_width += (self.marker_target_width - self.marker_width) / 10
        self.marker_x += (self.marker_target_x - self.marker_x) / 10

    def render(self):  # Рендеринг
        pygame.draw.rect(self.game.main_surface, (self.game.color_handler.get_color_rgb("taptap.marker")),
                         ((self.marker_x, self.marker_y), (self.marker_width, 5)), False, 5)

        for index, quote_pack in enumerate(self.quote_packs):
            text_surface = self.game.font_handler.get_font("default").render(quote_pack['display_name'], True, (
                self.game.color_handler.get_color_rgb("taptap.text")))
            if self.menu_id - index == 0:
                self.marker_target_width = text_surface.get_width() + 20
                self.marker_target_x = self.game.display_width / 2 - text_surface.get_width() / 2 - 10
            else:
                text_surface.set_alpha(256 / (abs(self.menu_id - index) * 1))
            self.game.main_surface.blit(text_surface, (
            self.game.display_width / 2 - text_surface.get_width() / 2, self.quote_pack_y[index]))  # noqa


class taptap:

    def __init__(self, game):
        self.game = game

        self.typing_test_scene = typing_test(self.game)
        self.result_screen_scene = result_screen(self.game)
        self.main_screen_scene = main_screen(self.game)
        self.pack_selection_scene = pack_selection(self.game)

        self.game.sound_handler.load_sound("key_sound_0", "key_sound_0")
        self.game.sound_handler.load_sound("key_sound_1", "key_sound_1")
        self.game.sound_handler.load_sound("key_sound_2", "key_sound_2")
        self.game.sound_handler.load_sound("key_sound_3", "key_sound_3")

        if not os.path.exists(os.path.join("save_data", "taptap_save.json")):
            with open(os.path.join("save_data", "taptap_save.json"), "w") as file:
                file.write('{"all_plays": []}')
        with open(os.path.join("save_data", "taptap_save.json"), "r") as file_save_file:
            self.save_file = json.load(file_save_file)

    current_scene = ""

    clock = pygame.time.Clock()
    dt = 0

    def play_key_sound(self):
        random_int = random.randint(0, 3)
        self.game.sound_handler.play_sound("key_sound_" + str(random_int))

    def switch_scene(self, scene):
        self.current_scene = scene

    def start_quote(self, quote):
        self.typing_test_scene.type_this = self.quotes[quote]["quote"]
        self.typing_test_scene.quote = quote
        self.switch_scene("typing_test")

    def show_result_screen(self, quote, net_wpm, errors):
        self.result_screen_scene.quote = quote
        self.result_screen_scene.net_wpm = net_wpm
        self.result_screen_scene.errors = errors
        self.switch_scene("result_screen")

    def stop(self):
        with open(os.path.join("save_data", "taptap_save.json"), "w") as file:
            file.write(str(self.save_file).replace("'", '"'))


class fps:  # noqa

    def __init__(self, game):
        self.game = game  # Логично

        # Три обьекта (Обновление, Отрисовка ну и Итог):
        self.update = self.game.font_handler.get_font("default_18").render(
            "Обновление:         Fps   (           ms)", True, self.game.color_handler.get_color_rgb("options.text"))
        self.render = self.game.font_handler.get_font("default_18").render(
            "Отрисовка:            Fps   (           ms)", True, self.game.color_handler.get_color_rgb("options.text"))
        self.total = self.game.font_handler.get_font("default_18").render(
            "Итого:                     Fps   (           ms)", True,
            self.game.color_handler.get_color_rgb("options.text"))

    def draw_stats(self, update_time, draw_time):  # Рисует на экране Статистику
        cub = pygame.Surface((410, 90), pygame.SRCALPHA)
        pygame.draw.rect(cub, self.game.color_handler.get_color_rgb("options.background"), ((0, 0), (410, 100)), False,
                         10)
        cub.set_alpha(128)
        self.game.main_surface.blit(cub, (self.game.display_width - 310, self.game.display_height - 90))

        # Здесь Показыается FPS:
        update_fps = self.game.font_handler.get_font("default_18").render(
            str(1 / max(update_time, 0.0001)).split(".")[0], True,
            self.game.color_handler.get_color_rgb("options.text"))

        render_fps = self.game.font_handler.get_font("default_18").render(
            str(1 / max(draw_time, 0.0001)).split(".")[0], True, self.game.color_handler.get_color_rgb("options.text"))

        total_fps = self.game.font_handler.get_font("default_18").render(
            str(1 / max(draw_time + update_time, 0.0001)).split(".")[0], True,
            self.game.color_handler.get_color_rgb("options.text"))

        # Здесь Показыается PING:
        update_ping = self.game.font_handler.get_font("default_18").render(str(update_time * 1000)[0: 5], True,
                                                                           self.game.color_handler.get_color_rgb(
                                                                               "options.text"))
        render_ping = self.game.font_handler.get_font("default_18").render(str(draw_time * 1000)[0: 5], True,
                                                                           self.game.color_handler.get_color_rgb(
                                                                               "options.text"))
        total_ping = self.game.font_handler.get_font("default_18").render(
            str((draw_time + update_time) * 1000)[0: 5], True, self.game.color_handler.get_color_rgb("options.text"))

        # Отрисовка:
        for i in range(1, 4):
            # Текст:
            self.game.main_surface.blit([self.update, self.render, self.total][i - 1], (
                self.game.display_width - 300, self.game.display_height - update_fps.get_height() * i - 10))

            # FPS:
            self.game.main_surface.blit([update_fps, render_fps, total_fps][i - 1], (
                self.game.display_width - 182, self.game.display_height - update_fps.get_height() * i - 10))
            # Ping:
            self.game.main_surface.blit([update_ping, render_ping, total_ping][i - 1], (
                self.game.display_width - 90, self.game.display_height - update_ping.get_height() * i - 10))


class Game:
    main_screen = pygame.display.set_mode((1920, 1080))
    main_surface = pygame.Surface((1920, 1080))

    game_speed = 1
    clock = pygame.time.Clock()

    running = True
    title = "Game"

    current_assetpack = "main"

    display_width, display_height = pyautogui.size()

    def stop(self):
        self.running = False

    def change_title(self, title):
        self.title = title
        pygame.display.set_caption(title)

    def __init__(self):
        self.input = Input()
        self.notification_handler = Notification_Handler(self)
        self.color_handler = Color_Handler(self)
        self.font_handler = Font_Handler(self)
        self.sound_handler = Sound_Handler(self)

        self.taptap= taptap(self)

        self.display_width, self.display_height = pyautogui.size()

        self.scene_options = options(self)

        self.show_debug = False

        self.previous_time = time.time()

        with open(os.path.join("src", "properties.json"), "r") as file:
            self.properties = json.load(file)

        self.change_title(self.properties["id"])
        icon = pygame.image.load(os.path.join("src", "resources", self.current_assetpack, "assets", "icon.png"))
        pygame.display.set_icon(icon)

    def initialize(self):
        self.notification_handler.send("Successful Start",
                                       "Game started succesfully on version " + self.properties["version"])
        self.change_title(self.properties["id"])
        self.input.input_state = "game"

    def begin_update(self):

        # Calculate Delta Time
        now = time.time()
        self.delta_time = now - self.previous_time
        self.previous_time = now

        self.input.any_key_pressed = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.stop()
            if event.type == pygame.KEYDOWN:
                self.input.any_key_pressed = True

    def update(self):
        self.scene_options.update()

    def end_update(self):
        self.notification_handler.update()

        self.input.check_keys()

    def render(self):
        self.scene_options.render()

        self.notification_handler.render()

        copyright_text = self.font_handler.get_font("default_15").render("IK0T&ARSENIQ", True,
                                                                         (self.color_handler.get_color_rgb("taptap.text")))
        self.main_surface.blit(copyright_text, (self.display_width / 2 - copyright_text.get_width() / 2,
                                                self.display_height - self.font_handler.get_font_size("default_15") - 10))

    def main_loop_final(self, update_time, render_time):
        if self.scene_options.show_fps == True:
            self.scene_options.fps_module.draw_stats(update_time, render_time)

        surf = self.main_surface
        if self.main_screen.get_width() != self.main_surface.get_width():
            if self.main_screen.get_height() != self.main_surface.get_height():
                surf = pygame.transform.scale(self.main_surface, (self.main_screen.get_width(),
                                                                  self.main_screen.get_height()))
        self.main_screen.blit(surf, (0, 0))
        pygame.display.update()
        self.clock.tick(60)


game = Game()




game.initialize()

game.taptap.switch_scene("main_screen")

def begin_update():
    game.begin_update()

def update():
    game.update()

    if game.taptap.current_scene == "main_screen":
        game.taptap.main_screen_scene.update()
    elif game.taptap.current_scene == "pack_selection":
        game.taptap.pack_selection_scene.update()
    elif game.taptap.current_scene == "typing_test":
        game.taptap.typing_test_scene.update()
    elif game.taptap.current_scene == "result_screen":
        game.taptap.result_screen_scene.update()

def end_update():
    game.end_update()

def render():
    game.main_surface.fill(game.color_handler.get_color_rgb("taptap.background"))

    if game.taptap.current_scene == "main_screen":
        game.taptap.main_screen_scene.render()
    elif game.taptap.current_scene == "pack_selection":
        game.taptap.pack_selection_scene.render()
    if game.taptap.current_scene == "typing_test":
        game.taptap.typing_test_scene.render()
    elif game.taptap.current_scene == "result_screen":
        game.taptap.result_screen_scene.render()

    game.render()

def stop():
    game.taptap.stop()

while game.running:
    update_start_time = time.time()
    begin_update()

    update()

    end_update()
    update_end_time = time.time()

    render_start_time = time.time()
    render()
    render_end_time = time.time()

    game.main_loop_final(update_end_time - update_start_time, render_end_time - render_start_time)

stop()
pygame.quit()
