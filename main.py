from telebot import types, TeleBot
from PIL import Image
import os
import time
import json

# ==========================
# Foydalanuvchilarni saqlash
# ==========================
USERS_FILE = "users.json"

def load_users():
    try:
        with open(USERS_FILE, "r") as f:
            return set(json.load(f))
    except (FileNotFoundError, json.JSONDecodeError):
        return set()

def save_users():
    with open(USERS_FILE, "w") as f:
        json.dump(list(all_users), f)

user_fan = {}
user_teacher = {}
user_states = {}  # {user_id: "state_name"}
pending_questions = {}  # {question_msg_id: student_id}
all_users = load_users()   # ✅ Fayldan yuklanadi
pending_broadcast = {}  # {admin_id: {"messages": [], "collecting": True}}

# ==========================
# Ko'p adminli tizim
# ==========================
ADMINS_FILE = "admins.json"
SUPER_ADMIN_ID = 8230858921  # Bosh admin — adminlarni boshqaradi

def load_admins():
    try:
        with open(ADMINS_FILE, "r") as f:
            return set(json.load(f))
    except (FileNotFoundError, json.JSONDecodeError):
        return {SUPER_ADMIN_ID}

def save_admins():
    with open(ADMINS_FILE, "w") as f:
        json.dump(list(admins), f)

admins = load_admins()  # Barcha adminlar ID si

def is_admin(user_id):
    return user_id in admins or user_id == SUPER_ADMIN_ID

def is_super_admin(user_id):
    return user_id == SUPER_ADMIN_ID

