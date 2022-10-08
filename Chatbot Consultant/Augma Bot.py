import re
import random as rand
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, precision_score
from tkinter import *
from tkinter import ttk

df = pd.read_csv("Survey Minat dan Bakat ver 2.1.csv")

# Pembagian independent variabel dan dependent variabel
x = df.iloc[:,0]
y = df.iloc[:,1]

j = 0

# membuang tanda baca
for i in x:
    x[j] = re.sub(pattern = "[^\w\s]", repl = "", string = x[j])
    x[j] = x[j].lower()
    j += 1

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size= 0.2, random_state = 0)

# Data independent variable akan dilihat kemungkinan pentingnya
vectorizer = CountVectorizer()
x_traincv = vectorizer.fit_transform(x_train)
x_testcv = vectorizer.transform(x_test)

#membuat modelnya
model = MultinomialNB()
model.fit(x_traincv, y_train)
model.fit(x_testcv, y_test)

test_set = model.predict(x_testcv)
test_set1 = model.predict(x_traincv)

# Pengecekan Akurasi
acc = accuracy_score(test_set, y_test)
acc1 = accuracy_score(test_set1, y_train)
prec = precision_score(test_set, y_test, average = None)
prec1 = precision_score(test_set1, y_train, average = None)

# Perkenalan diri
# Deklarasi pengecek serta corpus input, respon dan reject
greet_check = False
exit_check = False
exit_inputs = ("keluar", "klr", "exit", "out", "malas", "males", "stop", "berhenti", "leave")
exit_response = ["Terima kasih telah menggunakan Augma Bot~"]
greet_inputs = ("hello", "helo", "hai", "hi", "hey", "hy","halo", "hallo" ,"hoi", "oi", "bangun")
greet_response = ["Halo nama saya Augma Bot!", 
                  "Perkenalkan, nama saya Augma Bot.", 
                  "Selamat datang di sesi konsultasi ini. Nama saya Augma Bot.", 
                  "Halo bang, kek mananya kau? G kenal aku ini siapa? Salken salken Augma Bot ini bos"]
greet_reject = ["System    : Sepertinya anda salah mengetikkan panggilannya.", 
                "System    : Augma Bot gagal dipanggil, silakan masukan panggilan yang sesuai.",
                "System    : Panggilan tidak berhasil. Petunjuk untuk panggilan telah disematkan pada pembicaraan diatas.", 
                "System    : Untuk melanjutkan pembicaraannya, harap untuk memanggil Augma Bot dengan kode yang telah ditentukan."]

# fungsi perkenalan diri dan keluar
def greet(sentence):
    global greet_check
    global exit_check
    greet_check = False
    exit_check = False
    for word in sentence.split():
        if word.lower() in exit_inputs:
            exit_check = True
            return rand.choice(exit_response)
        elif word.lower() in greet_inputs:
            greet_check = True
            return rand.choice(greet_response)
    return rand.choice(greet_reject)

# Sebelum melakukan konsultasi
# Deklarasi pengecek serta corpus positive, negative, response dan reject
have_consult = False
consult_positive = ("mengerti", "ngerti", "paham", "sudah pernah", "pernah", "ya", "y", "iya", "tw", "tau", "tahu")
consult_negative = ("tidak", "ga", "nggak", "ngga", "enggak", "engga", "g", "blm", "blm pernah", "belum", "belum pernah","tdk", "blm", "no", "n", "nope", "nah", "noh")
consult_response = ["Baik. Langsung saja kita mulai pembahasan inti dari konsultasi ini.",
                    "Baiklah kalau begitu. Mari kita langsung mulai konsultasinya.",
                    "Kalau begitu, penjelasan mengenai cara mengikuti konsultasi ini akan kita lewati. Kita akan memulai konsultasinya.",
                    "Paten g usah susah susah Augma Bot bercakap"]
consult_reject = ["Baiklah, Augma Bot akan menjelaskan terlebih dahulu tata cara yang perlu dilakukan. Anda cukup menjawab pertanyaan yang akan saya tanyakan seperti mata pelajaran apa yang kamu sukai dan kuasai. Cukup simple bukan?",
                  "Jangan khawatir. Tata cara untuk mendapatkan hasil yang sesuai cukup mudah. Anda hanya perlu memberitahukan saya mata pelajaran yang anda minati dan kuasai.",
                  "Jangan pusing-pusing. Gampang aja kok, ikuti dan jawab aja pertanyaanku nanti :v Gampangnya itu..."]

