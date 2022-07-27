from cigar import Cigar

f = open("result.sam", "r")
new_file = open("final.txt", "w")
count = 0
for line in f:
    dup_line = f.readline()
    features = line[0:len(line)-1].split("\t")
    dup_features = dup_line[0:len(dup_line)-1].split("\t")
    if int(features[4]) > int(dup_features[4]):
        features.append("Greater Mapping Quality\n")
        dem = "\t"
        dem = dem.join(features)
        new_file.write(dem)
    elif int(features[4]) < int(dup_features[4]):
        dup_features.append("Greater Mapping Quality\n")
        dem = "\t"
        dem = dem.join(dup_features)
        new_file.write(dem)
    else:
        cigar = Cigar(features[5])
        dup_cigar = Cigar(dup_features[5])
        list1 = list(cigar.items())
        list2 = list(dup_cigar.items())
        num_match = 0
        dup_num_match = 0
        for i in list1:
            if i[1] == 'M':
                num_match += i[0]
        for i in list2:
            if i[1] == 'M':
                dup_num_match += i[0]
        if (num_match > dup_num_match and num_match >= 61):
            features.append("Better CIGAR\n")
            dem = "\t"
            dem = dem.join(features)
            new_file.write(dem)
        elif (num_match < dup_num_match and dup_num_match >= 61):
            dup_features.append("Better CIGAR\n")
            dem = "\t"
            dem = dem.join(dup_features)
            new_file.write(dem)
        else:
            id = str(line[0])
            dup_id = str(dup_line[0])
            if id < dup_id:
                features.append("Lower ID\n")
                dem = "\t"
                dem = dem.join(features)
                new_file.write(dem)
            elif id > dup_id:
                dup_features.append("Lower ID\n")
                dem = "\t"
                dem = dem.join(dup_features)
                new_file.write(dem)
            else:
                temp1 = features[0][2:len(features[0])]
                temp2 = dup_features[0][2:len(dup_features[0])]
                if temp1 < temp2:
                    features.append("Lower ID\n")
                    dem = "\t"
                    dem = dem.join(features)
                    new_file.write(dem)
                elif temp1 > temp2:
                    dup_features.append("Lower ID\n")
                    dem = "\t"
                    dem = dem.join(dup_features)
                    new_file.write(dem)
                else:
                    features.append("Cannot determine\n")
                    dup_features.append("Cannot determine\n")
                    dem = "\t"
                    new_file.write(dem.join(features))
                    new_file.write(dem.join(dup_features))

