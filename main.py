python
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout

from mcgg_core import montecarlo_predict

KV = 
BoxLayout:
    orientation: 'vertical'
    padding: 12
    spacing: 12

    TextInput:
        id: player_name
        hint_text: 'Masukkan nama player'
        size_hint_y: None
        height: '44dp'

    BoxLayout:
        size_hint_y: None
        height: '44dp'
        Button:
            text: 'Prediksi'
            on_release: app.do_predict(player_name.text)
        Button:
            text: 'Clear'
            on_release: app.do_clear()

    ScrollView:
        Label:
            id: output
            text: ''
            size_hint_y: None
            height: self.texture_size[1]
            text_size: self.width, None


class MCGGApp(App):
    def build(self):
        return Builder.load_string(KV)

    def do_predict(self, name: str):
        if not name:
            self.root.ids.output.text = 'Isi nama dulu.'
            return
        res = montecarlo_predict(name, sims=500)
        if not res:
            self.root.ids.output.text = 'Tidak ada prediksi.'
            return
        t = "Hasil Prediksi Lawan:\n"
        for n,p in res:
            t += f"{n}: {p:.1%}\n"
        self.root.ids.output.text = t

    def do_clear(self):
        self.root.ids.output.text = ''

if __name__ == '__main__':
    MCGGApp().run()