# Fungsi Sebelum melakukan konsultasi
def start(sentence):
    global have_consult
    have_consult = False
    for word in sentence.split():
        if word.lower() in consult_negative:
            have_consult = True
            return "Augma Bot : " + rand.choice(consult_reject)
        elif word.lower() in consult_positive:
            have_consult = True
            return "Augma Bot : " + rand.choice(consult_response)
        else:
            return "Augma Bot : Saya kurang mengerti ucapan anda"

# Menanyakan pengguna apakah sudah siap dengan konsultasi atau tidak
# Deklarasi pengecek serta corpus positive, negativem response dan reject
ready_bool = False
wrong = False
ready_positive = ("iya", "iyes", "iy", "yes", "y", "ya", "sudah", "sdh", "siap", "sip", "ready", "ok", "oke", "okay", "kay", "siap")
ready_negative = ("tidak", "tdk", "no", "n", "belum", "blm", "ga", "nggak", "ngga", "enggak", "engga", "g")
ready_response = ["Baik Augma Bot akan memberikan pertanyaan yang pertama.",
                 "Baiklah anda akan memasukki pertanyaan yang pertama.",
                 "Yok kita lanjut wak ^_^"]
ready_reject = ["Tidak apa-apa. Augma Bot akan menunggu sampai anda siap.",
                "Baiklah Augma Bot akan kembali beristirahat selagi menunggu anda.",
                "Kalau begitu Augma Bot akan tidur kembali untuk mengisi ulang energi agar energi! uwu",
                "Ntah apanya kau... ahh tidur dulu aku ko ganggu aku kucampakkan kau dari sini!!"]

# Fungsi readynya
def ready(sentence):
    global ready_bool
    global wrong
    wrong = False
    ready_bool = False
    for word in sentence.split():
        if word.lower() in ready_negative:
            return "Augma Bot : " + rand.choice(ready_reject)
        elif word.lower() in ready_positive:
            ready_bool = True
            return "Augma Bot : " + rand.choice(ready_response)
        else:
            wrong = True
            return "Augma Bot : Augma Bot kurang mengerti ucapan anda..."

# kuasai ataupun suka, akan menggunakan corpus dan fungsi yang sama
mapel_check = False
count = int(0)
mapel_correct = ("inggris", "jepang", "mandarin", "indonesia", "matematika", "biologi", "fisika",
                 "kimia", "sosiologi", "ekonomi", "sejarah", "akuntansi", "geografi", "kewarganegaraan",
                 "seni", "lukis", "tari", "agama", "islam", "kristen", "buddha", "hindu", "komputer")
mapel_correct_response = ["Jawaban anda akan Augma Bot tampung. Mari kita lanjutkan!",
                          "Augma Bot mengerti. Mari pergi ke bagian selanjutnya :D",
                          "Sip mantab wakgeng kita gas ke part selanjutnya :v"]
mapel_reject_response = ["Apakah anda salah menuliskan mata pelajarannya? Silakan kembali menuliskan jawaban anda dari pilihan ini, yaitu",
                         "Berikut adalah daftar dari mata pelajaran yang Augma Bot simpan. Mohon bantuannya untuk menuliskan mata pelajaran yang terdaftar, yaitu",
                         "Gak semua bisa ko tulis bang awak bot ini bukan manusia ksh la dispensasi. Noh ini yang ko bisa tulis"]

# Fungsi validasi mapel yang ada
def mapel_validation(sentence, banyak):
    global mapel_check
    global count
    count = int(0)
    banyak = int(banyak)
    mapel_check = False
    for word in sentence.split():
        word = re.sub(pattern = "[^\w\s]", repl = "", string = word)
        if word.lower() in mapel_correct:
            count += 1
    if (count >= banyak):
        mapel_check = True
        return "Augma Bot : " + rand.choice(mapel_correct_response)
    else:
        return "Augma Bot : " + rand.choice(mapel_reject_response) + " inggris, jepang, mandarin, indonesia, biologi, fisika, kimia, sosiologi, ekonomi, sejarah, akuntansi, geografi, kewarganegaraan, seni, lukis, tari, agama, islam, kristen, buddha, hindu dan komputer"

from tkinter import *

mapel = ""
byk = 0
    