teachers_data = {
    "📗 Matematika": {
        "Bozorov Mansurbek": {
            "info": """📚 Matematika

🗂 Oliy toifali o'qituvchi

📊 +7 yillik tajriba

📈O'z fanini bilish sertifikatlari:
  🔹 Milliy sertifikat A+
  🔹 GRE xalqaro sertifikat 158

📞O'qituvchi bilan bog'lanish:
    ☎️ +998939098865
    📲 @bozorovmansurbek""",
            "photo": "images/bozorovmansurbek.jpg"
        },
        "Ashurov Akmal": {
            "info": """📚 Matematika

🗂 Birinchi toifali o'qituvchi

📊 +4 yillik tajriba

📈O'z fanini bilish sertifikatlari:
  🔹 Milliy sertifikat A
  🔹 GRE xalqaro sertifikat 160

📞O'qituvchi bilan bog'lanish:
    ☎️ +998991140596
    📲 t.me/+998991140596""",
            "photo": "images/ashurovakmal.jpg"
        },
        "Eshmatov Zafar": {
            "info": """📚 Matematika

🗂 Birinchi toifali o'qituvchi

📊 +10 yillik tajriba

📈O'z fanini bilish sertifikatlari:
  🔹 Milliy sertifikati A+
  🔹 Xalqaro GRE sertifikati 159 ball
  
📞O'qituvchi bilan bog'lanish:
    ☎️ +998995572539
    📲 t.me/+998995572539""",
            "photo": "images/eshmatovzafar.jpg"
        },
        "Abdusattorova Marjona": {
            "info": """📚 Matematika

🗂 Oliy toifali o'qituvchi

📊 +6 yillik tajriba

📈O'z fanini bilish sertifikatlari:
    🔹 Milliy sertifikati B+
    🔹 SAT xalqaro sertifikati 760

📞O'qituvchi bilan bog'lanish:
    ☎️ +998906698797
    📲 @marjona_abdusattorova""",
            "photo": "images/abdusattorovamarjona.jpg"
        },
        "Tojiyeva Zamira": {
            "info": """📚 Matematika

🗂 Birinchi toifali o'qituvchi

📊 +11 yillik tajriba

📈O'z fanini bilish sertifikatlari:
    🔹SAT xalqaro sertifikati 770
    🔹 Milliy sertifikat B+

📞O'qituvchi bilan bog'lanish:
☎️ +998945294404
📲 t.me/+998945294404""",
            "photo": "images/tojiyevazamira.jpg"
        },
        "Nazarov Farrux": {
            "info": """📚 Matematika

🗂 Birinchi toifali o'qituvchi

📊 +6 yillik tajriba

📈O'z fanini bilish sertifikatlari:
    🔹GMAT xalqaro sertifikati 41

📞O'qituvchi bilan bog'lanish:
    ☎️ +998996663267
    📲 @FarruxNazarov3267""",
            "photo": "images/nazarovfarrux.jpg"
        },
        "Daynovov Hasan": {
            "info": """📚 Matematika

🗂 Ikkinchi toifali o'qituvchi

📊 +7 yillik tajriba

📈O'z fanini bilish sertifikatlari:
    🔹SAT xalqaro sertifikati 740 
    🔹Milliy Sertifikat A

📞O'qituvchi bilan bog'lanish:
    ☎️ +998919560359
    📲 @H_Daynovov""",
            "photo": "images/daynovovhasan.jpg"
        },
        "Abzoirova Madina": {
            "info": """📚 Matematika

🗂 Birinchi toifali o'qituvchi

📊 +7 yillik tajriba

📈O'z fanini bilish sertifikatlari:
    🔹SAT xalqaro sertifikati 760
    🔹Milliy sertifikat A

📞O'qituvchi bilan bog'lanish:
    ☎️ +998932502807
    📲 t.me/+998932502807""",
            "photo": "images/abzoirovamadina.jpg"
        },
        "Bahromov Ozodbek": {
            "info": """📚 Matematika

🗂 Oliy toifali o'qituvchi

📊 +4 yillik tajriba

📈O'z fanini bilish sertifikatlari:
    🔹Milliy sertifikat A+
    🔹GRE xalqaro sertifikati 157

📞O'qituvchi bilan bog'lanish:
    ☎️ +998996652023
    📲 t.me/+998996652023""",
            "photo": "images/bahromovozodbek.jpg"
        },
        "Abdivayidov Erkin": {
            "info": """📚 Matematika

🗂 Oliy toifali o'qituvchi

📊 +6 yillik tajriba

📈O'z fanini bilish sertifikatlari:
    🔹Milliy sertifikat B+
    🔹GRE xalqaro sertifikati 155

📞O'qituvchi bilan bog'lanish:
    ☎️ +998993340657
    📲 t.me/+998993340657""",
            "photo": "images/abduvayidoverkin.jpg"
        },
        "Azimov Jasur": {
            "info": """📚 Matematika

🗂 Birinchi toifali o'qituvchi

📊 +6 yillik tajriba

📈O'z fanini bilish sertifikatlari:
    🔹Milliy sertifikat A+
    🔹GRE xalqaro sertifikati 161

📞O'qituvchi bilan bog'lanish:
    ☎️ +998996793397
    📲 @JasurbekAzimov13""",
            "photo": "images/azimovjasur.jpg"
        },
        "Abduzairova Mashhura": {
            "info": """📚 Matematika

🗂 Oliy toifali o'qituvchi

📊 +8 yillik tajriba

📈O'z fanini bilish sertifikatlari:
 🔹Milliy sertifikat A+
 🔹GRE xalqaro sertifikati 165

📞O'qituvchi bilan bog'lanish:
    ☎️ +998996639514
    📲 t.me/+998996639514""",
            "photo": "images/abduzayirovamashhura.jpg"
        }
    },
    "📗 Fizika": {
        "Soatov Odil": {
            "info": """📚 Fizika

🗂 Oliy toifali o'qituvchi

📊 +8 yillik tajriba

📈O'z fanini bilish sertifikatlari:
    🔹Milliy sertifikati B+

📞O'qituvchi bilan bog'lanish:
    ☎️ +998996602069
    📲 t.me/+998996602069""",
            "photo": "images/soatovodil.jpg"
        },
        "Boltayev Alisher": {
            "info": """📚Fizika

🗂 Oliy toifali o'qituvchi

📊 +3 yillik tajriba

📈O'z fanini bilish sertifikatlari:
    🔹Milliy sertifikati A

📞O'qituvchi bilan bog'lanish:
☎️ +998993654306
📲 @Alisher_Boltayev""",
            "photo": "images/boltayevalisher.jpg"
        },
        "Isomiddinov Zayniddin": {
            "info": """📚 Fizika

🗂 Oliy toifali o'qituvchi

📊 +5 yillik tajriba

📈O'z fanini bilish sertifikatlari:
    🔹Milliy sertifikat B+
    🔹GRE xalqaro sertifikati 750
    🔹Matematika fanidan Milliy sertifikat A

📞O'qituvchi bilan bog'lanish:
    ☎️ +998996629860
    📲 @Zayniddin_Isomiddinov""",
            "photo": "images/isomiddinovzayniddin.jpg"
        },
        "Bobomuratov Allanazar": {
            "info": """📚 Fizika

🗂 Oliy toifali o'qituvchi

📊 +5 yillik tajriba

📈O'z fanini bilish sertifikatlari:
    🔹Fizika fanidan Milliy sertifikat A+

📞O'qituvchi bilan bog'lanish:
    ☎️ +998919516796
    📲 t.me/+998919516796""",
            "photo": "images/bobomuratovallanazar.jpg"
        },
        "Cho'lliyeva Shohsanam": {
            "info": """📚 Fizika

🗂 Birinchi toifali o'qituvchi

📊 +11 yillik tajriba

📞O'qituvchi bilan bog'lanish:
    ☎️ +998940384449
    📲 t.me/+998940384449""",
            "photo": "images/chulliyevashohsanam.jpg"
        }
    },
    "📗 Ona tili va adabiyot": {
        "Kabilov Nuriddin": {
            "info": """📚 Ona tili va Adabiyot

🗂 Oliy toifali o'qituvchi

📊 +14 yillik tajriba

📈O'z fanini bilish sertifikatlari:
    🔹Milliy sertifikat B+
    
📞O'qituvchi bilan bog'lanish:
    ☎️ +998906089337
    📲 t.me/+998906089337""",
            "photo": "images/kabilovnuriddin.jpg"
        },
        "Xamrayeva Nilufar": {
            "info": """📚 Ona tili va Adabiyot

🗂️ Oliy toifali o'qituvchi

📊 +23 yillik tajriba

📈O'z fanini bilish sertifikatlari:
    🔹Milliy sertifikat A

📞O'qituvchi bilan bog'lanish:
    ☎️ +998996862602
    📲 t.me/+998996862602""",
            "photo": "images/xamrayevanilufar.jpg"
        },
        "Mirzayeva Saodat": {
            "info": """📚 Ona tili va Adabiyot

🗂 Birinchi toifali o'qituvchi

📊 +24 yillik tajriba

📈O'z fanini bilish sertifikatlari:
    🔹Milliy sertifikat B+

📞O'qituvchi bilan bog'lanish:
    ☎️ +998999410280
    📲 @Soadatmirzayeva""",
            "photo": "images/mirzayevasaodat.jpg"
        }
    },
    "📗 Rus tili": {
        "Mitanova Go'zal": {
            "info": """📚 Rus tili

🗂 Oliy toifali o'qituvchi

📊 +37 yillik tajriba

📈O'z fanini bilish sertifikatlari:
    🔹TRKI xalqaro sertifikati C1

📞O'qituvchi bilan bog'lanish:
    ☎️ +998997068370
    📲 @MITANOVA_G""",
            "photo": "images/mitanovaguzal.jpg"
        },
        "Choriyeva Oysifat": {
            "info": """📚 Rus tili

🗂 Oliy toifali o'qituvchi

📊 +34 yillik tajriba

📈O'z fanini bilish sertifikatlari:
    🔹Milliy sertifikati A+
    🔹TRKI xalqaro sertifikati C1
    
📞O'qituvchi bilan bog'lanish:
    ☎️ +998991652050
    📲 t.me/+998991652050""",
            "photo": "images/choriyevaoysifat.jpg"
        },
        "Nurmatova Ra'no": {
            "info": """📚 Rus tili

🗂 Birinchi toifali o'qituvchi

📊 +32 yillik tajriba

📈O'z fanini bilish sertifikatlari:
    🔹TRKI xalqaro sertifikati C1

📞O'qituvchi bilan bog'lanish:
    ☎️ +998990211472
    📲 t.me/+998990211472""",
            "photo": "images/nurmatovarano.jpg"
        }
    },
    "📗 Ingliz tili": {
        "Nurmatov Nurkeldi": {
            "info": """📚 Ingliz tili

🗂 Birinchi toifali o'qituvchi

📊 +6 yillik tajriba

📈O'z fanini bilish sertifikatlari:
    🔹CEFR C1
    🔹IELTS 6.5

📞O'qituvchi bilan bog'lanish:
    ☎️ +998990229617
    📲 t.me/+998990229617""",
            "photo": "images/nurmatovnurkeldi.jpg"
        },
        "Amanqulova Yulduz": {
            "info": """📚 Ingliz tili

🗂 Birinchi toifali o'qituvchi

📊 +13 yillik tajriba

📈O'z fanini bilish sertifikatlari:
    🔹CEFR B2
    🔹TKT 3 ta modul

📞O'qituvchi bilan bog'lanish:
    ☎️ +998945233113
    📲 t.me/+998945233113""",
            "photo": "images/amanqulovayulduz.jpg"
        },
        "Tashmatova Aziza": {
            "info": """📚 Ingliz tili

🗂 Oliy toifali o'qituvchi

📊 +9 yillik tajriba

📈O'z fanini bilish sertifikatlari:
    🔹CEFR B2 
    🔹TKT 3 ta modul

📞O'qituvchi bilan bog'lanish:
    ☎️ +998930700765
    📲 @sinora3009""",
            "photo": "images/tashmatovaaziza.jpg"
        },
        "Normo'minova Zebiniso": {
            "info": """📚 Ingliz tili

🗂 Oliy toifali o'qituvchi

📊 +4 yillik tajriba

📈O'z fanini bilish sertifikatlari:
    🔹IELTS 7

📞O'qituvchi bilan bog'lanish:
    ☎️ +998919581499
    📲 t.me/+998919581499""",
            "photo": "images/normuminovazebiniso.jpg"
        },
        "Qoraxonova Muhayyo": {
            "info": """📚 Ingliz tili

🗂 Ikkinchi toifali o'qituvchi

📊 +2 yillik tajriba

📈O'z fanini bilish sertifikatlari:
    🔹TKT 3ta modul

📞O'qituvchi bilan bog'lanish:
    ☎️ +998931021798
    📲 t.me/+998931021798""",
            "photo": "images/qoraxonovamuhayyo.jpg"
        },
        "Qarshiyev Akbar": {
            "info": """📚 Ingliz tili

🗂 Oliy toifali o'qituvchi

📊 +4 yillik tajriba

📈O'z fanini bilish sertifikatlari:
    🔹CEFR B2
    🔹TKT 3 ta modul
📞O'qituvchi bilan bog'lanish:
    ☎️ +998990631723
    📲 t.me/+998990631723""",
            "photo": "images/qarshiyevakbar.jpg"
        }
    },
    "📗 Tarix, Tarbiya": {
        "Xudoyqulov Samariddin": {
            "info": """📚 Tarix va Tarbiya

🗂 Oliy toifali o'qituvchi

📊 +13 yillik tajriba

📈O'z fanini bilish sertifikatlari:
    🔹Milliy sertifikati A+

📞 O'qituvchi bilan bog'lanish:
    ☎️ +998932471317
    📲 @SamariddinXudoyqulov""",
            "photo": "images/xudoyqulovsamariddin.jpg"
        },
        "Jaylovov Komil": {
            "info": """📚 Tarix va Tarbiya

🗂 Oliy toifali o'qituvchi

📊 +5 yillik tajriba

📈O'z fanini bilish sertifikatlari:
    🔹Milliy sertifikati A+

📞O'qituvchi bilan bog'lanish:
    ☎️ +998942929213
    📲 t.me/+998942929213""",
            "photo": "images/jaylovovkomil.jpg"
        },
        "Eshmamatov Alizod": {
            "info": """📚 Tarix va Tarbiya

🗂 Oliy toifali o'qituvchi

📊 +6 yillik tajriba

📈O'z fanini bilish sertifikatlari:
    🔹Milliy sertifikati A+

📞O'qituvchi bilan bog'lanish:
    ☎️ +998945277742
    📲 t.me/+998945277742""",
            "photo": "images/eshmamatovalizod.jpg"
        }
    },
    "📗 Informatika": {
        "Jabborov Ilhom": {
            "info": """📚 Informatika

🗂 Oliy toifali o'qituvchi

📊 +15 yillik tajriba

📈O'z fanini bilish sertifikatlari:
    🔹Google xalqaro sertifikati level 2

📞O'qituvchi bilan bog'lanish:
    ☎️ +998974502807
    📲 @Ilhom8501""",
            "photo": "images/jabborovilhom.jpg"
        },
        "Ko'chimov Farxod": {
            "info": """📚 Informatika

🗂 Oliy toifali o'qituvchi

📊 +5 yillik tajriba

📈O'z fanini bilish sertifikatlari: 
    🔹MCE xalqaro sertifikati 952
    🔹Astrum 114

📞O'qituvchi bilan bog'lanish:
    ☎️ +998902888832
    📲 t.me/+998902888832""",
            "photo": "images/kuchimovfarxod.jpg"
        },
        "Tojiyev Sardor": {
            "info": """📚 Informatika va Sun'iy intellekt

🗂 Ikkinchi toifali o'qituvchi

📊 +1 yillik tajriba

📈O'z fanini bilish sertifikatlari:
    🔹CEFR B2

📞O'qituvchi bilan bog'lanish:
    ☎️ +998938306888
    📲 @developer_071""",
            "photo": "images/tojiyevsardor.jpg"
        }
    },
    "📗 Robotexnika va AI": {
        "Tojiyev Sardor": {
            "info": """📚 Robotexnika va Sun'iy intellekt, Informatika

🗂 Ikkinchi toifali o'qituvchi

📊 +1 yillik tajriba

📈O'z fanini bilish sertifikatlari:
    🔹CEFR B2

📞O'qituvchi bilan bog'lanish:
    ☎️ +998938306888
    📲 @developer_071""",
            "photo": "images/tojiyevsardor.jpg"
        }
    },
    "📗 Biologiya": {
        "Qosimova Nigora": {
            "info": """📚 Biologiya, Sciense

🗂 Oliy toifali o'qituvchi

📊 +18 yillik tajriba

📞O'qituvchi bilan bog'lanish:
    ☎️ +998999459025
    📲 t.me/+998999459025""",
            "photo": "images/qosimovanigora.jpg"
        },
        "Jumayeva Shoxsanam": {
            "info": """📚 Biologiya, Sciense

🗂 Oliy toifali o'qituvchi

📊 +8 yillik tajriba

📈O'z fanini bilish sertifikatlari:
    🔹Milliy sertifikat B+

📞O'qituvchi bilan bog'lanish:
    ☎️ +998990964567
    📲 t.me/+998990964567""",
            "photo": "images/jumayevashohsanam.jpg"
        }
    },
    "📗 Science": {
        "Tojiyev Abubakir": {
            "info": """📚 Geografiya, Sciense

🗂 Oliy toifali o'qituvchi

📊 +3 yillik tajriba

📈O'z fanini bilish sertifikatlari:
    🔹Milliy sertifikati A+

📞O'qituvchi bilan bog'lanish:
    ☎️ +998500010402
    📲 t.me/+998500010402""",
            "photo": "images/tojiyevabubakir.jpg"
        },
        "Qosimova Nigora": {
            "info": """📚 Biologiya, Sciense

🗂 Oliy toifali o'qituvchi

📊 +18 yillik tajriba

📞O'qituvchi bilan bog'lanish:
    ☎️ +998999459025
    📲 t.me/+998999459025""",
            "photo": "images/qosimovanigora.jpg"
        },
    },
    "📗 Geografiya": {
        "Tojiyev Abubakir": {
            "info": """📚 Geografiya, Sciense

🗂 Oliy toifali o'qituvchi

📊 +3 yillik tajriba

📈O'z fanini bilish sertifikatlari:
    🔹Milliy sertifikati A+

📞O'qituvchi bilan bog'lanish:
    ☎️ +998500010402
    📲 t.me/+998500010402""",
            "photo": "images/tojiyevabubakir.jpg"
        },
    },
    "📗 Kimyo": {
        "Bektoshev Nurkomil": {
            "info": """📚 Kimyo

🗂 Oliy toifali o'qituvchi

📊 +5 yillik tajriba

📈O'z fanini bilish sertifikatlari:
    🔹Milliy sertifikati A

📞O'qituvchi bilan bog'lanish:
    ☎️ +998943393398
    📲 t.me/+998943393398""",
            "photo": "images/bektoshovnurkomil.jpg"
        }
    },
    "📗 Jismoniy Tarbiya": {
        "Berdiqulov Shavkat": {
            "info": """📚 Jismoniy tarbiya

🗂 Oliy toifali o'qituvchi

📊 +25 yillik tajriba

📞O'qituvchi bilan bog'lanish:
    ☎️ +998919560095
    📲 t.me/+998919560095""",
            "photo": "images/berdiqulovshavkat.jpg"
        },
        "Xolmahmatov Anvar": {
            "info": """📚 Jismoniy tarbiya

🗂 Ikkinchi toifali o'qituvchi

📊 +15 yillik tajriba

📞O'qituvchi bilan bog'lanish:
    ☎️ +998997739183
    📲 t.me/+998997739183""",
            "photo": "images/xolmahmatovanvarjon.jpg"
        }
    },
    "📗 San'at(Art)": {
        "Ashurov Suhrob": {
            "info": """📚Tasviriy san'at, Chizmachilik

🗂 Mutaxassis

📊 +3 yillik tajriba

📞O'qituvchi bilan bog'lanish:
    ☎️ +998939073128
    📲 t.me/+998939073128""",
            "photo": "images/ashurovsuhrob.jpg"
        }
    }
}

