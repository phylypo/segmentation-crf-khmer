# consonant and independent vowels
KHCONST = set(u'កខគឃងចឆជឈញដឋឌឍណតថទធនបផពភមយរលវឝឞសហឡអឣឤឥឦឧឨឩឪឫឬឭឮឯឰឱឲឳ')
KHVOWEL = set(u'឴឵ាិីឹឺុូួើឿៀេែៃោៅ\u17c6\u17c7\u17c8')
# subscript, diacritics
KHSUB = set(u'្')
KHDIAC = set(u"\u17c9\u17ca\u17cb\u17cc\u17cd\u17ce\u17cf\u17d0") #MUUSIKATOAN, TRIISAP, BANTOC,ROBAT,
KHSYM = set('៕។៛ៗ៚៙៘')
KHNUMBER = set(u'០១២៣៤៥៦៧៨៩0123456789') # remove 0123456789
# lunar date:  U+19E0 to U+19FF ᧠...᧿
KHLUNAR = set('᧠᧡᧢᧣᧤᧥᧦᧧᧨᧩᧪᧫᧬᧭᧮᧯᧰᧱᧲᧳᧴᧵᧶᧷᧸᧹᧺᧻᧼᧽᧾᧿')

def is_khmer_char(ch):
  if (ch >= '\u1780') and (ch <= '\u17ff'): return True
  if ch in KHLUNAR: return True
  return False

def is_start_of_kcc(ch):
  if is_khmer_char(ch):
    if ch in KHCONST: return True
    if ch in KHSYM: return True
    if ch in KHNUMBER: return True
    if ch in KHLUNAR: return True
    return False
  return True

# kcc base
def seg_kcc(str_sentence):
    str_sentence = str_sentence.replace(u'\u200b','')
    segs = []
    cur = ""
    for phr in str_sentence.split(' '):
        #print("PHR:[%s] len:%d" %(phr, len(phr)))
        for i,c in enumerate(phr):
            #print(i," c:", c)
            cur += c
            nextchar = phr[i+1] if (i+1 < len(phr)) else ""

            # cluster non-khmer chars together
            if not is_khmer_char(c) and nextchar != "" and not is_khmer_char(nextchar): continue
            # cluster number together
            if c in KHNUMBER and nextchar in KHNUMBER: continue

            # cluster non-khmer together
            # non-khmer character has no cluster
            if not is_khmer_char(c) or nextchar=="":
                segs.append(cur)
                cur=""
            elif is_start_of_kcc(nextchar) and not (c in KHSUB):
                segs.append(cur)
                cur=""
    return segs

# testing some text
'''
t1 = "យោងតាមប្រភពព័ត៌មានបានឱ្យដឹងថា កាលពីពេលថ្មីៗនេះក្រុមចក្រភពអង់គ្លេស Royal Marines ដែលមានមូលដ្ឋាននៅ Gibraltar បានរឹបអូសយកនាវាដឹកប្រេងឆៅរ
បស់អ៊ីរ៉ង់ដែលធ្វើដំណើរទៅកាន់រោងចក្រចម្រាញ់ប្រេងនៅក្នុងប្រទេសស៊ីរី ដោយក្រុងឡុងដ៍អះអាងថា ការរឹបអូសត្រូវបានគេសំដៅអនុវត្ត៕"
t2 = "This is a test."
t3 = "នៅរសៀលថ្ងៃទី២២ ខែ កក្កដា ឆ្នាំ២០១៩ ឯកឧត្តម គួច ចំរើន អភិបាលខេត្តព្រះសីហនុ"
print("kcc:", seg_kcc(t1))
'''

# generate list of (word, label), not splitting into phrases, just remove spaces
def gen_kcc_with_label(sentence):
    words = sentence.split()
    final_kccs = []
    for word in words:
        kccs = seg_kcc(word)
        labels = [1 if (i==0) else 0 for i, k in enumerate(kccs)]
        final_kccs.extend(list(zip(kccs,labels)))
    return final_kccs

# test label
'''
ts = "This is a test"
ts = "នៅ រសៀល ថ្ងៃ ទី ២២ ខែ កក្កដា ឆ្នាំ ២០១៩ ។"
kccs = seg_kcc(ts)
kl = gen_kcc_with_label(ts)
print("len of kcc:", len(kccs), " data:", kccs)
print("kcc with label len:", len(kl), " data:", kl)
'''

#@title Define char type

EN = set(u'abcdefghijklmnopqrstuvwxyz0123456789')

# E=English, C=Consonant, W=wowel, N=number, O=Other, S=subcript, D=Diacritic, NS=no_space
# roll up to: NS, C, W, S, D
NS = 'NS'
def get_type(chr):
  if chr.lower() in EN: return "NS"
  if chr in KHCONST: return "C"
  if chr in KHVOWEL: return "W"
  if chr in KHNUMBER: return "NS"
  if chr in KHSUB: return "S"
  if chr in KHDIAC: return "D"
  return "NS" #not U - same as N

# non-khmer character that we should not separate like number
# multiple characters are false
def is_no_space(k):
  if len(k) > 1: return False
  if get_type(k)==NS: return True
  return False

def kcc_type(k):
  if len(k)==1: return get_type(k)
  else: return "K" + str(len(k))

#testing '''
'''
print("kcc_type for u'\u17cb'", kcc_type(u'\u17cb'))
print("kcc_type for u'A'", kcc_type('A'))
print("kcc_type for u'២'", kcc_type('២'))
print("kcc_type for 'ថ្ងៃ'", kcc_type('ថ្ងៃ'))
print("is NS for 'A':", is_no_space("A"))
print("is NS for 'ថ្ងៃ':", is_no_space('ថ្ងៃ'))
'''