def kuasaimapel():
    global byk
    ans = answer.get()
    textarea.insert(END, 'You : ' + ans + "\n\n")
    textarea.insert(END, mapel_validation(ans,int(byk)) + "\n\n")
    answer.delete(0, END)
    global button
    if (mapel_check == False):
        textarea.insert(END, "Augma Bot : Ada berapa mata pelajaran yang anda minati?\n\n")
        button = button.pack_forget()
        button = Button(root, text = "Send", command = kuasaibanyak)
        button.pack()
    elif(mapel_check):
        global mapel
        mapel += ans
        mapel = mapel.lower()
        mapel = re.sub(pattern = "[^\w\s]", repl = "", string = mapel)
        mapel = pd.Series(mapel)
        mapel_cv = vectorizer.transform(mapel)
        hasil = model.predict(mapel_cv)
        textarea.insert(END, "Augma Bot : Jurusan yang cocok dengan anda adalah " + hasil[0] + '\n\n')
        if (hasil[0] == "MIPA"):
            textarea.insert(END, "Augma Bot : MIPA merupakan salah satu kategori jurusan yang cukup susah karena membutuhkan logika yang tinggi untuk mengerti mata kuliah yang ada. Matematika merupakan dasar dari semua jenis jurusan. Segala jenis jurusan yang berhubungan dengan MIPA akan menggunakan matematika. Perkuat matematika anda agar dapat menalukkan setiap mata kuliah yang ada. Perkuat fisika anda bila anda memilih mata kuliah teknik-teknik kecuali teknik yang lebih membutuhkan kimia. Biologi merupakan mata pelajaran yang sangat penting bila anda ingin menjadi dokter ataupun jurusan lainnya mengenai makhluk hidup. Kimia merupakan cabang dari fisika namun befokus pada reaksi antar atom-atom yang ada sehingga untuk jurusan seperti apoteker akan membutuhkan nilai kimia yang tinggi\n\n")
        elif (hasil[0] == "IPS"):
            textarea.insert(END, "Augma Bot : IPS merupakan salah satu kategori jurusan yang cukup luas, unik dan topiknya dapat bercabang-cabang dan fleksibel sehingga dibutuhkannya dasar yang kuat dengan mata pelajaran yang ada. Walaupun tidak membutuhkannya matematika, ada beberapa jurusan yang menggunakan matematika untuk menghitung suatu nilai. Geografi merupakan mata pelajaran yang berfokus pada tata letak dari suatu daratan maupun lautan sehingga mata kuliah ini tidak jauh-jauh dari matematika. Geografi sendiri memiliki banyak jurusan seperti panteologis. Sosiologi merupakan mata pelajaran yang berfokus pada manusia sebagai suatu makhluk sosial baik fenomena maupun gerak-gerik seseorang sehingga sangat cocok untuk memasukki jurusan seperti Psikologi. Ekonomi merupakan mata pelajaran yang berfokus pada uang keluar dan uang masuk serta hukum-hukum yang perlu diingat untuk mengerti apa yang terjadi dengan pengaliran uang yang ada sehingga jurusan yang cocok untuk mata pelajaran ini seperti jurusan ekonomi. Sejarah merupakan mata pelajaran yang berfokus menganalisa masa lalu dan melakukan suatu perubahan untuk membuat umat manusia semakin membaik sehingga jurusan yang cocok bila mata pelajaran ini seperti jurusan yang berhubungan dengan fosil maupun adat. Akuntansi merupakan mata pelajaran yang berfokus pada perhitungan masuk keluarnya uang dari suatu perusahaan dan kebetulan dari transaksi yang ada dan jurusan ini juga dapat diteruskan pada saat anda memasukki universitas\n\n")
        elif (hasil[0] == "Seni"):
            textarea.insert(END, "Augma Bot : Pertahankan hobi kamu dan buatlah hobi tersebut menjadi sesuatu hasil yang menawan dan indah dilihat. Seni Lukis merupakan mata pelajaran yang membuat suatu kertas kosong menjadi kertas yang berwarna dan berbentuk. Seni tari merupakan mata pelajaran yang membuat suatu gerakan yang lemah gemulai, kuat, ataupun standar. Hal ini dilakukan sesuai dengan dentuman musik yang ada dimana mata pelajaran ini ada hubungannya dengan mata pelajaran berikutnya yaitu Seni musik. Seni musik merupakan mata pelajaran yang berfokus dalam membuat irama ataupun dentuman yang enak didengar. Seni-seni yang akan dipelajari dibutuhkan kesabaran yang tinggi dan tidak akan bisa direplikasi bila tidak adanya konsistensi maupun dedikasi yang tinggi sehingga anda harus meningkatkan konsistensi latihan yang ada\n\n")
        elif(hasil[0] == "Literatur"):
            textarea.insert(END, "Augma Bot : Pelajarilah bahasa yang kalian inginkan baik indonesia, inggris, jepang, jerman, ataupun bahasa lainnya yang kalian sukai. Perpanjangan dari mata pelajaran literatur ini adalah filsafat. Perkuatlah dedikasi anda pada suatu bahasa sehingga anda dapat menguasai bahasa tersebut hingga ke akar-akarnya\n\n")
        elif(hasil[0] == "Agama"):
            textarea.insert(END, "Augma Bot : Baik agama apapun, anda harus meningkatkan iman dan rohani anda untuk mengerti mengenai agama apa yang ingin dipelajari. Hal ini bukanlah suatu tugas yang susah didengar namun tugas tersebut membutuhkan kesabaran yang tinggi untuk mengerti apa sebenarnya yang dipelajari dan bagaimana praktek dari literatur yang sudah dipelajarai\n\n")
        else:
            textarea.insert(END, "Augma Bot : Komputer merupakan salah satu temuan baru dan merupakan salah satu mata kuliah yang tersulit karena dapat diadaptasi kedalam komputer. Untuk permulaan, anda dapat mempelajari excel untuk memperkuat logika anda. Selain itu, jurusan komputer tidak akan jatuh jauh dari matematika sehingga bila anda ingin lari dari matematika karena komputer maka pemikiran tersebut sangatlah salah\n\n")
        textarea.insert(END, "Augma Bot : Terima kasih telah mengikuti sesi konsultasi ini sampai selesai! Augma Bot akan kembali tidur untuk beristirahat :D\n\n")
        textarea.insert(END, "System : Selamat datang di ruangan chat konsultasi jurusan perkuliahan. Sesi konsultasi anda akan ditemani oleh Augma Bot. Ketikkan 'Halo Augma Bot!!!' agar Augma Bot dapat bangun dari tidurnya. Bila ingin keluar atau tidak ingin melanjutkan konsultasi jurusan, anda bisa berhenti dari program ini.\n\n")
        button = button.pack_forget()
        button = Button(root, text = "Send", command = reply)
        button.pack()
        mapel = ""
        byk = 0
    