# ==========================================
# teachers_info — ro'yxat + index yordamida
# ==========================================
teachers_info_list = [
    {
        "label": "👨‍🏫 Maktab Direktori: Qurbonov Jaloliddin",
        "phone": "+998902883510",
        "username": "jaloliddinibadullayevich",
        "photo": "images/qurbanovjaloliddin.jpg"
    },
    {
        "label": "👨‍🏫 O'IBDO': Hazratov Qo'yli",
        "phone": "+998905226167",
        "username": "Hazratov_Q",
        "photo": "images/hazratovquyli.png"
    },
    {
        "label": "👨‍🏫 XIBDO': Baymirzayev Dilshod",
        "phone": "+998943354483",
        "username": "Dilshod_Baymirzayev",
        "photo": "images/baymirzayevdilshod.jpg"
    },
    {
        "label": "👩‍🏫 MMIBDO': Gulhayo Ismoilova",
        "phone": "+998991984777",
        "username": "ignortojiyevna",
        "photo": "images/ismailovagulhayo.jpg"
    },
    {
        "label": "👨‍🏫 ChQBT: Utamuradov Zafar",
        "phone": "+998939438900",
        "username": "Z8999R",
        "photo": "images/utamurodovzafar.jpg"
    },
    {
        "label": "👩‍🏫 Kadrlar bo'yicha menedjer: Mustafayeva Farida",
        "phone": "+998942959828",
        "username": "faridamaratovna",
        "photo": "images/kotiba.jpg"
    },
    {
        "label": "👩‍🏫 Kutubxona mudirasi: Tog'ayeva Nodira",
        "phone": "+998990261576",
        "username": "",
        "photo": "images/kutubxonachi.jpg"
    }
]

