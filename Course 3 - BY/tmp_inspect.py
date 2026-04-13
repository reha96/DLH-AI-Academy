import pickle, os
p = r'c:\Users\LetzPC Gaming\Documents\GitHub\DLH-AI-Academy\Course 3 - BY\embeddings\all-MiniLM-L6-v2.pkl'
print('exists', os.path.exists(p))
with open(p, 'rb') as f:
    d = pickle.load(f)
print(type(d))
if isinstance(d, dict):
    print('keys', list(d.keys()))
    for k in ['shape', 'embeddings']:
        if k in d:
            v = d[k]
            print(k, type(v), getattr(v,'shape', None), len(v) if hasattr(v, '__len__') else None)
