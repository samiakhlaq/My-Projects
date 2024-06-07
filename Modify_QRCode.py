import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.image import Image as KivyImage
import qrcode as qrc

# Kivy language for layout and style
kv = '''
AnchorLayout:
    anchor_x: 'center'
    anchor_y: 'center'
    BoxLayout:
        orientation: 'vertical'
        size_hint: None, None
        size: 300, 300
        padding: 10
        spacing: 10
        canvas.before:
            Color:
                rgba: 0, 0, 0, 1
            Rectangle:
                pos: self.pos
                size: self.size

        Label:
            text: "QRGen"
            color: 0, 1, 0, 1  # Green color
            font_size: '24sp'
            size_hint_y: None
            height: 40
            outline_width: 2
            outline_color: 1, 1, 1, 1  # White color

        TextInput:
            id: data_input
            hint_text: "Enter your text or link"
            multiline: False
            background_color: 0, 0, 0, 1  # Black color
            foreground_color: 1, 1, 1, 1  # White color
            size_hint_y: None
            height: 40

        TextInput:
            id: filename_input
            hint_text: "Enter your file name"
            multiline: False
            background_color: 0, 0, 0, 1  # Black color
            foreground_color: 1, 1, 1, 1  # White color
            size_hint_y: None
            height: 40

        Button:
            text: "Generate QR Code"
            background_color: 0, 1, 0, 1  # Green color
            size_hint_y: None
            height: 50
            on_press: app.generate_qr_code()

        Label:
            id: qr_text
            text: ""
            color: 1, 1, 1, 1
            size_hint_y: None
            height: 40
'''

class QRCodeApp(App):
    def build(self):
        self.title = "QRGen"
        self.root = Builder.load_string(kv)

        # Set window size to resemble an Android layout
        Window.size = (360, 640)
        return self.root

    def generate_qr_code(self):
        data = self.root.ids.data_input.text
        file_name = self.root.ids.filename_input.text + "_QRCode.png"
        
        if not data:
            self.show_message("Please enter the data for the QR code.")
            return
        if not file_name:
            self.show_message("Please enter a file name.")
            return
        
        qr = qrc.QRCode(
            version=1,
            error_correction=qrc.constants.ERROR_CORRECT_H,
            box_size=20,
            border=4
        )
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="Green", back_color="Black")
        img.save(file_name)
        
        self.show_message(f"QR code saved as {file_name}")
        self.show_qr_code_image(file_name)

    def show_message(self, message):
        message_label = Label(text=message, color=(1, 1, 1, 1))
        self.root.add_widget(message_label)
        self.root.remove_widget(message_label)  # Remove after a delay

    def show_qr_code_image(self, file_name):
        popup = Popup(title='QR Code', size_hint=(None, None), size=(300, 300))
        qr_image = KivyImage(source=file_name)
        popup.content = qr_image
        popup.open()

if __name__ == "__main__":
    QRCodeApp().run()