kanal = ['@Dehqonobod_Ixtisoslashtirilgan_M']
CHANNEL_USERNAME = kanal[0]

TOKEN = "8216327788:AAEet4-zyAIAhMDVi_6PejDeLsPsuUvaXa4"
bot = TeleBot(TOKEN)


# ==========================
# Obuna tekshirish
# ==========================
def obuna_tekshir():
    jb = types.InlineKeyboardMarkup(row_width=1)
    jb.add(types.InlineKeyboardButton(
        "📢Kanalga obuna bo'lish.",
        url=f"https://t.me/{kanal[0].lstrip('@')}"
    ))
    jb.add(types.InlineKeyboardButton("✅Obunani tekshirish", callback_data='check_sub'))
    return jb


@bot.message_handler(commands=['start'])
def salomlash(message):
    text = ("Assalomu alaykum!\n"
            "Botdan foydalanish uchun kanalimizga obuna bo'ling:")
    bot.send_message(message.chat.id, text, reply_markup=obuna_tekshir())


@bot.callback_query_handler(func=lambda c: c.data == "check_sub")
def obunani_aniqlash(call):
    user_id = call.from_user.id
    try:
        member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
        if member.status in ("creator", "administrator", "member", "restricted"):
            bot.answer_callback_query(call.id, "✅ Obuna tasdiqlandi!")
            bot.send_message(
                call.message.chat.id,
                "🎉 Tabirkaymiz! Siz kanalga obuna bo'lgansiz.",
                reply_markup=tugmalar(call.from_user.id)
            )
        else:
            bot.answer_callback_query(call.id, "❌ Obuna topilmadi.")
            bot.send_message(
                call.message.chat.id,
                "Siz kanalga obuna bo'lmagansiz! Iltimos, obuna bo'ling.",
                reply_markup=obuna_tekshir()
            )
    except Exception as e:
        bot.answer_callback_query(call.id, "Xato!")
        bot.send_message(call.message.chat.id, f"Tekshirishda xatolik yuz berdi.\nXato: {e}")


# ==========================
# Klaviaturalar
# ==========================
def tugmalar(user_id=None):
    tugma = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    tugma.add(
        types.KeyboardButton("🏫 Maktab haqida"),
        types.KeyboardButton("🚪 Maktabga qabul qilish tartibi")
    )
    tugma.add(
        types.KeyboardButton("⁉️ E'tiroz va takliflar"),
        types.KeyboardButton("👨‍🏫 O'qituvchilar")
    )
    tugma.add(
        types.KeyboardButton("📢 Telegram kanal"),
        types.KeyboardButton("📞 Rahbariyat bilan aloqa")
    )
    if user_id and is_admin(user_id):
        tugma.add(types.KeyboardButton("⚙️ Admin panel"))
    return tugma


def admin_panel_kb(user_id=None):
    kb = types.InlineKeyboardMarkup(row_width=1)
    kb.add(types.InlineKeyboardButton("📢 Xabar yuborish", callback_data="admin_broadcast"))
    kb.add(types.InlineKeyboardButton("👥 Foydalanuvchilar soni", callback_data="admin_usercount"))
    if user_id and is_super_admin(user_id):
        kb.add(types.InlineKeyboardButton("➕ Admin qo'shish", callback_data="admin_add"))
        kb.add(types.InlineKeyboardButton("➖ Admin o'chirish", callback_data="admin_remove"))
        kb.add(types.InlineKeyboardButton("📋 Adminlar ro'yxati", callback_data="admin_list"))
    return kb


def broadcast_action_kb():
    kb = types.InlineKeyboardMarkup(row_width=2)
    kb.add(
        types.InlineKeyboardButton("✅ Yuborish", callback_data="broadcast_send"),
        types.InlineKeyboardButton("❌ Bekor qilish", callback_data="broadcast_cancel")
    )
    return kb


# ==========================
# ASOSIY ROUTER - matn xabarlar
# ==========================
@bot.message_handler(content_types=['text'])
def router(message):
    all_users.add(message.chat.id)
    save_users()  # ✅ Faylga saqlash
    user_text = message.text.strip()
    user_id = message.chat.id

    # ❌ Agar foydalanuvchi savol jarayonidaydi
    if user_states.get(user_id) == "waiting_for_question":
        if user_text in ["🏫 Maktab haqida", "⁉️ E'tiroz va takliflar",
                        "👨‍🏫 O'qituvchilar", "📢 Telegram kanal", "📞 Rahbariyat bilan aloqa",
                        "🚪 Maktabga qabul qilish tartibi", "⬅️ Asosiy menyu", "⚙️ Admin panel"]:
            user_states.pop(user_id, None)
            return router(message)
        else:
            return send_question_to_teacher(message)

    if is_admin(message.from_user.id) and message.chat.id in pending_broadcast:
        return collect_broadcast_message(message)

    if user_text == "🏫 Maktab haqida":
        user_states.pop(user_id, None)
        return school_about(message)

    elif user_text == "⁉️ E'tiroz va takliflar":
        user_states[user_id] = "waiting_for_question"
        return questions(message)

    elif user_text == "👨‍🏫 O'qituvchilar":
        user_states.pop(user_id, None)
        return teachers(message)

    elif user_text in teachers_data:
        user_states.pop(user_id, None)
        user_fan[message.chat.id] = user_text
        return teachers_by_fan(message, user_text)

    elif user_text == "🔙 Orqaga":
        user_states.pop(user_id, None)
        return teachers(message)

    elif user_text == "⬅️ Asosiy menyu":
        user_states.pop(user_id, None)
        bot.send_message(
            message.chat.id,
            "🏠 Asosiy menyu",
            reply_markup=tugmalar(message.from_user.id)
        )

    elif user_text == "⚙️ Admin panel":
        user_states.pop(user_id, None)
        if is_admin(message.from_user.id):
            bot.send_message(message.chat.id, "🔐 Admin panel:", reply_markup=admin_panel_kb(message.from_user.id))
        else:
            bot.send_message(message.chat.id, "❌ Sizda ruxsat yo'q!")

    elif message.chat.id in user_fan and user_text in teachers_data.get(user_fan[message.chat.id], {}):
        user_states.pop(user_id, None)
        return teacher_info(message, user_fan[message.chat.id], user_text)

    elif user_text == "📢 Telegram kanal":
        user_states.pop(user_id, None)
        return channel(message)

    elif user_text == "📞 Rahbariyat bilan aloqa":
        user_states.pop(user_id, None)
        return communication(message)

    elif user_text == "🚪 Maktabga qabul qilish tartibi":
        user_states.pop(user_id, None)
        return acceptance(message)

    else:
        if not user_text.startswith('/'):
            bot.send_message(
                message.chat.id,
                "Boshqa savollaringiz bo'lsa, ⁉️E'tiroz va takliflar bo'limiga yozishingiz mumkin."
            )


