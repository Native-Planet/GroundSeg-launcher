def theme():
    return {
            "CTk": {"fg_color": ["gray92", "gray14"]},
            "CTkToplevel": {"fg_color": ["gray92", "gray14"]},
            "CTkFrame": {
                "corner_radius": 6,
                "border_width": 0,
                "fg_color": ["gray86", "gray17"],
                "top_fg_color": ["gray81", "gray20"],
                "border_color": ["gray65", "gray28"]
                },
            "CTkButton": {
                "corner_radius": 6,
                "border_width": 0,
                "fg_color": ["#3B8ED0", "#1F6AA5"],
                "hover_color": ["#36719F", "#144870"],
                "border_color": ["#3E454A", "#949A9F"],
                "text_color": ["#DCE4EE", "#DCE4EE"],
                "text_color_disabled": ["gray74", "gray60"]
                },
             "CTkLabel": {
                "corner_radius": 0,
                "fg_color": "transparent",
                "text_color": ["gray10", "#DCE4EE"]
                },
             "CTkEntry": {
                "corner_radius": 6,
                "border_width": 2,
                "fg_color": ["#F9F9FA", "#343638"],
                "border_color": ["#979DA2", "#565B5E"],
                "text_color":["gray10", "#DCE4EE"],
                "placeholder_text_color": ["gray52", "gray62"]
              },
             "CTkCheckbox": {
                "corner_radius": 6,
                "border_width": 3,
                "fg_color": ["#3B8ED0", "#1F6AA5"],
                "border_color": ["#3E454A", "#949A9F"],
                "hover_color": ["#3B8ED0", "#1F6AA5"],
                "checkmark_color": ["#DCE4EE", "gray90"],
                "text_color": ["gray10", "#DCE4EE"],
                "text_color_disabled": ["gray60", "gray45"]
              },
             "CTkSwitch": {
                "corner_radius": 1000,
                "border_width": 3,
                "button_length": 0,
                "fg_Color": ["#939BA2", "#4A4D50"],
                "progress_color": ["#3B8ED0", "#1F6AA5"],
                "button_color": ["gray36", "#D5D9DE"],
                "button_hover_color": ["gray20", "gray100"],
                "text_color": ["gray10", "#DCE4EE"],
                "text_color_disabled": ["gray60", "gray45"]
              },
              "CTkRadiobutton": {
                "corner_radius": 1000,
                "border_width_checked": 6,
                "border_width_unchecked": 3,
                "fg_color": ["#3B8ED0", "#1F6AA5"],
                "border_color": ["#3E454A", "#949A9F"],
                "hover_color": ["#36719F", "#144870"],
                "text_color": ["gray10", "#DCE4EE"],
                "text_color_disabled": ["gray60", "gray45"]
              },
              "CTkProgressBar": {
                "corner_radius": 1000,
                "border_width": 0,
                "fg_color": ["#939BA2", "#4A4D50"],
                "progress_color": ["#3B8ED0", "#1F6AA5"],
                "border_color": ["gray", "gray"]
              },
              "CTkSlider": {
                "corner_radius": 1000,
                "button_corner_radius": 1000,
                "border_width": 6,
                "button_length": 0,
                "fg_color": ["#939BA2", "#4A4D50"],
                "progress_color": ["gray40", "#AAB0B5"],
                "button_color": ["#3B8ED0", "#1F6AA5"],
                "button_hover_color": ["#36719F", "#144870"]
              },
              "CTkOptionMenu": {
                "corner_radius": 6,
                "fg_color": ["#3B8ED0", "#1F6AA5"],
                "button_color": ["#36719F", "#144870"],
                "button_hover_color": ["#27577D", "#203A4F"],
                "text_color": ["#DCE4EE", "#DCE4EE"],
                "text_color_disabled": ["gray74", "gray60"]
              },
              "CTkComboBox": {
                "corner_radius": 6,
                "border_width": 2,
                "fg_color": ["#F9F9FA", "#343638"],
                "border_color": ["#979DA2", "#565B5E"],
                "button_color": ["#979DA2", "#565B5E"],
                "button_hover_color": ["#6E7174", "#7A848D"],
                "text_color": ["gray10", "#DCE4EE"],
                "text_color_disabled": ["gray50", "gray45"]
              },
              "CTkScrollbar": {
                "corner_radius": 1000,
                "border_spacing": 4,
                "fg_color": "transparent",
                "button_color": ["gray55", "gray41"],
                "button_hover_color": ["gray40", "gray53"]
              },
              "CTkSegmentedButton": {
                "corner_radius": 6,
                "border_width": 2,
                "fg_color": ["#979DA2", "gray29"],
                "selected_color": ["#3B8ED0", "#1F6AA5"],
                "selected_hover_color": ["#36719F", "#144870"],
                "unselected_color": ["#979DA2", "gray29"],
                "unselected_hover_color": ["gray70", "gray41"],
                "text_color": ["#DCE4EE", "#DCE4EE"],
                "text_color_disabled": ["gray74", "gray60"]
              },
              "CTkTextbox": {
                "corner_radius": 6,
                "border_width": 0,
                "fg_color": ["#F9F9FA", "gray23"],
                "border_color": ["#979DA2", "#565B5E"],
                "text_color":["gray10", "#DCE4EE"],
                "scrollbar_button_color": ["gray55", "gray41"],
                "scrollbar_button_hover_color": ["gray40", "gray53"]
              },
              "DropdownMenu": {
                "fg_color": ["gray90", "gray20"],
                "hover_color": ["gray75", "gray28"],
                "text_color": ["gray10", "gray90"]
              },
              "CTkFont": {
                "macOS": {
                  "family": "SF Display",
                  "size": 13,
                  "weight": "normal"
                },
                "Windows": {
                  "family": "Roboto",
                  "size": 13,
                  "weight": "normal"
                },
                "Linux": {
                  "family": "Roboto",
                  "size": 13,
                  "weight": "normal"
                }
              }
            }
