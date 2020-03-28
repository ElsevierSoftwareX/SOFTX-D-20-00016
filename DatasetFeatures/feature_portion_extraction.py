# Questo script estrae un sottoinsieme delle feature del dataset Match_2019_02_13_#002
# Analisi effettuata osservando i frame a partire da 4592 fino a 10592 (60 secondi), ovvero da 00:50s a 01:50s del video

count = 0
with open("features_Match_2019_02_13_#002.log", 'r') as f:
    f_o = open("features_Match_2019_02_13_#002_extracted.log", "w")

    for line in f:
        if line.startswith("4592") or count > 1:
            count += 1
            f_o.write(line)
        
        if (count > 6000 * 23):
            break

    f.close()
    f_o.close()