# ==========================
# MEDIA ROUTER
# ==========================
@bot.message_handler(content_types=['photo', 'video', 'document', 'audio',
                                     'voice', 'sticker', 'animation', 'video_note'])
def media_router(message):
    all_users.add(message.chat.id)
    save_users()  # ✅ Faylga saqlash
    if is_admin(message.from_user.id) and message.chat.id in pending_broadcast:
        return collect_broadcast_message(message)


# ==========================
# BROADCAST
# ==========================
@bot.callback_query_handler(func=lambda call: call.data in (
    "admin_broadcast", "admin_usercount", "broadcast_send", "broadcast_cancel",
    "admin_add", "admin_remove", "admin_list"
))
def admin_panel_handler(call):
    if not is_admin(call.from_user.id):
        bot.answer_callback_query(call.id, "❌ Ruxsat yo'q!")
        return

    if call.data == "admin_usercount":
        bot.answer_callback_query(call.id)
        bot.send_message(
            call.message.chat.id,
            f"👥 Jami foydalanuvchilar: {len(all_users)} ta"
        )

    elif call.data == "admin_list":
        if not is_super_admin(call.from_user.id):
            bot.answer_callback_query(call.id, "❌ Faqat bosh admin!")
            return
        bot.answer_callback_query(call.id)
        if len(admins) == 0:
            text = "📋 Adminlar ro'yxati bo'sh."
        else:
            lines = ["📋 *Adminlar ro'yxati:*\n"]
            for i, aid in enumerate(admins, 1):
                marker = "👑" if aid == SUPER_ADMIN_ID else "👤"
                lines.append(f"{i}. {marker} `{aid}`")
            text = "\n".join(lines)
        bot.send_message(call.message.chat.id, text, parse_mode="Markdown",
                         reply_markup=admin_panel_kb(call.from_user.id))

    elif call.data == "admin_add":
        if not is_super_admin(call.from_user.id):
            bot.answer_callback_query(call.id, "❌ Faqat bosh admin!")
            return
        bot.answer_callback_query(call.id)
        msg = bot.send_message(
            call.message.chat.id,
            "➕ Yangi admin ID sini yuboring:\n(Foydalanuvchi botga /start bosishi kerak)"
        )
        bot.register_next_step_handler(msg, process_add_admin)

    elif call.data == "admin_remove":
        if not is_super_admin(call.from_user.id):
            bot.answer_callback_query(call.id, "❌ Faqat bosh admin!")
            return
        bot.answer_callback_query(call.id)
        removable = [aid for aid in admins if aid != SUPER_ADMIN_ID]
        if not removable:
            bot.send_message(call.message.chat.id, "❌ O'chirish uchun admin yo'q.",
                             reply_markup=admin_panel_kb(call.from_user.id))
            return
        kb = types.InlineKeyboardMarkup(row_width=1)
        for aid in removable:
            kb.add(types.InlineKeyboardButton(f"🗑 {aid}", callback_data=f"del_admin|{aid}"))
        kb.add(types.InlineKeyboardButton("❌ Bekor qilish", callback_data="admin_cancel"))
        bot.send_message(call.message.chat.id, "➖ O'chirmoqchi bo'lgan adminni tanlang:", reply_markup=kb)

    elif call.data == "admin_broadcast":
        bot.answer_callback_query(call.id)
        pending_broadcast[call.from_user.id] = {"messages": [], "album_groups": {}}
        bot.send_message(
            call.message.chat.id,
            "📢 *Broadcast rejimi yoqildi!*\n\n"
            "Endi xabarlaringizni yuboring:\n"
            "• ✏️ Matn\n"
            "• 🖼 Rasm (caption bilan yoki bepul)\n"
            "• 🖼🖼 Albom (bir necha rasm ketma-ket)\n"
            "• 🎥 Video\n"
            "• 📄 Fayl / Hujjat\n"
            "• 🎵 Audio, 🎤 Ovozli xabar\n"
            "• ↩️ Forward xabar\n\n"
            "Hammasi tayyor bo'lgach '✅ Yuborish' bosing.",
            parse_mode="Markdown",
            reply_markup=broadcast_action_kb()
        )

    elif call.data == "broadcast_send":
        bot.answer_callback_query(call.id)
        data = pending_broadcast.get(call.from_user.id)
        if not data or not data["messages"]:
            bot.send_message(call.message.chat.id, "❌ Hali hech qanday xabar yuborilmagan!")
            return
        msgs = data["messages"]
        pending_broadcast.pop(call.from_user.id, None)
        do_broadcast(call.message.chat.id, msgs, call.from_user.id)

    elif call.data == "broadcast_cancel":
        bot.answer_callback_query(call.id)
        pending_broadcast.pop(call.from_user.id, None)
        bot.send_message(
            call.message.chat.id,
            "❌ Broadcast bekor qilindi.",
            reply_markup=admin_panel_kb(call.from_user.id)
        )


def process_add_admin(message):
    if not is_super_admin(message.from_user.id):
        return
    try:
        new_id = int(message.text.strip())
        if new_id in admins:
            bot.send_message(message.chat.id, f"⚠️ {new_id} allaqachon admin!",
                             reply_markup=admin_panel_kb(message.from_user.id))
        else:
            admins.add(new_id)
            save_admins()
            bot.send_message(message.chat.id, f"✅ {new_id} admin qilindi!",
                             reply_markup=admin_panel_kb(message.from_user.id))
            # Yangi adminga xabar yuborish
            try:
                bot.send_message(new_id, "🎉 Siz admin qilindingiz!\n⚙️ Admin paneldan foydalanishingiz mumkin.",
                                 reply_markup=tugmalar(new_id))
            except Exception:
                pass
    except ValueError:
        bot.send_message(message.chat.id, "❌ Noto'g'ri ID! Faqat raqam kiriting.",
                         reply_markup=admin_panel_kb(message.from_user.id))


@bot.callback_query_handler(func=lambda call: call.data.startswith("del_admin|"))
def delete_admin_callback(call):
    if not is_super_admin(call.from_user.id):
        bot.answer_callback_query(call.id, "❌ Faqat bosh admin!")
        return
    try:
        target_id = int(call.data.split("|")[1])
        if target_id == SUPER_ADMIN_ID:
            bot.answer_callback_query(call.id, "❌ Bosh adminni o'chirib bo'lmaydi!")
            return
        admins.discard(target_id)
        save_admins()
        bot.answer_callback_query(call.id, f"✅ {target_id} admin o'chirildi!")
        bot.edit_message_text(
            f"✅ {target_id} admin ro'yxatidan o'chirildi.",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=admin_panel_kb(call.from_user.id)
        )
        # O'chirilgan adminga xabar yuborish
        try:
            bot.send_message(target_id, "⚠️ Siz admin ro'yxatidan o'chirildingiz.",
                             reply_markup=tugmalar(target_id))
        except Exception:
            pass
    except (ValueError, IndexError):
        bot.answer_callback_query(call.id, "Xatolik!")


