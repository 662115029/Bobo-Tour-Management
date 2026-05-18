import codecs

for fname in ['001_schema.sql', '002_seed.sql']:
    with codecs.open(fname, 'r', 'utf-16') as f:
        content = f.read()
    out = fname.replace('.sql', '_utf8.sql')
    with codecs.open(out, 'w', 'utf-8') as f:
        f.write(content)
    print('Done: ' + fname + ' -> ' + out)