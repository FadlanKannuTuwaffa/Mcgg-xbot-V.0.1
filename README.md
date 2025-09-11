# MCGG Pairing Predictor (KivyMD) - OCR Offline Version

This project is a KivyMD Android app template that integrates **offline OCR (EasyOCR)** to extract player/opponent names from screenshots.
It includes:
- KivyMD UI (tabs for Predict, History, OCR)
- Adaptive Monte-Carlo predictor that learns from logged matches
- OCR offline integration via `easyocr` (requires `torch` / `torchvision`)

Important notes BEFORE building:
- EasyOCR requires PyTorch. Including PyTorch/EasyOCR will make the APK **very large** (100+ MB) and the build process can be **fragile**.
- Building on GitHub Actions may fail due to heavy native dependencies. Expect to iterate and debug build settings.
- If you prefer a lighter solution, consider using an OCR API (online) instead of offline OCR in APK.

If build fails, copy the Actions logs and share them — I can help debug adjustments.