@bot.callback_query_handler(func=lambda call: call.data == "admin_cancel")
def admin_cancel_callback(call):
    bot.answer_callback_query(call.id)
    bot.edit_message_text("❌ Bekor qilindi.", call.message.chat.id, call.message.message_id,
                          reply_markup=admin_panel_kb(call.from_user.id))


def collect_broadcast_message(message):
    data = pending_broadcast.get(message.from_user.id)
    if not data:
        return

    media_group_id = getattr(message, "media_group_id", None)

    if media_group_id:
        groups = data.setdefault("album_groups", {})
        item = {}
        if message.content_type == "photo":
            item = {
                "content_type": "photo",
                "file_id": message.photo[-1].file_id,
                "caption": message.caption,
                "caption_entities": message.caption_entities,
            }
        elif message.content_type == "video":
            item = {
                "content_type": "video",
                "file_id": message.video.file_id,
                "caption": message.caption,
                "caption_entities": message.caption_entities,
            }

        if media_group_id not in groups:
            groups[media_group_id] = []
            album_entry = {
                "content_type": "album",
                "media_group_id": media_group_id,
                "items": groups[media_group_id],
            }
            data["messages"].append(album_entry)

        groups[media_group_id].append(item)
        total = len(groups[media_group_id])
        bot.send_message(
            message.chat.id,
            f"🖼 Albomga {total}-rasm qo'shildi.\nHali ko'proq rasm yuborsangiz yoki '✅ Yuborish' bosing.",
            reply_markup=broadcast_action_kb()
        )
        return

    msg_info = {"content_type": message.content_type}

    if message.content_type == "text":
        msg_info["text"] = message.text
        msg_info["entities"] = message.entities
    elif message.content_type == "photo":
        msg_info["file_id"] = message.photo[-1].file_id
        msg_info["caption"] = message.caption
        msg_info["caption_entities"] = message.caption_entities
    elif message.content_type == "video":
        msg_info["file_id"] = message.video.file_id
        msg_info["caption"] = message.caption
        msg_info["caption_entities"] = message.caption_entities
    elif message.content_type == "document":
        msg_info["file_id"] = message.document.file_id
        msg_info["caption"] = message.caption
        msg_info["caption_entities"] = message.caption_entities
    elif message.content_type == "audio":
        msg_info["file_id"] = message.audio.file_id
        msg_info["caption"] = message.caption
    elif message.content_type == "voice":
        msg_info["file_id"] = message.voice.file_id
    elif message.content_type == "video_note":
        msg_info["file_id"] = message.video_note.file_id
    elif message.content_type == "sticker":
        msg_info["file_id"] = message.sticker.file_id
    elif message.content_type == "animation":
        msg_info["file_id"] = message.animation.file_id
        msg_info["caption"] = message.caption

    data["messages"].append(msg_info)
    count = len(data["messages"])
    bot.send_message(
        message.chat.id,
        f"✅ Xabar #{count} qabul qilindi ({message.content_type})\n\n"
        f"Yana xabar yuboring yoki '✅ Yuborish' bosing.",
        reply_markup=broadcast_action_kb()
    )


def do_broadcast(admin_chat_id, messages, admin_id=None):
    success = 0
    fail = 0
    for user_id in all_users:
        try:
            for msg in messages:
                send_one_message(user_id, msg)
            success += 1
        except Exception:
            fail += 1

    bot.send_message(
        admin_chat_id,
        f"✅ Broadcast muvaffaqiyatli yakunlandi!\n\n"
        f"📨 Xabar turlari soni: {len(messages)} ta\n"
        f"👍 Muvaffaqiyatli yuborildi: {success} ta\n"
        f"❌ Yuborilmadi: {fail} ta",
        reply_markup=admin_panel_kb(admin_id)
    )


def send_one_message(user_id, msg):
    ct = msg.get("content_type")

    if ct == "text":
        bot.send_message(user_id, msg["text"], entities=msg.get("entities"))
    elif ct == "photo":
        bot.send_photo(user_id, msg["file_id"], caption=msg.get("caption"),
                       caption_entities=msg.get("caption_entities"))
    elif ct == "video":
        bot.send_video(user_id, msg["file_id"], caption=msg.get("caption"),
                       caption_entities=msg.get("caption_entities"))
    elif ct == "document":
        bot.send_document(user_id, msg["file_id"], caption=msg.get("caption"),
                          caption_entities=msg.get("caption_entities"))
    elif ct == "audio":
        bot.send_audio(user_id, msg["file_id"], caption=msg.get("caption"))
    elif ct == "voice":
        bot.send_voice(user_id, msg["file_id"])
    elif ct == "video_note":
        bot.send_video_note(user_id, msg["file_id"])
    elif ct == "sticker":
        bot.send_sticker(user_id, msg["file_id"])
    elif ct == "animation":
        bot.send_animation(user_id, msg["file_id"], caption=msg.get("caption"))
    elif ct == "album":
        media = []
        for i, item in enumerate(msg.get("items", [])):
            caption = item.get("caption") if i == 0 else None
            if item["content_type"] == "photo":
                media.append(types.InputMediaPhoto(
                    item["file_id"], caption=caption,
                    caption_entities=item.get("caption_entities") if i == 0 else None
                ))
            elif item["content_type"] == "video":
                media.append(types.InputMediaVideo(
                    item["file_id"], caption=caption,
                    caption_entities=item.get("caption_entities") if i == 0 else None
                ))
        if media:
            bot.send_media_group(user_id, media)


# ==========================
# Bo'lim funksiyalari
# ==========================
def school_about(message):
    text = """📚 MAKTAB HAQIDA

🏫 Maktabimiz 2022-yil 14-apreldagi PF-106-sonli farmoniga muvofiq tashkil etilgan.
📍 Dehqonobod tuman ixtisoslashtirilgan maktabi 2022-yil 5-sentabrdan faoliyat boshlagan.

🎯 Yo'nalishlarimiz:
🔹 Aniq fanlar (5–11 sinflar)
🔹 Tabiiy fanlar (7–11 sinflar)

👨‍🎓 Ta'lim jarayoni:
• 19 ta sinf, har birida 24 nafargacha o'quvchi tahsil oladi,
• Ixtisoslik fanlari 12 nafardan guruhlarga ajratib o'qitiladi,
• Matematika, fizika, ingliz, rus tili, informatika, kimyo, biologiya chuqurlashtirib o'qitiladi.

👨‍🏫 O'qituvchilar:
• 95 % oliy va birinchi toifali
• 3 bosqichli saralash imtihonidan o'tgan

🏅 Natijalar:
• Maktabdagi 60 % o'quvchilar sertifikatga ega
• 365+ milliy va xalqaro (SAT, IELTS)
• Xalqaro va asosiy fan olimpiadasi g'oliblari

⏰ 08:30–14:45 dars, 15:00–16:30 to'garaklar
💰 Ta'lim bepul

🏢 Zamonaviy maktab, kutubxona, sport zal, oshxona, kompyuter xonalari mavjud

🎓 35 nafar bitiruvchi (2025–2026) o'rtacha 158 ball bilan OTMlarda tahsil olmoqda

✨ Kelajak sari dadil qadam!"""
    photo = open('maktab_haqida.png', 'rb')
    bot.send_photo(message.chat.id, photo, caption=text)


