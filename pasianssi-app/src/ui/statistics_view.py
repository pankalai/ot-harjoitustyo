from repositories.game_repository import game_repository
from ui.element import Element, Button
from datetime import datetime
import ui_settings
import pygame

def row_offset(start,offset):
    return start[0]+offset[0], start[1]+offset[1]

def string_to_datetime(string):
    return datetime.strptime(string, "%Y-%m-%d %H:%M:%S")

def time_diff_in_hours_minutes_seconds(datetime1, datetime2):
    dt1 = datetime.timestamp(datetime1)
    dt2 = datetime.timestamp(datetime2)

    dt1 = datetime.fromtimestamp(dt1)
    dt2 = datetime.fromtimestamp(dt2)

    return str(dt2 - dt1)
    

class StatisticsView:
    # button_size = (100, 40)
    # button_color = (114, 214, 114)

    # link_color = (15, 35, 50)
    # text_color = (59, 19, 19)

    # header_font_size = 44
    # sub_header_font_size = 28
    # button_font_size = 24
    # text_font_size = 18

    def __init__(self, window):
        self.window = window
        self.width, self.height = window.get_size()
        self.background_color = ui_settings.background_color

        self.top_by_time1 = game_repository.find_top_plays_by_time("klondike",1)
        self.top_by_moves1 = game_repository.find_top_plays_by_moves("klondike",1)

        self.top_by_time3 = game_repository.find_top_plays_by_time("klondike",3)
        self.top_by_moves3 = game_repository.find_top_plays_by_moves("klondike",3)

        self.header_text = Element(
            self.window,
            (self.width/2, 50),
            None,
            "Parhaat tulokset",
            ui_settings.text_size_header,
            ui_settings.text_color
        )

        # Column 1
        self.start_pos1 = 100,110
        self.header1 = Element(self.window, self.start_pos1, None, "Helppo", ui_settings.text_size_sub_header, ui_settings.text_color)
        self.sub_header1_1 = Element(self.window, row_offset(self.start_pos1,(125,15)), None, "Aika", ui_settings.text_size_medium, ui_settings.text_color)
        self.sub_header1_1.set_underline()
        self.sub_header1_2 = Element(self.window, row_offset(self.start_pos1,(325,15)), None, "Siirrot", ui_settings.text_size_medium, ui_settings.text_color)
        self.sub_header1_2.set_underline()

        # Column 2
        self.start_pos2 = 100,275
        self.header2 = Element(self.window, self.start_pos2, None, "Vaikea", ui_settings.text_size_sub_header, ui_settings.text_color)
        self.sub_header2_1 = Element(self.window, row_offset(self.start_pos2,(125,15)), None, "Aika", ui_settings.text_size_medium, ui_settings.text_color)
        self.sub_header2_1.set_underline()
        self.sub_header2_2 = Element(self.window, row_offset(self.start_pos2,(325,15)), None, "Siirrot", ui_settings.text_size_medium, ui_settings.text_color)
        self.sub_header2_2.set_underline()

        self.sub_headers = [self.header1, self.sub_header1_1, self.sub_header1_2, self.header2, self.sub_header2_1, self.sub_header2_2]

        self.button_back = Button(self.window, "Takaisin", (
            self.width/2-ui_settings.button_size_big[0]/2, self.height-ui_settings.button_size_big[1]*1.25), ui_settings.button_size_big, ui_settings.button_color, ui_settings.link_color, ui_settings.text_size_big)
    
    def draw_table(self):
        offset = 20, 75

        # By time
        lists = [self.top_by_time1,self.top_by_time3]
        for i,header in enumerate([self.sub_header1_1, self.sub_header2_1]):
            left, top = row_offset(header.get_position(),(0,25))
            for row in lists[i]:
                elem1 = Element(self.window,(left,top),None,row["username"],ui_settings.text_size_medium,ui_settings.text_color)
                elem1.draw()
                elem2 = Element(self.window,(left+offset[1],top),None, time_diff_in_hours_minutes_seconds(string_to_datetime(row["start_time"]), string_to_datetime(row["end_time"])),ui_settings.text_size_medium,ui_settings.text_color)
                elem2.draw()
                top += offset[0]
            
        # By moves
        lists = [self.top_by_moves1,self.top_by_moves3]
        for i,header in enumerate([self.sub_header1_2, self.sub_header2_2]):
            left, top = row_offset(header.get_position(),(0,25))
            for row in lists[i]:
                elem1 = Element(self.window,(left,top),None,row["username"],ui_settings.text_size_medium,ui_settings.text_color)
                elem1.draw()
                elem2 = Element(self.window,(left+offset[1],top),None,str(row["moves"]),ui_settings.text_size_medium,ui_settings.text_color)
                elem2.draw()
                top += offset[0]

    def show(self):
        self.window.fill(self.background_color)

        # Headers
        self.header_text.draw()

        for header in self.sub_headers:
            header.draw()

        # Tables
        self.draw_table()

        # Button
        self.button_back.draw()

        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        pygame.display.update()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONUP:
                    if self.button_back.touch(event.pos):
                        running = False

                elif event.type == pygame.MOUSEMOTION:
                    if self.button_back.touch(event.pos):
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    else:
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)