def kuasaibanyak():
    ans = answer.get()
    textarea.insert(END, 'You : ' + ans + "\n\n")
    answer.delete(0, END)
    global button
    global byk
    try:
        int(ans)
    except:
        textarea.insert(END, 'Augma Bot : Anda salah memasukkan jumlah mata pelajaran...\n\n')
        textarea.insert(END, "Augma Bot : Ada berapa mata pelajaran yang anda kuasai?\n\n")
    else:
        byk = ans
        textarea.insert(END, "Augma Bot : Semasa menjalani sekolah menengah atas, pelajaran apa yang anda kuasai?\n\n")
        button = button.pack_forget()
        button = Button(root, text = "Send", command = kuasaimapel)
        button.pack()

def sukaimapel():
    global byk
    ans = answer.get()
    textarea.insert(END, 'You : ' + ans + "\n\n")
    textarea.insert(END, mapel_validation(ans,int(byk)) + "\n\n")
    answer.delete(0, END)
    global button
    if (mapel_check == False):
        textarea.insert(END, "Augma Bot : Ada berapa mata pelajaran yang anda minati?\n\n")
        button = button.pack_forget()
        button = Button(root, text = "Send", command = sukaibanyak)
        button.pack()
    elif(mapel_check):
        global mapel
        mapel += ans + " "
        textarea.insert(END, "Augma Bot : Ada berapa mata pelajaran yang anda kuasai?\n\n")
        button = button.pack_forget()
        button = Button(root, text = "Send", command = kuasaibanyak)
        button.pack()

