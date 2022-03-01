import pygame

# Сцена прописи фразы
pygame.init()
pygame.font.init()


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
