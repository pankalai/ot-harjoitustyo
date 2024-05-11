class UISettings:
    """Sovelluksen käyttöliittymän asetukset sisältävä luokka
    """
    # Yleiset asetukset
    window_size = (750, 500)
    background_color = (219, 219, 200)

    button_size_big = (100, 40)
    button_color = (114, 214, 114)

    link_color = (15, 35, 50)
    text_color = (59, 19, 19)

    text_size_header = 44
    text_size_sub_header = 24
    text_size_big = 24
    text_size_medium = 18
    text_size_small = 15

    border_size = 1
    border_color_button = (55, 155, 55)
    border_color_input_field = (100, 100, 100)

    input_field_background = (219, 219, 219)

    # Aloitusnäkymä
    input_size = (200, 25)
    input_text_size = 21

    # Viestinäkymä
    window_size_message_view = (350, 200)
    button_size_small = (125, 25)

    # Elementit
    text_color_element = (5, 5, 5)
    text_size_element = 22

    # Alapalkki
    text_color_sub_bar = (55, 55, 55)
    text_size_sub_bar = 15

class KlondikeUISettings:
    """Klondiken ulkoasuasetukset sisältävä luokka
    """
    background_color = (219, 219, 200)
    card_size = (75, 110)

    stack_position = (50, 50)
    waste_position = (150, 50)
    pile_position = (50, 200)
    foundation_position = (325, 50)

    waste_offset = card_size[0]*0.25
    pile_offset_left = card_size[0]*1.25
    pile_offset_top = card_size[0]*0.25
    foundation_offset = card_size[0]*1.25

    empty_stack_color = (0, 0, 255)
    empty_foundation_color = (255, 0, 0)


ui_settings = UISettings()
klondike_ui_settings = KlondikeUISettings()
