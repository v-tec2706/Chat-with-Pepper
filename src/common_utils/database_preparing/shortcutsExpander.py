import csv
from csvWriter import CsvWriter

class ShortcutsExpander():

    def expand_shortcuts(self, file_in, file_out):
        f_out_writer = CsvWriter(file_out)
        with open(file_in, encoding="utf-8") as csv_file:
            read_csv = csv.reader(csv_file, delimiter='#')
            for row in read_csv:
                text = row[len(row) - 1]
                row[len(row) - 1] = self.expand_text_shortcuts(text)
                tags = row[:-1]
                text = row[len(row) - 1]
                print('TAGS:\t', tags)
                print('TEXT:\t', text)
                f_out_writer.write_tags_and_text(tags, text)

    def expand_text_shortcuts(self, text):
        words = text.split()
        for i in range(len(words)):
            words[i] = self.try_to_expand(words[i])
        final_text = ''
        for i in range(len(words)):
            final_text += words[i] + ' '
        final_text = final_text[:-1]
        return final_text

    def try_to_expand(self, word):
        word = word.lower()
        if word == '+48':
            return '48'
        if word == '1.':
            return '1'
        if word == '100.':
            return '100'
        if word == 'al.':
            return 'aleje'
        if word == 'art.':
            return 'artykuł'
        if word == 'bip':
            return 'biuletyn informacji publicznej'
        if word == 'dkg':
            return 'dekagramów'
        if word == 'doc.':
            return 'docent'
        if word == 'dr':
            return 'doktor'
        if word == 'dra':
            return 'doktora'
        if word == 'drem':
            return 'doktorem'
        if word == 'drowi':
            return 'doktorowi'
        if word == 'ds.':
            return 'do spraw'
        if word == 'ew.':
            return 'ewentualnie'
        if word == 'ha':
            return 'hektarów'
        if word == 'hab.':
            return 'habilitowany'
        if word == 'im.':
            return 'imienia'
        if word == 'inż.':
            return 'inżynier'
        if word == 'itp.':
            return 'i tym podobne'
        if word == 'ks.':
            return 'ksiądz'
        if word == 'łac.':
            return 'łaciny'
        if word == 'm.in.':
            return 'między innymi'
        if word == 'mgr':
            return 'magister'
        if word == 'mgra':
            return 'magistra'
        if word == 'mm':
            return 'milimetrów'
        if word == 'nadzw.':
            return 'nadzwyczajny'
        if word == 'n.s.d.a.p.':
            return 'narodowosocjalistycznej niemieckiej partii robotników'
        if word == 'np.':
            return 'na przykład'
        if word == 'nr':
            return 'numer'
        if word == 'nrf':
            return 'niemieckiej republiki federalnej'
        if word == 'nszz':
            return 'niezależny samorządowy związek zawodowy'
        if word == 'ok.':
            return 'około'
        if word == 'pn.':
            return 'pod nazwą'
        if word == 'pow.':
            return 'powiat'
        if word == 'pr':
            return 'public relations'
        if word == 'prof.':
            return 'profesor'
        if word == 'r.':
            return 'roku'
        if word == 'r.,':
            return 'roku,'
        if word == 'tel.':
            return 'telefon'
        if word == 'tj.':
            return 'to jest'
        if word == 'tzw.':
            return 'tak zwany'
        if word == 'ust.':
            return 'ustawy'
        if word == 'wew.':
            return 'wewnętrzny'
        if word == 'wg':
            return 'według'
        if word == 'wyd.':
            return 'wydanie'
        if word == 'zw.':
            return 'zwyczajny'
        return word

# ShortcutsExpander().expand_shortcuts('csv_files\db_191116_4000.csv', 'csv_files\db_191116_4000_shortcutsExpanded.csv')
