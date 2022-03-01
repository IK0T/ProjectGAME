import pygame
# Сцена Главного Меню
pygame.init()
pygame.font.init()


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
