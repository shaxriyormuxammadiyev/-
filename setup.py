import os
import subprocess
import sys


def install_requirements(file_path="requirements.txt"):
    # 1. Fayl rostdan ham borligini tekshiramiz
    if not os.path.exists(file_path):
        print(
            f"Xatolik: '{file_path}' fayli topilmadi. "
            f"Iltimos, fayl skript bilan bir xil papkada ekanligini tekshiring."
        )
        return

    print(
        f"'{file_path}' aniqlandi. Kutubxonalarni o'rnatish boshlanmoqda...\n"
    )

    try:
        # 2. Terminalda 'pip install -r requirements.txt' buyrug'ini ishga tushiramiz
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "-r", file_path]
        )
        print("\n[Muvaffaqiyatli]: Barcha kutubxonalar yuklab olindi!")

    except subprocess.CalledProcessError as e:
        print(f"\n[Xatolik]: Kutubxonalarni yuklashda xatolik yuz berdi: {e}")


if __name__ == "__main__":
    install_requirements()