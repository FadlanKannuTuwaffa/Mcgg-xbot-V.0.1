from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.clock import Clock
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.dialog import MDDialog
from kivymd.uix.filemanager import MDFileManager
from mcgg_core import montecarlo_predict, log_actual_match, add_or_update_player

# Try to import easyocr; if not available, OCR feature will be disabled at runtime
try:
    import easyocr
    OCR_AVAILABLE = True
except Exception as e:
    OCR_AVAILABLE = False

KV = '''
Screen:
    MDBoxLayout:
        orientation: 'vertical'
        padding: dp(12)
        spacing: dp(12)

        MDToolbar:
            title: "MCGG OCR Offline"
            md_bg_color: app.theme_cls.primary_color
            elevation: 10

        MDBoxLayout:
            orientation: 'vertical'
            padding: dp(8)
            spacing: dp(8)
            size_hint_y: None
            height: self.minimum_height

            MDTextField:
                id: player_name
                hint_text: "Nama player untuk prediksi"
                mode: "rectangle"
                size_hint_x: 1

            MDBoxLayout:
                size_hint_y: None
                height: dp(48)
                spacing: dp(8)
                MDRaisedButton:
                    text: "Prediksi"
                    on_release: app.on_predict(player_name.text)
                MDFlatButton:
                    text: "Clear"
                    on_release: app.on_clear()

        MDSeparator:
            height: dp(1)

        # OCR area
        MDBoxLayout:
            orientation: 'vertical'
            padding: dp(8)
            spacing: dp(8)
            size_hint_y: None
            height: self.minimum_height

            MDLabel:
                text: "OCR: pilih screenshot untuk ekstrak nama"
                halign: "left"

            MDBoxLayout:
                size_hint_y: None
                height: dp(44)
                MDRaisedButton:
                    text: "Pilih Gambar"
                    on_release: app.file_manager_open()
                MDFlatButton:
                    text: "Isi Dari OCR"
                    on_release: app.fill_from_ocr()

            MDLabel:
                id: ocr_result
                text: ""
                halign: "left"
                theme_text_color: "Hint"

        MDSeparator:
            height: dp(1)

        # Log actual match
        MDBoxLayout:
            orientation: 'vertical'
            padding: dp(8)
            spacing: dp(8)
            size_hint_y: None
            height: self.minimum_height

            MDLabel:
                text: "Log Hasil Match (untuk pembelajaran)"
                halign: "left"
            MDTextField:
                id: log_round
                hint_text: "Round (mis. 5)"
                mode: "rectangle"
                size_hint_x: 1
            MDTextField:
                id: log_player
                hint_text: "Nama player (yang kamu amati)"
                mode: "rectangle"
                size_hint_x: 1
            MDTextField:
                id: log_opponent
                hint_text: "Nama opponent sebenarnya"
                mode: "rectangle"
                size_hint_x: 1
            MDBoxLayout:
                size_hint_y: None
                height: dp(44)
                MDRaisedButton:
                    text: "Simpan Log"
                    on_release: app.on_log_match(log_round.text, log_player.text, log_opponent.text)

        ScrollView:
            MDBoxLayout:
                id: output_box
                orientation: 'vertical'
                size_hint_y: None
                height: self.minimum_height
                padding: dp(8)
                spacing: dp(8)
'''

class MCGGApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.file_manager = MDFileManager(select_path=self.select_path, exit_manager=self.exit_manager)
        self._selected_image = None

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Indigo"
        return Builder.load_string(KV)

    def show_snackbar(self, msg):
        Snackbar(text=msg).open()

    def file_manager_open(self):
        # start file chooser at sdcard root
        try:
            self.file_manager.show('/sdcard/')
        except Exception:
            self.file_manager.show('/')

    def select_path(self, path):
        self._selected_image = path
        self.file_manager.close()
        self.root.ids.ocr_result.text = f"Selected: {path}"
        self.show_snackbar('Gambar dipilih. Tekan "Isi Dari OCR" untuk memproses.')

    def exit_manager(self, *args):
        self.file_manager.close()

    def fill_from_ocr(self):
        if not OCR_AVAILABLE:
            self.show_snackbar('OCR tidak tersedia (easyocr belum terpasang).')
            return
        if not self._selected_image:
            self.show_snackbar('Pilih gambar dulu.')
            return
        try:
            reader = easyocr.Reader(['en'], gpu=False)
            results = reader.readtext(self._selected_image)
            texts = [t[1] for t in results]
            joined = ' '.join(texts)
            self.root.ids.ocr_result.text = joined[:400]
            if texts:
                self.root.ids.player_name.text = texts[0]
            self.show_snackbar('OCR selesai. Cek hasil dan edit jika perlu.')
        except Exception as e:
            self.show_snackbar(f'OCR error: {e}')

    def on_predict(self, name: str):
        name = (name or "").strip()
        if not name:
            self.show_snackbar("⚠ Isi nama player dulu!")
            return
        add_or_update_player(name, 30, 1)
        self.dialog = MDDialog(title="Loading", text="Sedang memprediksi...")
        self.dialog.open()
        Clock.schedule_once(lambda dt: self._do_predict(name), 0.1)

    def _do_predict(self, name):
        try:
            res = montecarlo_predict(name, sims=500, history_weight=2.0)
        except Exception as e:
            self.dialog.dismiss()
            self.show_snackbar(f"Error saat prediksi: {e}")
            return
        self.dialog.dismiss()
        output_box = self.root.ids.output_box
        output_box.clear_widgets()
        if not res:
            self.show_snackbar("Tidak ada prediksi (player tidak ditemukan atau sedikit data).")
            return
        from kivymd.uix.card import MDCard
        from kivymd.uix.label import MDLabel
        from kivy.metrics import dp
        card = MDCard(orientation='vertical', padding=12, size_hint=(1,None))
        text = "📊 Hasil Prediksi Lawan:\n\n"
        for n,p in res:
            text += f"• {n}: {p:.1%}\n"
        lbl = MDLabel(text=text, halign='left', size_hint_y=None)
        lbl.height = dp(120)
        card.add_widget(lbl)
        output_box.add_widget(card)

    def on_clear(self):
        self.root.ids.player_name.text = ""
        self.root.ids.output_box.clear_widgets()

    def on_log_match(self, round_text, player_text, opp_text):
        try:
            rnd = int(round_text)
        except:
            self.show_snackbar("Round harus angka")
            return
        player = (player_text or "").strip()
        opp = (opp_text or "").strip()
        if not player or not opp:
            self.show_snackbar("Isi player dan opponent")
            return
        add_or_update_player(player, 30, 1)
        add_or_update_player(opp, 30, 1)
        try:
            log_actual_match(rnd, player, opp)
        except Exception as e:
            self.show_snackbar(f"Error saat simpan log: {e}")
            return
        self.show_snackbar("Log tersimpan. Model akan adaptasi pada prediksi berikutnya.")

if __name__ == '__main__':
    MCGGApp().run()
