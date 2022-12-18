

def tagging(hsv):
    h, s, v = hsv

    if s < 11 or v < 11: # 무채색
        result = dark(v)
    else:                # 유채색
        result = [color(h), level(s), level(v)]
    return result

def dark(v):    # 무채색
    if 0 <= v <= 10:
        return ('Bk', 0, 0)
    elif 11 <= v <= 43:
        return ('Bk', 1, 0)
    elif 43 <= v <= 75:
        return ('Bk', 2, 0)
    elif 76 <= v <= 100:
        return ('Bk', 3, 0)

def color(h):
    if 345 <= h or h <= 15:
        return 'R'
    elif 16 <= h <= 45:
        return 'O'
    elif 46 <= h <= 75:
        return 'Y'
    elif 76 <= h <= 105:
        return 'Ga'
    elif 106 <= h <= 135:
        return 'Gb'
    elif 136 <= h <= 165:
        return 'Gc'
    elif 166 <= h <= 195:
        return 'Ba'
    elif 196 <= h <= 225:
        return 'Bb'
    elif 226 <= h <= 255:
        return 'Bc'
    elif 256 <= h <= 285:
        return 'Pa'
    elif 286 <= h <= 315:
        return 'Pb'
    elif 316 <= h <= 344:
        return 'Pc'

def level(sv):
    if 11 <= sv <= 43:
        return 0
    elif 44 <= sv <= 75:
        return 1
    elif 76 <= sv <= 100:
        return 2

if __name__ == '__main__':
    pass