def questions(message):
    user_id = message.chat.id
    user_states[user_id] = "waiting_for_question"
    msg = bot.send_message(
        message.chat.id,
        "❓ Savollarni yozib qoldiring\nAdmin tez orada javob beradi:\n\n(Bekor qilish uchun /bekor buyrug'ini yozing)"
    )
    bot.register_next_step_handler(msg, send_question_to_teacher)


def send_question_to_teacher(message):
    user_id = message.chat.id

    if message.text == "/bekor":
        user_states.pop(user_id, None)
        bot.send_message(user_id, "❌ Savol berish bekor qilindi.", reply_markup=tugmalar(message.from_user.id))
        return

    if message.text in ["🏫 Maktab haqida", "⁉️ E'tiroz va takliflar",
                       "👨‍🏫 O'qituvchilar", "📢 Kanal", "📞 Aloqa",
                       "🚪 Maktabga qabul qilish tartibi", "⬅️ Asosiy menyu", "⚙️ Admin panel"]:
        user_states.pop(user_id, None)
        return router(message)

    user_states.pop(user_id, None)

    student_id = message.chat.id
    username = f"@{message.from_user.username}" if message.from_user.username else f"ID: {student_id}"
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(
        text="✍️ Javob berish",
        callback_data=f"reply|{student_id}"
    ))
    sent = bot.send_message(
        SUPER_ADMIN_ID,
        f"📩 Yangi savol!\nFoydalanuvchi: {username}\n\n{message.text}",
        reply_markup=kb
    )
    # Boshqa adminlarga ham yuborish
    for admin_id in admins:
        if admin_id != SUPER_ADMIN_ID:
            try:
                bot.send_message(
                    admin_id,
                    f"📩 Yangi savol!\nFoydalanuvchi: {username}\n\n{message.text}",
                    reply_markup=kb
                )
            except Exception:
                pass
    pending_questions[sent.message_id] = student_id
    bot.send_message(student_id, "✅ Savolingiz adminga yuborildi", reply_markup=tugmalar(message.from_user.id))


@bot.callback_query_handler(func=lambda call: call.data.startswith("reply|"))
def admin_reply_callback(call):
    if not is_admin(call.from_user.id):
        bot.answer_callback_query(call.id, "❌ Siz admin emassiz!")
        return
    student_id = int(call.data.split("|")[1])
    msg = bot.send_message(call.from_user.id, "✍️ Javobingizni yozing:")
    bot.register_next_step_handler(msg, lambda m: send_answer_to_student(m, student_id))
    bot.answer_callback_query(call.id)


def send_answer_to_student(message, student_id):
    if is_admin(message.from_user.id):
        bot.send_message(student_id, f"👨‍🏫 Admin javobi:\n\n{message.text}")
        bot.send_message(message.from_user.id, "✅ Javob foydalanuvchiga yuborildi!")


def teachers(message):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for fan in teachers_data.keys():
        kb.add(fan)
    kb.add("⬅️ Asosiy menyu")
    bot.send_message(message.chat.id, "👨‍🏫 Fan tanlang:", reply_markup=kb)


def teachers_by_fan(message, fan):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for ustoz in teachers_data[fan].keys():
        kb.add(ustoz)
    kb.add("🔙 Orqaga")
    bot.send_message(message.chat.id, "👨‍🏫 Ustozni tanlang:", reply_markup=kb)


def teacher_info(message, fan, ustoz):
    data = teachers_data[fan][ustoz]
    fixed_path = fix_image(data["photo"])
    with open(fixed_path, "rb") as photo:
        bot.send_photo(
            message.chat.id,
            photo,
            caption=f"👨‍🏫 {ustoz}\n\n{data['info']}"
        )


def fix_image(path):
    img = Image.open(path)
    img.thumbnail((800, 800))
    img = img.convert("RGB")
    new_path = "fixed.jpg"
    img.save(new_path, "JPEG", quality=75, optimize=True)
    return new_path


def channel(message):
    photo = open('channel.jpg', 'rb')
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(
        text="📢 Bizning Telegram kanalimiz",
        url=f"https://t.me/{CHANNEL_USERNAME.lstrip('@')}"
    ))
    bot.send_photo(
        message.chat.id,
        photo,
        caption="Bizning Telegram kanalimiz:",
        reply_markup=kb
    )


def communication(message):
    photo = open('communication.jpg', 'rb')
    kb = types.InlineKeyboardMarkup(row_width=1)
    for i, teacher in enumerate(teachers_info_list):
        kb.add(types.InlineKeyboardButton(
            text=teacher["label"],
            callback_data=f"tc|{i}"
        ))
    bot.send_photo(
        message.chat.id,
        photo,
        caption="📞 Aloqa bo'limi\nUstozni tanlang:",
        reply_markup=kb
    )


@bot.callback_query_handler(func=lambda call: call.data.startswith("tc|"))
def teacher_contact(call):
    try:
        idx = int(call.data.split("|")[1])
        data = teachers_info_list[idx]
    except (IndexError, ValueError):
        bot.answer_callback_query(call.id, "Xatolik!")
        return

    photo_path = data.get("photo", "images/mengliqulovanurizar.jpg")
    fixed_path = fix_image(photo_path)

    caption = f"{data['label']}\n\n"
    if data.get("phone"):
        caption += f"📞 Telefon: {data['phone']}\n"
    if data.get("username"):
        caption += f"💬 Telegram: @{data['username']}\n"

    with open(fixed_path, "rb") as photo:
        bot.send_photo(call.message.chat.id, photo, caption=caption.strip())

    bot.answer_callback_query(call.id)


