import pygame

# Экран результатов
pygame.init()
pygame.font.init()


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
