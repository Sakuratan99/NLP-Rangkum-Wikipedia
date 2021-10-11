from nltk.tokenize import sent_tokenize as st , word_tokenize as wt
from nltk.corpus import stopwords
import bs4 as bs 
import re 
import urllib.request
import heapq




url = str(input("masukan url wikipedia:"))
jumlah_kalimat = int(input("jumlah kalimat yang ingin ditampilkan:"))


data_artikel = urllib.request.urlopen(url)
artikel = data_artikel.read()

parsed_artikel = bs.BeautifulSoup(artikel,"lxml")
#lxml -> parsing

paragraf = parsed_artikel.find_all('p')
#mengambil tag p (paragraph)

teks_artikel = ""

for p in paragraf:
    teks_artikel += p.text

#menghilangkan tanda  refrensi dan space tambahan
teks_artikel = re.sub(r'\[[0-9]*\]',' ',teks_artikel)
teks_artikel = re.sub(r'\s+',' ',teks_artikel)

#menghilangkan angka dan special karakter
format_teks_artikel = re.sub(r'[^a-zA-Z]',' ',teks_artikel)
format_teks_artikel = re.sub(r'\s+',' ',format_teks_artikel)

#menkonversi teks ke kalimat
list_kalimat = st(teks_artikel)

stopwords_indo = set(stopwords.words('Indonesian'))

frekuensi_kata = {}

for word in wt(format_teks_artikel):
    if word not in stopwords_indo:
        if word not in frekuensi_kata.keys():
            frekuensi_kata[word] = 1
        else:
            frekuensi_kata[word] += 1

max_frekuensi =  max(frekuensi_kata.values())

for word in frekuensi_kata.keys():
    frekuensi_kata[word] : (frekuensi_kata[word]/max_frekuensi)

nilai_kalimat = {}
for sent in list_kalimat :
    for word in wt(sent.lower()):
        if word in frekuensi_kata.keys():
            if len(sent.split(' ')) < 27:
                if sent not in nilai_kalimat.keys():
                    nilai_kalimat[sent] = frekuensi_kata[word]
                else:
                    nilai_kalimat[sent] += frekuensi_kata[word]


ringkasan_kalimat = heapq.nlargest(jumlah_kalimat,nilai_kalimat,key=nilai_kalimat.get)

ringkasan = ' '.join(ringkasan_kalimat)
print("\n")
print(ringkasan)
