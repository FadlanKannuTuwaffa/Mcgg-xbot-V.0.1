from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button


class MainScreen(BoxLayout):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(orientation="vertical", padding=20, spacing=15, **kwargs)

        # Judul
        self.add_widget(Label(
            text="MCGG-Xbot V0.1",
            font_size="24sp",
            bold=True,
            size_hint=(1, 0.2)
        ))

        # Status prediksi (placeholder)
        self.status_label = Label(
            text="Belum ada prediksi...",
            font_size="18sp",
            size_hint=(1, 0.2)
        )
        self.add_widget(self.status_label)

        # Tombol prediksi
        predict_btn = Button(
            text="Mulai Prediksi",
            size_hint=(1, 0.2),
            background_color=(0.1, 0.5, 0.8, 1),
            color=(1, 1, 1, 1),
            font_size="18sp"
        )
        predict_btn.bind(on_press=self.on_predict)
        self.add_widget(predict_btn)

        # Tombol keluar
        exit_btn = Button(
            text="Keluar",
            size_hint=(1, 0.2),
            background_color=(0.8, 0.1, 0.1, 1),
            color=(1, 1, 1, 1),
            font_size="18sp"
        )
        exit_btn.bind(on_press=self.on_exit)
        self.add_widget(exit_btn)

    def on_predict(self, instance):
        # Simulasi prediksi (dummy)
        self.status_label.text = "Prediksi lawan: Player #3"
        print("Prediksi dijalankan!")

    def on_exit(self, instance):
        App.get_running_app().stop()


class McggXbotApp(App):
    def build(self):
        return MainScreen()


if __name__ == "__main__":
    McggXbotApp().run()