def sukaibanyak():
    ans = answer.get()
    textarea.insert(END, 'You       : ' + ans + "\n\n")
    answer.delete(0, END)
    global button
    global byk
    try:
        int(ans)
    except:
        textarea.insert(END, 'Augma Bot : Anda salah memasukkan jumlah mata pelajaran.\n\n')
        textarea.insert(END, "Augma Bot : Ada berapa mata pelajaran yang kamu minati?\n\n")
    else:
        byk = ans
        textarea.insert(END, "Augma Bot : Semasa sekolah menengah atas, mata pelajaran apa yang anda minati?\n\n")
        button = button.pack_forget()
        button = Button(root, text = "Send", command = sukaimapel)
        button.pack()
    
def consultation():
    ans = answer.get()
    textarea.insert(END, 'You : ' + ans + "\n\n")
    textarea.insert(END, ready(ans) + "\n\n")
    answer.delete(0, END)
    global button
    global ready_bool
    if(ready_bool):
        textarea.insert(END, "Augma Bot : Ada berapa mata pelajaran yang kamu minati?\n\n")
        button = button.pack_forget()
        button = Button(root, text = "Send", command = sukaibanyak)
        button.pack()
    elif(wrong == True):
        textarea.insert(END, "Augma Bot : Apakah anda siap untuk mengikuti konsultasi ini?\n\n")
    elif(ready_bool == False):
        textarea.insert(END, "System : Selamat datang di ruangan chat konsultasi jurusan perkuliahan. Sesi konsultasi anda akan ditemani oleh Augma Bot. Ketikkan 'Halo Augma Bot!!!' agar Augma Bot dapat bangun dari tidurnya. Bila ingin keluar atau tidak ingin melanjutkan konsultasi jurusan, anda bisa berhenti dari program ini.\n\n")
        button = button.pack_forget()
        button = Button(root, text = "Send", command = reply)
        button.pack()
    else:
        textarea.insert(END, "Augma Bot : Apakah anda siap dalam konsultasi ini?\n\n")
    
def have():
    ans = answer.get()
    textarea.insert(END, 'You : ' + ans + "\n\n")
    textarea.insert(END, start(ans) + '\n\n')
    answer.delete(0, END)
    global button
    global have_consult
    if (have_consult):
        textarea.insert(END, "Augma Bot : Apakah anda siap mengikuti konsultasi ini?\n\n")
        button = button.pack_forget()
        button = Button(root, text = "Send", command = consultation)
        button.pack()
    else:
        textarea.insert(END, 'Augma Bot : Apakah anda pernah mengikuti atau tahu mengenai konsultasi perkuliahan ini?\n\n')

def reply():
    ans = answer.get()
    textarea.insert(END, 'You : ' + ans + '\n\n')
    textarea.insert(END, 'Augma Bot : ' + greet(ans) + '\n\n')
    answer.delete(0, END)
    global button
    global greet_check
    if (greet_check == True):
        textarea.insert(END, 'Augma Bot : Apakah anda pernah mengikuti atau tahu mengenai konsultasi perkuliahan ini?\n\n')
        button = button.pack_forget()
        button = Button(root, text = "Send", command = have)
        button.pack()
    else:
        textarea.insert(END, "System : Selamat datang di ruangan chat konsultasi jurusan perkuliahan. Sesi konsultasi anda akan ditemani oleh Augma Bot. Ketikkan 'Halo Augma Bot!!!' agar Augma Bot dapat bangun dari tidurnya. Bila ingin keluar atau tidak ingin melanjutkan konsultasi jurusan, anda bisa berhenti dari program ini.\n\n")

root = Tk()

root.geometry('500x570+100+100')
root.title('Augma Bot')
root.config(bg = '#000000')

chatframe = Frame(root)
chatframe.pack()

scrollbar = Scrollbar(chatframe)
scrollbar.pack(side = RIGHT)

textarea = Text(chatframe, font = ('consolas', '16', 'bold'), height = 18, yscrollcommand = scrollbar.set, wrap = 'word', bg = '#FFEC4E')
textarea.pack()
scrollbar.config(command = textarea.yview())

answer = Entry(root, font = ('consolas', '20'))
answer.pack(pady = 15, fill = X)
textarea.insert(END, "System : Selamat datang di ruangan chat konsultasi jurusan perkuliahan. Sesi konsultasi anda akan ditemani oleh Augma Bot. Ketikkan 'Halo Augma Bot!!!' agar Augma Bot dapat bangun dari tidurnya. Bila ingin keluar atau tidak ingin melanjutkan konsultasi jurusan, anda bisa berhenti dari program ini.\n\n")
button = Button(root, text = "Send", command = reply)
button.pack()

root.mainloop()
