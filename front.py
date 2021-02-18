
from kivy.lang.builder import Builder


class Front_YG():
    def __init__(self):
        self.notes = []
        self.key = []
        pass

    ############################################################

    def Table(self):
        w = Builder.load_string("""
BoxLayout:
    orientation: "vertical"
    spacing:6

    Box_Label:

        AnchorLayout:
            anchor_y:"center"
            anchor_x:"center"
            ToggleButton:

                color: Color_Text
                background_color: 0,0,0,0

                text:'...'

                text_size: self.size
                valign: 'center'
                padding_x: 15

                background_normal:''
                background_down:'./ico/green.png'
                on_state:app.layout._Select_Key(self,root)

            AnchorLayout:
                padding: [0,5,10,5]
                anchor_y:"center"
                anchor_x:"right"
                Button:
                    size_hint_x:0.05
                    background_down:'./ico/delete_key_teach.png'
                    background_normal:'./ico/delete_key.png'
                    border:(1, 1, 1, 1)
                    on_release: app.layout.Del_Key(root)



    Box_TextInput:
        Main_TextInput:
            hint_text: "Примечания:"
            multiline: False
            focus: False
            on_focus: app.layout.Change_Text_Notes(self.focus,self)
        """)

        self.key.append(w.children[1].children[0].children[1])
        self.notes.append(w.children[0].children[0])
        return w
