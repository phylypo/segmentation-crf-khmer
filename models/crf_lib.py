from kcc import *

#@title Define CRF features
# only pass in kccs list (without labels)
def kcc_to_features(kccs, i):
    maxi = len(kccs)
    kcc = kccs[i]

    features = {
        #'bias': 1.0,
        'kcc': kcc,
        't': kcc_type(kcc),
        'ns': is_no_space(kcc)
    }
    if i >= 1:
        features.update({
            'kcc[-1]'  : kccs[i-1],
            'kcc[-1]t' : kcc_type(kccs[i-1]),
            'kcc[-1:0]': kccs[i-1] + kccs[i],
            'ns-1' : is_no_space(kccs[i-1])
        })
    else:
        features['BOS'] = True

    if i >= 2:
        features.update({
            'kcc[-2]'   : kccs[i-2],
            'kcc[-2]t'  : kcc_type(kccs[i-2]),
            'kcc[-2:-1]': kccs[i-2] + kccs[i-1],
            'kcc[-2:0]' : kccs[i-2] + kccs[i-1] + kccs[i],
        })
    if i >= 3:
        features.update({
            'kcc[-3]'   : kccs[i-3],
            'kcc[-3]t'  : kcc_type(kccs[i-3]),
            'kcc[-3:0]' : kccs[i-3] + kccs[i-2] + kccs[i-1] + kccs[i],
            'kcc[-3:-1]': kccs[i-3] + kccs[i-2] + kccs[i-1],
            'kcc[-3:-2]': kccs[i-3] + kccs[i-2],
        })

    if i < maxi-1:
        features.update({
            'kcc[+1]'  : kccs[i+1],
            'kcc[+1]t'  : kcc_type(kccs[i+1]),
            'kcc[+1:0]': kccs[i] + kccs[i+1],
            'ns+1' : is_no_space(kccs[i+1])

        })
    else:
        features['EOS'] = True

    if i < maxi-2:
        features.update({
            'kcc[+2]'   : kccs[i+2],
            'kcc[+2]t'   : kcc_type(kccs[i+2]),
            'kcc[+1:+2]': kccs[i+1] + kccs[i+2],
            'kcc[0:+2]' : kccs[i+0] + kccs[i+1] + kccs[i+2],
            'ns+2' : is_no_space(kccs[i+2])
        })
    if i < maxi-3:
        features.update({
            'kcc[+3]'   : kccs[i+3],
            'kcc[+3]t'   : kcc_type(kccs[i+3]),
            'kcc[+2:+3]': kccs[i+2] + kccs[i+3],
            'kcc[+1:+3]': kccs[i+1] + kccs[i+2] + kccs[i+3],
            'kcc[0:+3]' : kccs[i+0] + kccs[i+1] + kccs[i+2] + kccs[i+3],
        })

    return features

def generate_kccs_label_per_phrase(sentence):
    phrases = sentence.split()
    print("prep_kcc_labels -- number of phrases:", len(phrases))
    final_kccs = []
    for phrase in phrases:
        kccs = seg_kcc(phrase)
        labels = [1 if (i==0) else 0 for i, k in enumerate(kccs)]
        final_kccs.extend(list(zip(kccs,labels)))
    return final_kccs

def create_kcc_features(kccs):
    return [kcc_to_features(kccs, i) for i in range(len(kccs))]

# take label in second element from kcc with label
def create_labels_from_kccs(kccs_label):
    return [str(part[1]) for part in kccs_label]

# test
'''
ts = "នៅ រសៀល ថ្ងៃ ទី ២២ ខែ កក្កដា ឆ្នាំ ២០១៩ ។"
kccs = seg_kcc(ts)
kccs_label = gen_kcc_with_label(ts) # only need for training
print("kcc with label:", kccs_label )
print("format features:", create_kcc_features(kccs))
print("create labels:", create_labels_from_kccs(kccs_label))
print("create labels:", create_kcc_features(seg_kcc("NS123")))
'''