def acceptance(message):
    caption_1 = """#Qabul_2026 🎓

🏫 Dehqonobod tuman ixtisoslashtirilgan maktabiga 2026-2027 o'quv yili qabuli 15-maydan boshlanadi!

✅ 5-sinf ANIQ FAN yoʻnalishiga
4-sinfni tugatayotgan o'quvchilar qabul qilinadi.

🔰 7-sinf TABIIY FAN yoʻnalishiga
6-sinfni tugatayotgan o'quvchilar qabul qilinadi.

🌐 Qabul jarayoni ariza.piima.uz sayti orqali elektron shaklda 15-maydan 4-iyungacha davom etadi.

Kirish imtihoni Qarshi shahrida test sinovi shaklida oʻtkaziladi

💼 Hujjatlarni to'g'ri va ishonchli topshirish uchun maktabimizda qabul shtabi faoliyat yuritmoqda.

📍Manzil: Eski Agrosanoat kolleji

Murojaat uchun telefon:
☎️ 905226167
«Aniq fan» yo'nalishi bo'yicha:
📞+998996629860 (5-sinf)
«Tabiiy fan» yo'nalishi bo'yicha:
📞+998995660096 (7-sinf)
Telegram: 
@DehqonobodTIMbot
Maktabda o'qish, hujjat va imtihon topshirish BEPUL!

📲Bizni kuzatib boring
@Dehqonobod_Ixtisoslashtirilgan_M"""
    caption_2 = """#Qabul_2026 🎓

❓Dehqonobod tuman ixtisoslashtirilgan maktabiga kirish uchun qaysi fanlardan imtihon bo'ladi?

✅ Kirish imtihonlari yoʻnalishlar boʻyicha bir bosqichda quyidagi fanlardan test shaklida oʻtkaziladi:

🔹Aniq fanlar yoʻnalishi boʻyicha:
➖5-sinflar uchun (Ayni vaqtda maktabning 4-sinfini tugatayotgan o'quvchilari hujjat topshiradi)
➖Matematika (30 ta topshiriq), ingliz tili (15 ta topshiriq) fanlaridan (jami 45 ta topshiriq);

🔸Tabiiy fanlar yoʻnalishi boʻyicha:
➖7-sinflar uchun (Ayni vaqtda maktabning 6-sinfini tugatayotgan o'quvchilari hujjat topshiradi)
➖Tabiiy (sceince) fan (30 ta topshiriq) va ingliz tili (15 ta topshiriq) fanlaridan (jami 45 ta topshiriq);

Shuningdek savollar matiqiy fikrlash va mulohazaga qaratilgan bo'ladi.

Murojaat uchun telefon:
«Aniq fan» yo'nalishi bo'yicha:
📞+998996629860 (5-sinf)
«Tabiiy fan» yo'nalishi bo'yicha:
📞+998995660096 (7-sinf)
Maktabda o'qish, hujjat va imtihon topshirish BEPUL!

📲Bizni kuzatib boring
@Dehqonobod_Ixtisoslashtirilgan_M"""
    caption_3 = """#Qabul_2026 🎓

❓SAVOL:
Dehqonobod tuman ixtisoslashtirilgan maktabiga kirish imtihoni QACHON-QAYERDA bo'ladi? 
———————————
✅ JAVOB:
1️⃣ Kirish imtihonlari 25-iyun➖5-iyul oralig'ida 10 kun davomida o'tkazilishi rejalashtirilgan. (Ariza va hujjat topshirish 15-maydan 4-iyungacha amalga oshiriladi)

2️⃣ Imtihonlarning barchasi Qarshi shahrida markazlashgan holda amalga oshiriladi.

Kirish imtihonlari va materiallari Agentlik tomonidan mahalliy va xorijiy mutaxassislarni jalb etgan holda tegishli tashkilotlar bilan hamkorlikda oʻtkaziladi.
Belgilangan kvota doirasida kirish imtihonlari natijalariga koʻra eng yuqori ball toʻplagan oʻquvchilar oʻqishga qabul qilinadi.

📲 Telegram kanalimizni kuzatib boring, qabul bo'yicha rasmiy maʼlumotlar eʼlon qilib boriladi.
@Dehqonobod_Ixtisoslashtirilgan_M ➖Bilim va muvaffaqiyat maskani!"""
    caption_4 = """#Qabul_2026 🎓

❓Maktabimizga qaysi sinflarga qabul bo'ladi? 

✅ Qabul yangi ochiladigan 5-ANIQ sinf va 7-TABIIY sinflarga bo'ladi. 

Undan tashqari 6-7-8-9 sinflardagi bo'sh o'rinlarga qabul bo'ladi. 
———————————————
Aniqroq qilib aytaman: 

🔷 5-sinf «Aniq fanlar» yo'nalishiga 48 nafar o'quvchi qabul qilinadi. 

🔶 7-sinf «Tabiiy fanlar» yo'nalishiga 24 nafar o'quvchi qabul qilinadi.

🔹 9-sinf «Aniq fanlar» yo'nalishiga bo'sh o'rinlarga 3 nafar o'quvchi qabul qilinadi.

⁉️ 6-, 7-, 8-sinf «Aniq fanlar» yo'nalishlarda ayni vaqtda yetarlicha bo'sh o'quvchi o'rinlari mavjud bo'lmaganligi sababli hozircha qabul ochilishi aniq emas. 
✅ Lekin o'quv yili oxirigacha bo'sh o'rin ochilishiga qarab may oyida qo'shimcha qabul rasman eʼlon qilinadi! 
———————————————
10-11 sinflarga o'tgan o'quv yillarida qabul amalga oshirilmagan. 
Ammo shu yil qabul ochilishi ehtimoli bor. 

Telegram kanalimizni kuzatib boring, qabul bo'yicha rasmiy maʼlumotlar eʼlon qilib boriladi.
@Dehqonobod_Ixtisoslashtirilgan_M"""
    caption_file = """❓ Imtihon savollari qanday mavzularda tuziladi? 

Dehqonobod tuman ixtisoslashtirilgan maktabiga kiruvchilar uchun barcha fanlardan SPESTIFIKATSIYALAR 
(2025-yil) 

📶 Batafsil: https://portal.piima.uz/page/qabul-imtihon-materiallari-spesifikatsiyasi

⚠️ Maktabimizga 2026-2027 o'quv yili qabuli 15-maydan 4-iyungacha davom etadi

Murojaat uchun telefon:
☎️ 905226167
«Aniq fan» yo'nalishi bo'yicha:
📞+998996629860 (5-sinf)
«Tabiiy fan» yo'nalishi bo'yicha:
📞+998995660096 (7-sinf)
Telegram: 
@DehqonobodTIMbot
Maktabda o'qish, hujjat va imtihon topshirish BEPUL!

📲Bizni kuzatib boring
@Dehqonobod_Ixtisoslashtirilgan_M
➖Bilim va muvaffaqiyat maskani!"""
    caption_album = """#Qabul_2026 🎓

Qabul uchun kerakli HUJJATLAR:
1️⃣ Ota-onasining pasporti
2️⃣ Telefon raqami
3️⃣ O'quvchining guvohnomasi
4️⃣ O'quvchining 3x4 rasmi (elektron)

🌐 Hujjatlar ariza.piima.uz sayti orqali elektron shaklda 15-maydan 4-iyungacha qabul qilinadi.

📲Bizni kuzatib boring
@Dehqonobod_Ixtisoslashtirilgan_M
➖Bilim va muvaffaqiyat maskani!"""

    photo1 = open('image1.jpg', 'rb')
    bot.send_photo(message.chat.id, photo1, caption=caption_1)

    photo2 = open('image2.jpg', 'rb')
    bot.send_photo(message.chat.id, photo2, caption=caption_2)

    photo3 = open('image3.jpg', 'rb')
    bot.send_photo(message.chat.id, photo3, caption=caption_3)

    photo4 = open('image4.jpg', 'rb')
    bot.send_photo(message.chat.id, photo4, caption=caption_4)

    file = open('Imtihon SPESTIFIKATSIYASI 2026.zip', 'rb')
    bot.send_document(message.chat.id, file, caption=caption_file)

    media_group = [
        types.InputMediaPhoto(open('album1.jpg', 'rb')),
        types.InputMediaPhoto(open('album2.jpg', 'rb')),
        types.InputMediaPhoto(open('album5.jpg', 'rb'))
    ]
    media_group[0].caption = caption_album
    media_group[0].parse_mode = 'HTML'

    bot.send_media_group(message.chat.id, media_group)


# ==========================
# Admin buyrug'i
# ==========================
@bot.message_handler(commands=['admin'])
def admin_command(message):
    if is_admin(message.from_user.id):
        bot.send_message(message.chat.id, "🔐 Admin panel:", reply_markup=admin_panel_kb(message.from_user.id))
    else:
        bot.send_message(message.chat.id, "❌ Sizda ruxsat yo'q!")


# ==========================
# Ishga tushirish
# ==========================
print("✅ BOT STARTED")
print(f"📦 Saqlangan foydalanuvchilar: {len(all_users)} ta")
print(f"👮 Adminlar soni: {len(admins)} ta")
bot.infinity_polling(timeout=60, long_polling_timeout=60)
