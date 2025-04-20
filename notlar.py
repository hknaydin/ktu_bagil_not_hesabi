#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import division, print_function
import math

def round1(x):
    return int(x + 0.5)

def round2(x):
    if x > 0:
        return int((x + 0.005) * 100) / 100.0
    else:
        return int((x - 0.005) * 100) / 100.0

def parse_score(s):
    s = s.strip().upper()
    if s.isdigit():
        return int(s)
    if s in ('G', 'E', 'D'):
        return -2
    return 0

# ------- Kullanıcıya göre ayarlayın -------
input_filename  = "notlar.txt"
output_filename = "sonuclar.txt"
# -------------------------------------------

# Tablo‑1’e göre sınıf düzeyi eşik tablosu:
grade_thresholds = {
    "USTUN BASARI": [(57, "AA"), (52, "BA"), (47, "BB"), (42, "CB"),
                     (37, "CC"), (32, "DC"), (27, "DD"), (22, "FD"),
                     (0,  "FF")],
    "MUKEMMEL":    [(59, "AA"), (54, "BA"), (49, "BB"), (44, "CB"),
                     (39, "CC"), (34, "DC"), (29, "DD"), (24, "FD"),
                     (0,  "FF")],
    "COK IYI":     [(61, "AA"), (56, "BA"), (51, "BB"), (46, "CB"),
                     (41, "CC"), (36, "DC"), (31, "DD"), (26, "FD"),
                     (0,  "FF")],
    "IYI":         [(63, "AA"), (58, "BA"), (53, "BB"), (48, "CB"),
                     (43, "CC"), (38, "DC"), (33, "DD"), (28, "FD"),
                     (0,  "FF")],
    "ORTANIN USTU":[(65, "AA"), (60, "BA"), (55, "BB"), (50, "CB"),
                     (45, "CC"), (40, "DC"), (35, "DD"), (30, "FD"),
                     (0,  "FF")],
    "ORTA":        [(67, "AA"), (62, "BA"), (57, "BB"), (52, "CB"),
                     (47, "CC"), (42, "DC"), (37, "DD"), (32, "FD"),
                     (0,  "FF")],
    "ZAYIF":       [(69, "AA"), (64, "BA"), (59, "BB"), (54, "CB"),
                     (49, "CC"), (44, "DC"), (39, "DD"), (34, "FD"),
                     (0,  "FF")],
    "KOTU":        [(71, "AA"), (66, "BA"), (61, "BB"), (56, "CB"),
                     (51, "CC"), (46, "DC"), (41, "DD"), (36, "FD"),
                     (0,  "FF")],
}

# 1) Girdi dosyasını oku
with open(input_filename, "r") as f:
    lines = [l.strip() for l in f.readlines()]

students = int(lines[0])  # toplam öğrenci sayısı
raw_data = [line.split() for line in lines[1:] if line]

# 2) Veriyi parse et
data = []
for parts in raw_data:
    if len(parts) != 3:
        continue
    okul_no = int(parts[0])
    vize    = parse_score(parts[1])
    final   = parse_score(parts[2])
    data.append((okul_no, vize, final))

# 3) Ortalama ve istatistikler
ortalamalar = []
bagilaKatma = under15 = finD = 0

for okul_no, vize, final in data:
    if vize < -1:
        vize = 0
    if final < -1:
        final = 0
        finD += 1
    ort = (vize + final) / 2.0
    if final == 0 or ort <= 15:
        ortalamalar.append(0)
        bagilaKatma += 1
        if final != 0 and ort <= 15:
            under15 += 1
    else:
        ortalamalar.append(ort)

aktif_ogrenci = students - bagilaKatma
ortalama      = round2(sum(ortalamalar) / aktif_ogrenci)
stdsapma      = round2(math.sqrt(
    sum((o - ortalama) ** 2 for o in ortalamalar if o > 15)
    / aktif_ogrenci
))

# 4) Sınıf düzeyi
if ortalama > 80:
    sinif_duzeyi = "USTUN BASARI"
elif ortalama > 70:
    sinif_duzeyi = "MUKEMMEL"
elif ortalama > 62.5:
    sinif_duzeyi = "COK IYI"
elif ortalama > 57.5:
    sinif_duzeyi = "IYI"
elif ortalama > 52.5:
    sinif_duzeyi = "ORTANIN USTU"
elif ortalama > 47.5:
    sinif_duzeyi = "ORTA"
elif ortalama > 42.5:
    sinif_duzeyi = "ZAYIF"
else:
    sinif_duzeyi = "KOTU"

# 5) Z-notu, T-notu ve harfli notlar
z_notlari     = []
t_notlari     = []
harfli_notlar = []

for ort, (okul_no, vize, final) in zip(ortalamalar, data):
    if ort == 0 or final < 45:
        z = t = 0
    else:
        z = (ort - ortalama) / stdsapma
        t = round1(10 * z + 50)
    z_notlari.append(z)
    t_notlari.append(t)
    for thr, grd in grade_thresholds[sinif_duzeyi]:
        if t >= thr:
            harfli_notlar.append(grd)
            break

# 6) Sonuçları dosyaya yaz
with open(output_filename, "w") as out:
    out.write("FINALE GIRMEYENLER + DEVAMSIZLAR\t = %d\n" % finD)
    out.write("ORTALAMASI 15 VEYA ALTINDA OLANLAR\t = %d\n" % under15)
    out.write("BAGIL DEGERLENDIRMEYE KATILMAYANLAR\t = %d\n" % bagilaKatma)
    out.write("SINIF ORTALAMASI\t\t\t = %.6f\n" % ortalama)
    out.write("STANDART SAPMA\t\t\t\t = %.6f\n" % stdsapma)
    out.write("SINIF DUZEYI\t\t\t\t = %s\n\n" % sinif_duzeyi)
    out.write("NUMARA\t VIZE\t FINAL\t ORT.\t Z NOTU\t T NOTU\t HARFLI NOT\n")
    for (okul_no, vize, final), ort, z, t, hn in zip(data, ortalamalar, z_notlari, t_notlari, harfli_notlar):
        out.write("%d\t %d\t %d\t %.2f\t %.2f\t %d\t %s\n" % (
            okul_no, vize, final,
            round2(ort), round2(z),
            t, hn
        ))
    # 7) NOT ISTATISTIKLERI
    counts = {g: harfli_notlar.count(g) for g in ("AA","BA","BB","CB","CC","DC","DD","FD","FF")}
    out.write("\n NOT ISTATISTIKLERI :\n")
    out.write("    AA = %d\n" % counts["AA"])
    out.write("    BA = %d\n" % counts["BA"])
    out.write("    BB = %d\n" % counts["BB"])
    out.write("    CB = %d\n" % counts["CB"])
    out.write("    CC = %d\n" % counts["CC"])
    out.write("    DC = %d\n" % counts["DC"])
    out.write("    DD = %d\n" % counts["DD"])
    out.write("    FD = %d\n" % counts["FD"])
    out.write("    FF = %d\n" % counts["FF"])

print("Çıktı oluşturuldu:", output_filename)

