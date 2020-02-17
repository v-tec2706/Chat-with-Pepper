import unittest
from src.university_chatbot.university_conversation_bot import UniversityBot
from src.university_chatbot.university_conversation_logic_adapter import UniversityAdapter
from src.common_utils.database.database_service import DatabaseProxy
from chatterbot import ChatBot
from chatterbot.conversation import Statement
from configuration import Configuration

db = DatabaseProxy('mongodb://localhost:27017/', 'PepperChatDB')
chatbot = ChatBot(
            'testBot',
            logic_adapters=[
                {
                    'import_path': 'src.university_chatbot.university_conversation_logic_adapter'
                                   '.UniversityAdapter',
                    'database_proxy': db
                },
            ],
        )
_university_chatbot = UniversityBot('university_chatbot', db)
_university_adapter = UniversityAdapter(chatbot, database_proxy=db)

class TestUniversistyChatbot(unittest.TestCase):

    def check_phrase_response(self, question, correct_answer):
        response = _university_chatbot.get_bot_response(question)
        self.assertEqual(correct_answer.lower().strip(), response.text.lower().strip())

    def check_tags_response(self, question, correct_tags):
        # response = _university_chatbot.get_bot_response(question)
        resp = _university_adapter.process(Statement(question), None)
        doc = db.get_one_doc_from_collection_by_tags_list(Configuration.MAIN_COLLECTION.value, correct_tags)
        if doc is None:
            self.fail('get_one_doc_from_collection_by_tags_list returned None')
        self.assertEqual(doc['text'][0].lower().strip(), resp.text.lower().strip())


    # possible for future:
    # # TESTS with tags response expected
    # def test_tags_absolwent(self):
    #     self.check_tags_response(
    #         'opowiedz coś o absolwentach agh',
    #         ['absolwent']
    #     )
    #
    # def test_tags_aktualnosci(self):
    #     self.check_tags_response(
    #         'przedstaw akutalności o agh',
    #         ['aktualności:aktualność']
    #     )

    # TESTS with phrase response expected
    # 1
    def test_1_1(self):
        self.check_phrase_response(
            'ilu absolwentów wykształciła agh',
            'akademia wykształciła ponad 170 000 abwsolwentów - inżynierów i magistrów zapewniając kadrę dla naszej gospodarki'
        )

    def test_1_2(self):
        self.check_phrase_response(
            'czy istnieje jakiś dowód jakości i użyteczności wiedzy zdobywanej w agh',
            'błyskotliwe kariery wielu absolwentów agh, związane z piastowaniem przez nich wszelkich, w tym także bardzo często najwyższych stanowisk, stanowią łatwy do prześledzenia praktyczny dowód jakości i użyteczności wiedzy, jaką zdobyli oni w murach agh'
        )

    # 2
    def test_2_1(self):
        self.check_phrase_response(
            'jak obchodzono uroczystości jubileuszu otwarcia uczelni',
            'wspaniały jubileusz 100-lecia otwarcia uczelni rozpoczęliśmy 4 października 2018 roku inauguracją 100 roku akademickiego, a jego kulminacją były uroczystości w październiku 2019 roku'
        )

    # 3
    def test_3_1(self):
        self.check_phrase_response(
            'jak można poznać historię akademii',
            'historię akademii można lepiej poznać dzięki galeriom, filmom oraz wydawnictwom informacyjnym'
        )

    # 4
    def test_4_1(self):
        self.check_phrase_response(
            'kiedy została powołana uczelnia',
            'nasza uczelnia została powołana w 1913 roku, a jej otwarcie nastąpiło w 1919 roku'
        )

    def test_4_2(self):
        self.check_phrase_response(
            'kiedy otwarto uczelnię',
            'nasza uczelnia została powołana w 1913 roku, a jej otwarcie nastąpiło w 1919 roku'
        )

    def test_4_3(self):
        self.check_phrase_response(
            'oferowane kierunki kształcenia są nowe czy klasyczne',
            'zgodnie ze światowymi trendami rozwoju tworzymy nowe kierunki kształcenia, ale zachowujemy klasyczne, niezbędne do prawidłowego rozwoju nauki, techniki oraz gospodarki naszego kraju'
        )

    # 5
    def test_5_1(self):
        self.check_phrase_response(
            'jaka jest oferta dla biznesu',
            'oferta dla biznesu to: transfer, ochrona i promocja wyników badań, wynalazków oraz patentów: umowy oraz porozumienia z przemysłem, administracją oraz innymi instytucjami'
        )

    # 6
    def test_6_1(self):
        self.check_phrase_response(
            'na jakich rodzajach studiów kształci agh',
            'agh kształci na wszystkich rodzajach studiów: stacjonarnych, niestacjonarnych, doktoranckich i podyplomowych, oferując szeroki profil kształcenia dostosowany do pojawiających się trendów na rynku pracy'
        )

    def test_6_2(self):
        self.check_phrase_response(
            'kiedy wprowadzony został system boloński',
            'od roku akademickiego 2007/2008 akademia górniczo-hutnicza wprowadziła trzystopniowy system kształcenia (tak zwany system boloński)'
        )

    # 7
    def test_7_1(self):
        self.check_phrase_response(
            'ile jest oferowanych kierunków studiów podyplomowych',
            'w agh oferowanych jest około 100 kierunków studiów podyplomowych, a także kilkadziesiąt szkoleń i kursów dokształcających skierowanych zarówno do specjalistów kadry inżynierskiej , jak również do osób, które są zainteresowane zdobyciem nowej innej specjalizacji'
        )

    def test_7_2(self):
        self.check_phrase_response(
            'czy na agh istnieje kształcenie w zakresie poza inżynierskim',
            'Kształcenie w zakresie poza inżynierskim to między innymi studia w dziedzinie marketingu internetowego, informatyki i grafiki komputerowej, ochrony środowiska, rachunkowości i controllingu, bhp, szacowania i zarządzania nieruchomościami, zarządzania projektami, przedsiębiorstwem, organizacją it, zarządzania jakością oraz zarządzania sprzedażą'
        )

    # 8
    def test_8_1(self):
        self.check_phrase_response(
            'czy agh wykoszystuje e-materiały',
            'w swojej ofercie agh posiada e-materiały: e-materiały agh są dostępne bezpłatnie, na licencjach creative commons, dzięki czemu ich wykorzystanie nie ogranicza się jedynie do czytania, pobierania czy drukowania'
        )

    def test_8_2(self):
        self.check_phrase_response(
            'czy agh wykoszystuje e-learning',
            'dla pracowników i doktorantów agh, centrum e-learningu oferuje szkolenia na temat budowania i pisania e-podręczników oraz korzystania z otwartych zasobów edukacyjnych w dydaktyce akademickiej'
        )

    def test_8_3(self):
        self.check_phrase_response(
            'czy agh wykorzystuje e-podręczniki',
            'dla pracowników i doktorantów agh, centrum e-learningu oferuje szkolenia na temat budowania i pisania e-podręczników oraz korzystania z otwartych zasobów edukacyjnych w dydaktyce akademickiej'
        )

    # 10
    def test_10_1(self):
        self.check_phrase_response(
            'jaki jest adres agh',
            'adres agh: Akademia Górniczo-Hutnicza imienia Stanisława Staszica w Krakowie aleja Mickiewicza 30, 30-059 Kraków'
        )

    def test_10_2(self):
        self.check_phrase_response(
            'jaki jest telefon dla kandydatów',
            'Telefon dla kandydatów: 48 12 617 36 84'
        )

    def test_10_3(self):
        self.check_phrase_response(
            'jaki jest telefon do centrum rekrutacji',
            'Telefon centrum rekrutacji: 48 12 617 36 84'
        )

    def test_10_4(self):
        self.check_phrase_response(
            'jaki jest telefon w sprawie studiów stacjonarnych',
            'Telefon studia stacjonarne: 48 12 617 32 61'
        )

    def test_10_5(self):
        self.check_phrase_response(
            'jaki jest telefon w sprawie studiów niestacjonarnych',
            'Telefon studia niestacjonarne: 48 12 617 48 95'
        )

    def test_10_6(self):
        self.check_phrase_response(
            'jaki jest telefon w sprawie studiów podyplomowych',
            'Telefon studia podyplomowe: 48 12 617 32 81'
        )

    def test_10_7(self):
        self.check_phrase_response(
            'jaki jest telefon w sprawie studiów doktoranckich',
            'Telefon studia doktoranckie: 48 12 617 31 57 oraz 48 12 617 24 49'
        )

    def test_10_8(self):
        self.check_phrase_response(
            'jaki jest telefon do działu informacji i promocji',
            'Telefon dział informacji i promocji: 48 12 617 31 91'
        )

    def test_10_9(self):
        self.check_phrase_response(
            'jaki jest telefon do redakcji strony internetowej',
            'Telefon redakcja strony internetowej: magister Weronika Szewczyk 48 12 617 49 38, magister inżynier Maciej Tomczyk 48 12 617 48 97 oraz magister Katarzyna Wrzoszczyk 48 12 617 35 41'
        )

    def test_10_10(self):
        self.check_phrase_response(
            'jaki jest telefon do rzecznika prasowego agh',
            'Telefon rzecznik prasowy AGH magister Anna Żmuda-Muszyńska 48 12 617 25 45 oraz 48 605 109 858'
        )

    def test_10_11(self):
        self.check_phrase_response(
            'jaki jest telefon do inspektora ochrony danych osobowych',
            'Telefon inspektor ochrony danych osobowych magister Tomasz Józefko 48 12 617 53 25'
        )

    # 11
    def test_11_1(self):
        self.check_phrase_response(
            'czym jest centrum międzynarodowej promocji technologii i edukacji agh-unesco',
            'w agh od roku 2011 działa centrum międzynarodowej promocji technologii i edukacji agh-unesco, które jest pierwszą w polsce jednostką pod auspicjami unesco, inspirującą i koordynującą oraz wspierającą wymianę i transfer wiedzy i praktyki inżynierskiej oraz kształcenie na poziomie uniwersyteckim w dziedzinie nauk technicznych w wymiarze międzynarodowym, zwłaszcza adresowanym do krajów rozwijających się'
        )

    def test_11_2(self):
        self.check_phrase_response(
            'do kogo adresowane są działania centrum agh-unesco',
            'działania centrum agh-unesco wpisują się w priorytety unesco oraz agh i są adresowane do partnerów na całym świecie'
        )

    # 12
    def test_12_1(self):
        self.check_phrase_response(
            'czym jest biuletyn informacji publicznej',
            'biuletyn informacji publicznej to urzędowy publikator teleinformatyczny, składający się z ujednoliconego systemu stron w sieci informatycznej'
        )

    #
    def test_12_2(self):
        self.check_phrase_response(
            'w jakim celu został stworzony biuletyn informacji publicznej',
            'biuletyn informacji publicznej został stworzony w celu powszechnego udostępniania informacji publicznej'
        )

    # 13
    def test_13_1(self):
        self.check_phrase_response(
            'kto zatwierdził utworzenie wyższej szkoły górniczej w krakowie',
            '31 maja 1913 roku cesarz franciszek józef i zatwierdził utworzenie wyższej szkoły górniczej w krakowie'
        )

    def test_13_2(self):
        self.check_phrase_response(
            'kiedy zostało zatwierdzone  utworzenie wyższej szkoły górniczej w krakowie',
            '31 maja 1913 roku cesarz franciszek józef i zatwierdził utworzenie wyższej szkoły górniczej w krakowie'
        )

    def test_13_3(self):
        self.check_phrase_response(
            'kiedy został powołany komitet organizacyjny akademii górniczej',
            'w 1913 roku ministerstwo robót publicznych w wiedniu powołało komitet organizacyjny akademii górniczej, którego przewodniczącym został profesor józef morozewicz'
        )

    def test_13_4(self):
        self.check_phrase_response(
            'w którym roku został powołany komitet organizacyjny akademii górniczej',
            'w 1913 roku ministerstwo robót publicznych w wiedniu powołało komitet organizacyjny akademii górniczej, którego przewodniczącym został profesor józef morozewicz'
        )

    def test_13_5(self):
        self.check_phrase_response(
            'gdzie został powołany komitet organizacyjny akademii górniczej',
            'w 1913 roku ministerstwo robót publicznych w wiedniu powołało komitet organizacyjny akademii górniczej, którego przewodniczącym został profesor józef morozewicz'
        )

    def test_13_6(self):
        self.check_phrase_response(
            'kto był przewodniczącym komitetu organizacyjnego akademii górniczej',
            'w 1913 roku ministerstwo robót publicznych w wiedniu powołało komitet organizacyjny akademii górniczej, którego przewodniczącym został profesor józef morozewicz'
        )

    def test_13_7(self):
        self.check_phrase_response(
            'kiedy położono kamień węgielny pod budowę gmachu akademii górniczej',
            '15 czerwca 1923 roku położono kamień węgielny pod budowę przyszłego gmachu akademii górniczej'
        )

    def test_13_8(self):
        self.check_phrase_response(
            'kiedy powstał projekt godła akademii górniczej',
            'w 1925 roku powstał projekt godła akademii górniczej (zachowany w muzeum historii agh) sygnowany monogramem b t – bogdan treter, prawdopodobnie zatwierdzony przez zebranie ogólne profesorów'
        )

    def test_13_9(self):
        self.check_phrase_response(
            'jak zachowała się społeczność akademicka względem wpowadzenia stanu wojennego',
            '14 grudnia 1981 roku społeczność akademicka agh pod sztandarem „solidarności” odważyła się zaprotestować przeciwko stłumieniu – wprowadzeniem stanu wojennego – wywalczonego poczucia wolności i solidarności'
        )

    def test_13_10(self):
        self.check_phrase_response(
            'czy agh organizowało jakieś strajki okupacyjne podczas stanu wojennego',
            'niezależny samorządowy związek zawodowy „solidarność” agh był organizacją uczelnianą, jedyną w krakowie i jedną z trzech w kraju, które zorganizowały strajki okupacyjne w pierwszych dniach stanu wojennego'
        )

    # 14
    def test_14_1(self):
        self.check_phrase_response(
            'kiedy rozpoczęły się starania o utworzenie akademii górniczej',
            'starania o utworzenie w kraju uczelni górniczej oraz powołanie odpowiedniej kadry naukowej rozpoczęły się w drugiej połowie dziewiętnastego wieku i nasiliły wraz z uzyskaniem przez galicję autonomii'
        )

    def test_14_2(self):
        self.check_phrase_response(
            'kiedy otrzymano zezwolenie na otwarcie uczelni',
            'starania o powołanie w krakowie wyższej uczelni kształcącej inżynierów górnictwa zostały zwieńczone powodzeniem – 10 lipca 1912 roku władze krakowa otrzymały zezwolenie na otwarcie uczelni'
        )

    def test_14_3(self):
        self.check_phrase_response(
            'kto wystosował pisma do naczelnika państwa w sprawie mianowania pierwszych profesorów akademii górniczej',
            'w notatce z konferencji u prezydenta miasta krakowa juliusza lea widnieje dopisek w prawym dolnym rogu kartki na jednym z dokumentów: w kwietniu 1919 roku minister jan łukasiewicz wystosował pisma do naczelnika państwa w sprawie mianowania pierwszych profesorów akademii górniczej'
        )

    def test_14_4(self):
        self.check_phrase_response(
            'ilu profesorów mianował józef piłsudski',
            'sześciu profesorów zostało oficjalnie mianowanych przez józefa piłsudskiego 1 maja 1919 roku'
        )

    def test_14_5(self):
        self.check_phrase_response(
            'kto został wybrany pierwszym dziekanem wydziału górniczego',
            'na pierwszym posiedzeniu wydziału profesorów akademii górniczej na dziekana wydziału górniczego wybrany został profesor antoni hoborski, a prodziekanem został profesor jan stock'
        )

    def test_14_6(self):
        self.check_phrase_response(
            'kto został pierwszym prodziekanem wydziału górniczego',
            'na pierwszym posiedzeniu wydziału profesorów akademii górniczej na dziekana wydziału górniczego wybrany został profesor antoni hoborski, a prodziekanem został profesor jan stock'
        )

    def test_14_7(self):
        self.check_phrase_response(
            'kiedy odbyła się inauguracja pierwszego roku akademickiego akademii',
            '20 października 1919 roku odbyła się inauguracja pierwszego roku akademickiego w auli collegium novum uniwersytetu jagiellońskiego - józefa piłsudskiego powitała młodzież, ustawiona w szpalerze przed udekorowanym kwiatami gmachem'
        )

    def test_14_8(self):
        self.check_phrase_response(
            'gdzie odbyła się inauguracja pierwszego roku akademickiego akademii',
            '20 października 1919 roku odbyła się inauguracja pierwszego roku akademickiego w auli collegium novum uniwersytetu jagiellońskiego - józefa piłsudskiego powitała młodzież, ustawiona w szpalerze przed udekorowanym kwiatami gmachem'
        )

    def test_14_9(self):
        self.check_phrase_response(
            'kto zainaugurował pierwszy rok akademicki akademii',
            '20 października 1919 roku odbyła się inauguracja pierwszego roku akademickiego w auli collegium novum uniwersytetu jagiellońskiego - józefa piłsudskiego powitała młodzież, ustawiona w szpalerze przed udekorowanym kwiatami gmachem'
        )

    def test_14_10(self):
        self.check_phrase_response(
            'w jaki sposob akademia wychowuje studentów',
            'akademia pielęgnuje swoje tradycje i wychowuje studentów na ludzi mądrych i prawych, w duchu odpowiedzialności zawodowej i obywatelskiej, zgodnie ze swoją dewizą: „Labore creata, labori et scientiae servio”'
        )

    def test_14_11(self):
        self.check_phrase_response(
            'jaka jest dewiza agh',
            'akademia pielęgnuje swoje tradycje i wychowuje studentów na ludzi mądrych i prawych, w duchu odpowiedzialności zawodowej i obywatelskiej, zgodnie ze swoją dewizą: „Labore creata, labori et scientiae servio”'
        )

    # 15
    def test_15_1(self):
        self.check_phrase_response(
            'co stanowi godło agh',
            'godło akademii górniczo-hutniczej stanowi stylizowany orzeł z koroną i tarczą, na której umieszczone są perlik i żelazo (godło górnicze) oraz inicjały agh'
        )

    def test_15_2(self):
        self.check_phrase_response(
            'kiedy zaprojektowano godło agh',
            'obecna wersja godła agh została zaprojektowana na podstawie rysunku wykonanego w 1925 roku przez docenta krakowskiej asp bogdana tretera oraz graficznej aplikacji rysunku zachowanej na dyplomie przyznanym ignacemu mościckiemu w 1934 roku'
        )

    def test_15_3(self):
        self.check_phrase_response(
            'do czego przeznaczone jest godło agh',
            'godło agh przeznaczone jest wyłącznie do promowania historii oraz dziedzictwa naukowego uczelni i zostało zastrzeżone dla dokumentów rektora akademii górniczo-hutniczej'
        )

    def test_15_4(self):
        self.check_phrase_response(
            'czy godło agh jest zastrzeżone',
            'godło agh przeznaczone jest wyłącznie do promowania historii oraz dziedzictwa naukowego uczelni i zostało zastrzeżone dla dokumentów rektora akademii górniczo-hutniczej'
        )

    # 16
    def test_16_1(self):
        self.check_phrase_response(
            'z czego zbudowany jest znak graficzny agh',
            'znak graficzny akademii górniczo-hutniczej zbudowany jest z sygnetu oraz logotypu'
        )

    def test_16_2(self):
        self.check_phrase_response(
            'co służy identyfikacji wizualnej agh',
            'znak graficzny agh jest jedynym znakiem służącym codziennej identyfikacji wizualnej akademii górniczo-hutniczej'
        )

    # 17
    def test_17_1(self):
        self.check_phrase_response(
            'jaka jest symbolika barw agh',
            'symbolika barw agh jest nastęująca: zieleń odzwierciedla naturę, pola i lasy; czerń nawiązuje do głębi kopalń oraz symbolizuje cechy niezbędne w zawodzie górniczym i hutniczym, takie jak rozwaga, mądrość i stałość; czerwień to barwa ognia i roztopionego żelaza'
        )

    def test_17_2(self):
        self.check_phrase_response(
            'jakie są barwy agh',
            'barwami akademii górniczo-hutniczej są zieleń, czerń oraz czerwień'
        )

    # 18
    def test_18_1(self):
        self.check_phrase_response(
            'jakie są insygnia władzy agh',
            'insygnia władzy agh to: łańcuch, berło i topór ceremonialny oraz pierścień'
        )

    # 19
    def test_19_1(self):
        self.check_phrase_response(
            'kim jest doctor honoris causa',
            'doctor honoris causa (z łaciny dla zaszczytu) to honorowy tytuł naukowy nadawany przez uczelnie osobom szczególnie zasłużonym dla nauki i kultury'
        )

    def test_19_2(self):
        self.check_phrase_response(
            'czy istnieje jakiś honorowy tytuł naukowy dla osób szczególnie zasłużonych dla nauki i kultury',
            'doctor honoris causa (z łaciny dla zaszczytu) to honorowy tytuł naukowy nadawany przez uczelnie osobom szczególnie zasłużonym dla nauki i kultury'
        )

    # 20
    def test_20_1(self):
        self.check_phrase_response(
            'kto przyznaje tytuł zasłużony dla agh',
            'tytuł zasłużony dla agh przyznaje senat akademii podejmując uchwałę raz w roku na czerwcowym posiedzeniu'
        )

    def test_20_2(self):
        self.check_phrase_response(
            'kiedy przyznawane są tytuły zasłużony dla agh',
            'tytuł zasłużony dla agh przyznaje senat akademii podejmując uchwałę raz w roku na czerwcowym posiedzeniu'
        )

    def test_20_3(self):
        self.check_phrase_response(
            'kiedy odbywa się wręczenie tutułów zasłużony dla agh',
            'wręczenie insygniów związanych z tytułem "zasłużony dla agh" odbywa się w czasie inauguracji roku akademickiego'
        )

    # 21
    def test_21_1(self):
        self.check_phrase_response(
            'czym jest tytuł honorowego konsula agh',
            'tytuł honorowego konsula agh nadawany jest osobom związanym z uczelnią, których działalność przyczyniła się do jej rozwoju i promocji zgodnie z artykułem, tytułu tego nie mogą uzyskać aktualni pracownicy agh'
        )

    def test_21_2(self):
        self.check_phrase_response(
            'komu nadawany jest tytuł honorowego konsula agh',
            'tytuł honorowego konsula agh nadawany jest osobom związanym z uczelnią, których działalność przyczyniła się do jej rozwoju i promocji zgodnie z artykułem, tytułu tego nie mogą uzyskać aktualni pracownicy agh'
        )

    def test_21_3(self):
        self.check_phrase_response(
            'kto może otrzymać tytuł honorowego konsula agh',
            'tytuł honorowego konsula agh nadawany jest osobom związanym z uczelnią, których działalność przyczyniła się do jej rozwoju i promocji zgodnie z artykułem, tytułu tego nie mogą uzyskać aktualni pracownicy agh'
        )

    # 22
    def test_22_1(self):
        self.check_phrase_response(
            'komu nadawany jest tytuł profesora honorowego agh',
            'tytuł profesora honorowego agh nadaje się wybitnym uczonym, twórcom techniki oraz innym osobom, które są czynnymi lub emerytowanymi pracownikami uczelni; kandydat do tytułu musi posiadać stopień naukowy doktora'
        )

    # 23
    def test_23_1(self):
        self.check_phrase_response(
            'jaki jest skład rady uczelni',
            'w skład rady uczelni wchodzi sześć osób powołanych przez senat agh, w tym trzy osoby spoza wspólnoty uczelni'
        )

    def test_23_2(self):
        self.check_phrase_response(
            'jakie osoby są członkami pierwszej rady uczelni',
            'Członkami pierwszej rady uczelni są: profesor doktor habilitowany inżynier Janusz Filipiak, magister inżynier Bogusław Ochab, doktor inżynier Krzysztof Pawiński, profesor doktor habilitowany inżynier Zbigniew Kąkol, profesor doktor habilitowany inżynier Kazimierz Wiatr oraz profesor doktor habilitowany inżynier Magdalena Hasik'
        )

    def test_23_3(self):
        self.check_phrase_response(
            'jakie są zadania rady uczelni',
            'Do zadań Rady Uczelni należy między innymi: opiniowanie projektu strategii uczelni, opiniowanie projektu statutu, monitorowanie gospodarki finansowej uczelni, monitorowanie zarządzania uczelnią'
        )

    def test_23_4(self):
        self.check_phrase_response(
            'kiedy kończy się kadencja rady uczelni',
            'Kadencja pierwszej rady uczelni potrwa do 31 grudnia 2020 roku'
        )

    # 24
    def test_24_1(self):
        self.check_phrase_response(
            'czym jest senat',
            'senat jest najważniejszym ciałem kolegialnym uczelni'
        )

    def test_24_2(self):
        self.check_phrase_response(
            'jakie sprawy rozpoznaje senat',
            'Senat rozpatruje każdą sprawę, którą uzna za istotną dla Uczelni'
        )

    def test_24_3(self):
        self.check_phrase_response(
            'co należy do kompetencji senatu',
            'Do kompetencji Senatu należy między innymi: uchwalanie Statutu Uczelni, uchwalanie Regulaminu Studiów, Regulaminu Studiów Doktoranckich oraz Regulaminu Studiów Podyplomowych'
        )

    def test_24_4(self):
        self.check_phrase_response(
            'jaki jest skład senatu',
            'W skład Senatu wchodzą: Rektor jako jego przewodniczący, prorektorzy, dziekani wydziałów, przedstawiciele poszczególnych grup społeczności akademickiej wybrani zgodnie z ordynacją wyborczą'
        )

    # 25
    def test_25_1(self):
        self.check_phrase_response(
            'jaka jest struktura agh',
            'struktura akademii górniczo-hutniczej obejmuje następujące jednostki organizacyjne: wydziały i inne podstawowe jednostki organizacyjne, jednostki pozawydziałowe, administracja centralna i inne jednostki związane z działalnością uczelni, szkoły doktorskie'
        )

    # 26
    def test_26_1(self):
        self.check_phrase_response(
            'jakie są piony administracji centralnej',
            'piony administracji centralnej to: Pion Rektora, Pion Kształcenia, Pion Nauki, Pion Współpracy, Pion Ogólny, Pion Spraw Studenckich, Pion Kanclerza, Pion Kwestury'
        )

    # 27
    def test_27_1(self):
        self.check_phrase_response(
            'co tworzy pion rektora',
            'pion rektora tworzą stanowiska i jednostki merytorycznie podległe rektorowi, a organizacyjnie podległe dyrektorowi biura rektora'
        )

    def test_27_2(self):
        self.check_phrase_response(
            'czym jest biuro rektora',
            'biuro rektora zapewnia administracyjną i merytoryczną obsługę urzędu i działalności rektora oraz senatu'
        )

    # 28
    def test_28_1(self):
        self.check_phrase_response(
            'co zapewnia pion kształcenia',
            'pion kształcenia zapewnia administracyjną realizację uprawnień i obowiązków prorektora do spraw kształcenia'
        )

    def test_28_2(self):
        self.check_phrase_response(
            'komu podlega uczelniana komisja rekrutacyjna',
            'prorektorowi do spraw kształcenia podlega Uczelniana Komisja Rekrutacyjna oraz Uczelniany Zespół do spraw Jakości Kształcenia'
        )

    def test_28_3(self):
        self.check_phrase_response(
            'komu podlega uczelniany zespół do spraw jakości kształcenia',
            'prorektorowi do spraw kształcenia podlega Uczelniana Komisja Rekrutacyjna oraz Uczelniany Zespół do spraw Jakości Kształcenia'
        )

    def test_28_4(self):
        self.check_phrase_response(
            'jakie jednostki są podległe prorektorowi do spraw kształcenia',
            'prorektorowi do spraw kształcenia podlega Uczelniana Komisja Rekrutacyjna oraz Uczelniany Zespół do spraw Jakości Kształcenia'
        )

    # 29
    def test_29_1(self):
        self.check_phrase_response(
            'jaki pion  zapewnia realizację uprawnień i obowiązków prorektora do spraw nauki',
            'pion nauki zapewnia administracyjną realizację uprawnień i obowiązków prorektora do spraw nauki, który kieruje pionem'
        )

    def test_29_2(self):
        self.check_phrase_response(
            'co zapewnia obsługę badań naukowych w uczelni',
            'pion nauki zapewnia administracyjną, formalno-prawną, techniczną i informacyjną obsługę sfery badań naukowych w uczelni i jej promocji w tym zakresie'
        )

    # 30
    def test_30_1(self):
        self.check_phrase_response(
            'czym jest pion współpracy',
            'pion współpracy zapewnia administracyjną realizację uprawnień i obowiązków prorektora do spraw współpracy, który kieruje pionem'
        )

    # 31
    def test_31_1(self):
        self.check_phrase_response(
            'czym jest pion spraw studenckich',
            'pion spraw studenckich zapewnia administracyjną realizację uprawnień i obowiązków prorektora do spraw studenckich, który kieruje pionem'
        )

    # 32
    def test_32_1(self):
        self.check_phrase_response(
            'czym jest pion ogólny',
            'pion ogólny zapewnia administracyjną realizację uprawnień i obowiązków prorektora do spraw ogólnych, który kieruje pionem'
        )

    # 33
    def test_33_1(self):
        self.check_phrase_response(
            'co obejmuje pion kanclerza',
            'pion kanclerza obejmuje gospodarcze, techniczne, organizacyjne, prawne i administracyjne funkcjonowanie uczelni w zakresie zwykłego zarządu'
        )

    def test_33_2(self):
        self.check_phrase_response(
            'kto kieruje pionem kanclerza',
            'pionem kanclerza kieruje kanclerz uczelni'
        )

    # 34
    def test_34(self):
        self.check_phrase_response(
            'kto jest kwestorem agh',
            'Kwestor AGH - magister Maria Ślizień'
        )

    # 35
    def test_35_1(self):
        self.check_phrase_response(
            'czym jest konwent agh',
            'konwent agh jest wyjątkowym w skali kraju ciałem kolegialnym działającym przy wyższej uczelni'
        )

    def test_35_2(self):
        self.check_phrase_response(
            'jakie jednostki skupia w swych szeregach konwent agh',
            'skupiając w swych szeregach ścisłe władze województw oraz menedżerów wiodących przedsiębiorstw, konwent agh stanowi cenny organ doradczy uczelni'
        )

    def test_35_3(self):
        self.check_phrase_response(
            'jak często odbywają się obrady konwentu agh',
            'odbywające się dwa razy w roku obrady konwentu agh są platformą wymiany doświadczeń na styku szkolnictwa wyższego z przemysłem oraz samorządami'
        )

    def test_35_4(self):
        self.check_phrase_response(
            'czym są obrady konewntu agh',
            'odbywające się dwa razy w roku obrady konwentu agh są platformą wymiany doświadczeń na styku szkolnictwa wyższego z przemysłem oraz samorządami'
        )

    # 36
    def test_36_1(self):
        self.check_phrase_response(
            'czym jest rada seniorów agh',
            'Rada seniorów agh jest kontynuatorką konwentu seniorów agh, powołanego 18 lutego 1985 roku przez ówczesnego rektora agh profesora antoniego kleczkowskiego'
        )

    def test_36_2(self):
        self.check_phrase_response(
            'jaka jest liczba członków rady seniorów agh',
            'Liczba członków rady seniorów nie może przekroczyć 30 osób; kadencja w radzie jest dożywotnia, ustanie członkostwa w radzie może nastąpić jedynie na podstawie decyzji osoby rezygnującego z członkostwa'
        )

    def test_36_3(self):
        self.check_phrase_response(
            'jak długa jest kadencja w radzie seniorów agh',
            'Liczba członków rady seniorów nie może przekroczyć 30 osób; kadencja w radzie jest dożywotnia, ustanie członkostwa w radzie może nastąpić jedynie na podstawie decyzji osoby rezygnującego z członkostwa'
        )

    # 37
    def test_37_1(self):
        self.check_phrase_response(
            'jaki jest pełny skład rady seniorów',
            'pełny skład rady seniorów jest następujący: profesor Jerzy Niewodniczański – przewodniczący rady seniorów; profesor Kazimierz Jeleń – wiceprzewodniczący rady seniorów; profesor Józef Dańko – sekretarz rady seniorów; pozostali członkowie rady seniorów to: profesor Bronisław Barchański, profesor Wojciech Batko, profesor Stanisław Białas, profesor Aleksander Długosz, profesor Zbigniew Fajklewicz, profesor Aleksander Garlicki, profesor Józef Giergiel, profesor Andrzej Gołaś, profesor Henryk Górecki, profesor Mirosław Handke, profesor Wojciech Kapturkiewicz, profesor Danuta Kisielewska, profesor Andrzej Korbel, profesor Zygmunt Kolenda, profesor Stanisław Kreczmer, profesor Barbara Kwiecińska, profesor Jan Lech Lewandowski, profesor Andrzej Łędzki, profesor Janusz Łuksza, profesor Lidia Maksymowicz, profesor Andrzej Manecki, profesor Stanisław Mitkowski, profesor Janusz Roszkowski, profesor Jerzy Sędzimir, profesor Zbigniew Sitek, profesor Andrzej Skorupa, profesor Józef Zasadziński'
        )

    def test_37_2(self):
        self.check_phrase_response(
            'kto jest przewodniczącym rady seniorów',
            'profesor Jerzy Niewodniczański – przewodniczący rady seniorów'
        )

    def test_37_3(self):
        self.check_phrase_response(
            'kto jest wiceprzewodniczącym rady seniorów',
            'profesor Kazimierz Jeleń – wiceprzewodniczący rady seniorów'
        )

    def test_37_4(self):
        self.check_phrase_response(
            'kto jest sekretarzem rady seniorów',
            'profesor Józef Dańko – sekretarz rady seniorów'
        )

    # 38
    def test_38_1(self):
        self.check_phrase_response(
            'kto prowadzi posiedzenia rady seniorów',
            'posiedzenia rady seniorów prowadził przewodniczący rady jerzy niewodniczański, lub – pod jego nieobecność – wiceprzewodniczący kazimierz jeleń'
        )

    def test_38_2(self):
        self.check_phrase_response(
            'co jest w programie posiedzeń rady seniorów agh',
            'stałymi pozycjami programów posiedzeń rady seniorów były wystąpienia rektora lub prorektora agh obecnego na posiedzeniu oraz sprawy bieżące (w tym sprawozdanie z ostatniego posiedzenia senatu agh)'
        )

    # 39
    def test_39_1(self):
        self.check_phrase_response(
            'czym jest system identyfikacji wizualnej agh',
            'system identyfikacji wizualnej agh to zespół reguł oraz konsekwentnie zaprojektowanych wzorców, które mają utrwalać pożądane opinie na temat uczelni wśród pracowników, studentów i szeroko rozumianych odbiorców zewnętrznych'
        )

    # 40
    def test_40_1(self):
        self.check_phrase_response(
            'czym jest księga identyfikacji wizualnej',
            'księga identyfikacji wizualnej to uproszczone kompendium wiedzy na temat systemu wizualnego akademii górniczo-hutniczej'
        )

    def test_40_2(self):
        self.check_phrase_response(
            'co zawiera księga identyfikacji wizualnej',
            'księga indentyfikacji wizualnej zawiera opis podstawowych elementów identyfikacji, porządkuje elementy wizualne w celu prawidłowego kreowania wizerunku uczelni oraz wyznacza zasady w zakresie wykorzystania elementów identyfikujących uczelnię w promocji'
        )

    # 41
    def test_41_1(self):
        self.check_phrase_response(
            'jakie są wersje znaku graficznego agh',
            'znak graficzny agh posiada trzy wersje podstawowe: wersję wielobarwną oraz dwie wersje jednobarwne - pozytywową i negatywową'
        )

    # 42
    def test_42_1(self):
        self.check_phrase_response(
            'jak umieszczona jest nazwa uczelni w znaku graficznym agh',
            'w znaku graficznym agh pełna nazwa uczelni umieszczona jest pod znakiem agh i wyśrodkowana względem pionowej osi sygnetu'
        )

    # 43
    def test_43_1(self):
        self.check_phrase_response(
            'gdzie znajduje się informacja o zamawianiu wizytówek',
            'informacja odnośnie zamawiania wizytówek dla pracowników agh znajduje się w  komunikacie biura kanclerza numer 29/2009'
        )

    # 44
    def test_44_1(self):
        self.check_phrase_response(
            'czy uczelnia dyspoonuje bogatą infrastrukturą',
            'uczelnia dysponuje niezwykle bogatą infrastrukturą, nowoczesnym zapleczem dydaktycznym i naukowym, bazą mieszkaniową oraz doskonale wyposażonymi obiektami sportowymi'
        )

    def test_44_2(self):
        self.check_phrase_response(
            'ile wynosi łączna powierzchnia użytkowa budynków należących do agh',
            'budynki należące do agh, których łączna powierzchnia użytkowa wynosi 350 tysięcy metrów kwadratowych, zlokalizowane są na terenie: Krakowa (98%), Łukęcina, Krynicy, Miękinii i Regulic'
        )

    def test_44_3(self):
        self.check_phrase_response(
            'gdzie zlokalizowane sa budynki należące do agh',
            'budynki należące do agh, których łączna powierzchnia użytkowa wynosi 350 tysięcy metrów kwadratowych, zlokalizowane są na terenie: Krakowa (98%), Łukęcina, Krynicy, Miękinii i Regulic'
        )

    def test_44_4(self):
        self.check_phrase_response(
            'ile miejsc posiada kompus agh',
            'agh posiada największy kampus w polsce - 8000 miejsc, 20 domów studenckich (akademików), 38 hektarów powierzchni'
        )

    def test_44_5(self):
        self.check_phrase_response(
            'ile domów studenckich posiada kampus agh',
            'agh posiada największy kampus w polsce - 8000 miejsc, 20 domów studenckich (akademików), 38 hektarów powierzchni'
        )

    # 45
    def test_45_1(self):
        self.check_phrase_response(
            'jakie są ostatnie inwestycje agh',
            'ostatnie inwestycje agh to między innymi: rozbudowa budynku S-1, nowy budynek dla Wydziału Informatyki, Elektroniki i Telekomunikacji, Akademickie Centrum Kultury Klub STUDIO, Centrum Energetyki – największa inwestycja w historii uczelni, Akademickie Centrum Materiałów i Nanotechnologii AGH, Hala maszyn ACK CYFRONET AGH, Centrum Informatyki, Centrum Ceramiki, budynek Wydziału Energetyki i Paliw, Basen AGH, Centrum Dydaktyki, Laboratorium Edukacyjno-Badawcze Odnawialnych Źródeł i Poszanowania Energii w Miękini, Biblioteka Główna AGH'
        )

    # 46
    def test_46_1(self):
        self.check_phrase_response(
            'gdzie położony jest kampus agh',
            'kampus akademicki o powierzchni 38 hektarów położony jest w obrębie ulic: aleje mickiewicza, reymonta, buszka, tokarskiego, armii krajowej, gramatyka, nawojki oraz czarnowiejskiej'
        )

    def test_46_2(self):
        self.check_phrase_response(
            'jaka jest lokalizacja kampusu agh',
            'niewątpliwym atutem kampusu akademickiego jest doskonała lokalizacja (kilkanaście minut spacerem do rynku głównego), jak również dostęp do szerokiej sieci połączeń autobusowych i tramwajowych'
        )

    def test_46_3(self):
        self.check_phrase_response(
            'jakie są atuty kampusu agh',
            'niewątpliwym atutem kampusu akademickiego jest doskonała lokalizacja (kilkanaście minut spacerem do rynku głównego), jak również dostęp do szerokiej sieci połączeń autobusowych i tramwajowych'
        )

    def test_46_4(self):
        self.check_phrase_response(
            'co wchodzi w skład kampusu agh',
            'w skład kampusu akademickiego wchodzą: Pawilony dydaktyczno-naukowe, Biblioteka Główna, Stołówki studenckie, Przychodnia zdrowia, Domy studenckie, Hale sportowe, Kluby studenckie, Obiekty handlowo-usługowe, Obiekty pomocnicze'
        )

    def test_46_5(self):
        self.check_phrase_response(
            'czy istnieją jakieś udogodnienia dla rowerzystów na terenie kampusu',
            'na terenie kampusu znajdują się liczne stojaki rowerowe, jak również zadaszone parkingi rowerowe'
        )

    # 47
    def test_47_1(self):
        self.check_phrase_response(
            'jaka jest powierzchnia miasteczka studenckiego agh',
            'największe miasteczko studenckie w polsce, o powierzchni 13 hektarów, zlokalizowane jest w obrębie kampusu akademickiego agh pomiędzy ulicami: reymonta, buszka, tokarskiego, armii krajowej, nawojki i miechowską'
        )

    def test_47_2(self):
        self.check_phrase_response(
            'gdzie zlokalizowane jest miasteczko studenckieg agh',
            'największe miasteczko studenckie w polsce, o powierzchni 13 hektarów, zlokalizowane jest w obrębie kampusu akademickiego agh pomiędzy ulicami: reymonta, buszka, tokarskiego, armii krajowej, nawojki i miechowską'
        )

    def test_47_3(self):
        self.check_phrase_response(
            'co znajduje się na terenie miasteczka studenckiego oprócz domów studenckich',
            'na terenie miasteczka studenckiego oprócz 20 domów studenckich znajdują się między innymi: kluby studenckie, boiska sportowe, przedszkole, żłobek, korty tenisowe, supermarket, basen agh, bank oraz różne punkty handlowe, gastronomiczne i usługowe'
        )

    def test_47_4(self):
        self.check_phrase_response(
            'jaki jest dostęp do internetu w akademikach',
            'w akademikach agh wszystkie pokoje oddane do dyspozycji studentów posiadają bezpłatny dostęp do internetu'
        )

    # 48
    def test_48_1(self):
        self.check_phrase_response(
            'gdzie odbywają się zajęcia dydaktyczne',
            'zajęcia dydaktyczne odbywają się w: ponad 150 salach wykładowych, ponad 200 salach ćwiczeniowych, ponad 680 salach laboratoryjnych, ponad 40 salach konferencyjnych'
        )

    def test_48_2(self):
        self.check_phrase_response(
            'jak wyposażone są sale wykładowe i konferencyjne',
            'sale wykładowe i konferencyjne wyposażone są między innymi w: projektory multimedialne, wizualizery, tablice i monitory interaktywne, ekrany projekcyjne, systemy wideokonferencji, mikrofony, profesjonalne nagłośnienie czy też system tłumaczeń symultanicznych'
        )

    # 49
    def test_49_1(self):
        self.check_phrase_response(
            'jakie są inwestycje w baze sportowo rekreacyjną',
            'inwestycje w baze sportowo rekreacyjną to unowocześnienie studium wychowania fizycznego i sportu przy ulicy piastowskiej oraz wybudowanie basen, w którym znajdują się sauna, kręgielnia i siłownia'
        )

    # 50
    def test_50_1(self):
        self.check_phrase_response(
            'jakie jest wyposażenie basenu agh',
            'wyposażenie basenu agh to: basen sportowy (25-metrowy, posiadający homologację pzp), basen szkoleniowy (25-metrowy) oraz basen rekreacyjny z hydromasażami, jak również: jacuzzi, zjeżdżalnia oraz sauny (sucha i mokra)'
        )

    def test_50_2(self):
        self.check_phrase_response(
            'co oferuje basen agh',
            'pod okiem doświadczonych i wykwalifikowanych instruktorów basen agh oferuje: naukę i doskonalenie pływania dla niemowląt, dzieci, młodzieży i dorosłych, gimnastykę w wodzie dla kobiet w ciąży, aquaaerobik oraz ćwiczenia rehabilitacyjne w wodzie'
        )

    # 51
    def test_51_1(self):
        self.check_phrase_response(
            'gdzie usytuowane jest boisko',
            'nowoczesne boisko usytuowane jest w samym centrum studenckiego osiedla i ma wymiary 67x40 metrów, ale istnieje także możliwość podzielenia go na dwa mniejsze place do gry'
        )

    def test_51_2(self):
        self.check_phrase_response(
            'jakie wymiary ma boisko na osiedlu studenckim',
            'nowoczesne boisko usytuowane jest w samym centrum studenckiego osiedla i ma wymiary 67x40 metrów, ale istnieje także możliwość podzielenia go na dwa mniejsze place do gry'
        )

    def test_51_3(self):
        self.check_phrase_response(
            'w jaką nawierzchnię wyposażone jest boisko',
            'boisko wyposażone jest w sztuczną nawierzchnię, która umożliwia grę praktycznie przez cały rok, jest również oświetlone i ogrodzone'
        )

    def test_51_4(self):
        self.check_phrase_response(
            'w jakich godzinach można korzystać z boiska na miasteczku studenckim',
            'mieszkańcy miasteczka studenckiego agh mogą korzystać z boiska codziennie w godzinach 7:30 - 22:30 dokonując rezerwacji poprzez system elektroniczny'
        )

    # 52
    def test_52_1(self):
        self.check_phrase_response(
            'gdzie odbywają się zajęcia z wychowania fizycznego',
            'obligatoryjne zajęcia z wychowania fizycznego odbywają się w salach i obiektach otwartych prowadzonych przez studium wychowania fizycznego i sportu agh'
        )

    def test_52_2(self):
        self.check_phrase_response(
            'co obejmuje baza sportowa swfis agh',
            'baza sportowa swfis agh obejmuje: nowoczesne hale ze sztuczną nawierzchnią, nagłośnieniem, cyfrowymi tablicami wyników, dwie nowoczesne siłownie o profilu rekreacyjnym oraz siłowym, salę do aerobiku i ćwiczeń przy muzyce z nagłośnieniem, boisko piłkarskie, sale do gry w tenisa stołowego, stanowiska treningowe szermierki dla osób niepełnosprawnych, 3 wysokiej klasy jachty oraz kajaki, łaźnię parową'
        )

    def test_52_3(self):
        self.check_phrase_response(
            'z jakimi organizacjami współpracuje swfis agh',
            'swfis agh w szerokim zakresie współpracuje z klubem uczelnianym akademickiego związku sportowego agh, a także samorządem studentów, działem socjalnym, fundacją studentów i absolwentów „academica” oraz zrzeszeniem studentów niepełnosprawnych agh'
        )

    def test_52_4(self):
        self.check_phrase_response(
            'kto prowadzi szkolenia studentów w zakresie pomocy przedmedycznej',
            'swfis agh realizuje alternatywne zajęcia rehabilitacyjne dla studentów z problemami zdrowotnymi oraz prowadzi szkolenia studentów w zakresie pomocy przedmedycznej'
        )

    # 53
    def test_53_1(self):
        self.check_phrase_response(
            'w jakich jednostkach znajdujących się poza krakowem prowadzone jest kształcenie',
            'akademia górniczo-hutnicza prowadzi również kształcenie w jednostkach, które znajdują się poza krakowem: w Centralnym Laboratorium Techniki Strzelniczej i Materiałów Wybuchowych w Regulicach oraz Laboratorium Edukacyjno-Badawczym Odnawialnych Źródeł Energii AGH w Miękini'
        )

    def test_53_2(self):
        self.check_phrase_response(
            'gdzie znajduje się Centralne Laboratorium Techniki Strzelniczej i Materiałów Wybuchowych',
            'Centralne Laboratorium Techniki Strzelniczej i Materiałów Wybuchowych znajduje się w Regulicach'
        )

    def test_53_3(self):
        self.check_phrase_response(
            'gdzie znajduje się Laboratorium Edukacyjno-Badawcze Odnawialnych Źródeł Energii AGH',
            'Laboratorium Edukacyjno-Badawcze Odnawialnych Źródeł Energii AGH znajduje się w Miękini'
        )

    # 54
    def test_54_1(self):
        self.check_phrase_response(
            'z kim należy się skontaktować by opublikować wiadomość na stronie internetowej agh',
            'aby opublikować wiadomość na stronie internetowej agh, należy skontaktować się z pracownikami: telefon 48 12 617 49 38'
        )

    def test_54_2(self):
        self.check_phrase_response(
            'jakie informacje należy nadesłaż w celu publikacji informacji na stronie internetowej agh',
            'w celu publikacji informacji na stronie internetowej agh należy nadesłać podstawowe informacje takie jak między innymi czas, miejsce, organizator, cel, grupa odbiorców, link do strony internetowej'
        )

    # 55
    def test_55_1(self):
        self.check_phrase_response(
            'jakie osoby można znaleźć w gronie wychowanków akademii',
            'w gronie wychowanków akademii znaleźć można prezesów wielkich, międzynarodowych koncernów, osoby sprawujące funkcje publiczne (ministrowie, wojewodowie, prezydenci miast), ale także znanych i cenionych na całym świecie artystów'
        )

    def test_55_2(self):
        self.check_phrase_response(
            'co cenią sobie absolwenci',
            'absolwenci cenią sobie przede wszystkim wykształcenie zdobyte w akademii górniczo-hutniczej oraz praktyczny aspekt przekazywanej tutaj wiedzy'
        )

    def test_55_3(self):
        self.check_phrase_response(
            'czy studenci odbywają praktyki zawodowe lub staże',
            'studenci mają możliwość odbywania praktyk zawodowych oraz staży w wielu renomowanych firmach, co znacznie poprawia ich start w dorosłe, zawodowe życie'
        )

    def test_55_4(self):
        self.check_phrase_response(
            'czy studenci pracują w trakcie studiów',
            'duża część studentów podejmuje pracę już w trakcie studiów'
        )

    def test_55_5(self):
        self.check_phrase_response(
            'co sprawia, że agh od wielu lat pozostaje wiodącą polską uczelnią techniczną',
            'doskonała kadra naukowo-dydaktyczna, świetne wyposażenie, nowoczesne laboratoria i aparatura, szeroka współpraca z przemysłem i firmami nowoczesnych technologii oraz ciągła i nieustająca dbałość o jakość kształcenia sprawiają, że akademia górniczo-hutnicza imienia stanisława staszica w krakowie od stu lat pozostaje wiodącą polską uczelnią techniczną'
        )

    # 56
    def test_56_1(self):
        self.check_phrase_response(
            'co stanowi podstawę oceny skutecznośći systemu zapewnienia jakości kształcenia',
            'Podstawę oceny skuteczności Systemu Zapewnienia Jakości Kształcenia stanowią roczne raporty samooceny zatwierdzane na posiedzeniu Rad Wydziałów, a następnie przedkładane Prorektorowi do spraw Kształcenia i Pełnomocnikowi Rektora do spraw Jakości Kształcenia'
        )

    # 57
    def test_57_1(self):
        self.check_phrase_response(
            'czym jest ksiąga jakości agh',
            'zgodnie z zarządzeniem rektora agh księga jakości jest to publicznie dostępne opracowanie zawierające: zbiór wszystkich dokumentów prawnych dotyczących procesu kształcenia w uczelni, zbiór procedur obowiązujących w trakcie realizacji procesu kształcenia, w skład którego wchodzą wyodrębnione zarządzenia rektora oraz zalecenia uczelnianego zespołu do spraw jakości kształcenia, katalog dobrych praktyk, będący zbiorem przykładów rozwiązań godnych naśladowania, informacje na temat systemu zapewnienia jakości kształcenia w agh przeznaczone dla interesariuszy zewnętrznych, w szczególności dla kandydatów na studia, pracodawców i mediów'
        )

    # 58
    def test_58_1(self):
        self.check_phrase_response(
            'czym charakteryzuje się uczelniany system zapewnienia jakości kształcenia w agh',
            'uczelniany system zapewnienia jakości kształcenia w agh charakteryzuje się odpowiedniością struktur na poziomie uczelni i na poziomie wydziałów'
        )

    def test_58_2(self):
        self.check_phrase_response(
            'kto jest odpowiedzialny za jakość kształcenia na uczelni',
            'osobą odpowiedzialną za jakość kształcenia w skali uczelni jest rektor, a na wydziale dziekan; część obowiązków związanych z jakością kształcenia przejmuje prorektor do spraw kształcenia, a na wydziałach dziekan odpowiedzialny za kształcenie'
        )

    def test_58_3(self):
        self.check_phrase_response(
            'kto organizuje funkcjonowanie systemu zapewnienia jakości kształcenia',
            'osobą, która w skali uczelni organizuje funkcjonowanie systemu zapewnienia jakości kształcenia, jest pełnomocnik rektora do spraw jakości kształcenia; analogiczną rolę na wydziałach pełnią pełnomocnicy dziekanów do spraw jakości kształcenia'
        )

    def test_58_4(self):
        self.check_phrase_response(
            'czym zajmują się wydziałowe zespoły audytu dydaktycznego',
            'wydziałowe zespoły audytu dydaktycznego dbają o właściwą realizację programów kształcenia na poszczególnych kierunkach studiów, mogą prowadzić ankiety i inne analizy przebiegu kształcenia na danym kierunku, mogą wnioskować do zespołu do spraw jakości kształcenia o zmiany i modyfikacje programu kształcenia'
        )

    def test_58_5(self):
        self.check_phrase_response(
            'czym zajmuje się uczleniany zespół audytu dydaktycznego',
            'uczelniany zespół audytu dydaktycznego prowadzi kompleksową ocenę systemu jakości kształcenia na poszczególnych wydziałach; audyt polega na analizie dokumentów dotyczących kształcenia na wydziale oraz wizytacji wydziału'
        )

    def test_58_6(self):
        self.check_phrase_response(
            'co określa obowiązki rektora w zakresie jakości kształcenia',
            'obowiązki rektora w zakresie jakości kształcenia określa Uchwała Senatu AGH numer 253/2012 z dnia 28 listopada 2012 roku'
        )

    # 59
    def test_59_1(self):
        self.check_phrase_response(
            'czym są krajowe ramy kwalifikacji',
            'Krajowe Ramy Kwalifikacji (National Qualifications Framework) to opis wzajemnych relacji między kwalifikacjami, integrujący różne krajowe podsystemy kwalifikacji, służący większej przejrzystości, dostępności i jakości kwalifikacji, stworzony dla potrzeb rynku pracy i społeczeństwa obywatelskiego'
        )

    # 60
    def test_60_1(self):
        self.check_phrase_response(
            'jakim komisjom akredytacyjnym podlega jakość kształcenia w agh',
            'jakość kształcenia w akademii górniczo-hutniczej imienia stanisława staszica w krakowie podlega ocenom komisji akredytacyjnych: Polska Komisja Akredytacyjna, Komisja Akredytacyjna Uczelni Technicznych (KAUT), European Network for Accreditation of Engineering Education (ENAEE) oraz ABET (Accreditation Board for Engineering and Technology)'
        )

    # 61
    def test_61_1(self):
        self.check_phrase_response(
            'jakie formy pomocy i wsparcia proponowane są w ramach programu adapter',
            'w ramach programu adapter proponowane są dwie niezależne od siebie formy pomocy i wsparcia: cykl warsztatów oraz indywidualne spotkania w Punkcie Konsultacyjnym, w trakcie których promowane są odpowiednie postawy studenckie i sposoby redukcji czynników ryzyka'
        )

    # 62
    def test_62_1(self):
        self.check_phrase_response(
            'jakie jest cel studium doskonalenia dydaktycznego',
            'Celem Studium doskonalenia dydaktycznego powołanego na wydziale humanistycznym jest podnoszenie jakości prowadzonych zajęć dydaktycznych przez asystentów, lektorów, instruktorów zatrudnionych w AGH, a także doktorantów pierwszego roku studiów poprzez zobowiązanie do odbycia 75-godzinnego kursu kształcenia pedagogicznego'
        )

    # 63
    def test_63_1(self):
        self.check_phrase_response(
            'czym jest minimum kadrowe',
            'Jednym z wielu, ale niezwykle ważnym wymogiem by prowadzić studia wyższe jest tak zwane minimum kadrowe, czyli minimalna liczba i kwalifikacje nauczycieli akademickich zatrudnionych w pełnym wymiarze czasu'
        )

    # 64
    def test_64_1(self):
        self.check_phrase_response(
            'jaki wydział otrzymał status krajowego naukowego ośrodka wiodącego',
            'w lipcu 2012 roku konsorcjum kierowane przez wydział fizyki i informatyki stosowanej agh jako pierwsze w kraju otrzymało status krajowego naukowego ośrodka wiodącego (know) w dziedzinie nauk fizycznych'
        )

    def test_64_2(self):
        self.check_phrase_response(
            'kiedy wydział fizyki i informatyki stosowanej otrzymał status krajowego naukowego ośrodka wiodącego',
            'w lipcu 2012 roku konsorcjum kierowane przez wydział fizyki i informatyki stosowanej agh jako pierwsze w kraju otrzymało status krajowego naukowego ośrodka wiodącego (know) w dziedzinie nauk fizycznych'
        )

    def test_64_3(self):
        self.check_phrase_response(
            'czym jest know',
            'know (krajowy naukowy ośrodek wiodący) to pierwszy w polsce program wspierania najlepszych jednostek naukowych'
        )

    def test_64_4(self):
        self.check_phrase_response(
            'czym jest krajowy naukowy ośroodek wiodący',
            'know (krajowy naukowy ośrodek wiodący) to pierwszy w polsce program wspierania najlepszych jednostek naukowych'
        )

    def test_64_5(self):
        self.check_phrase_response(
            'co gwarantuje status know',
            'status know gwarantuje specjalne dofinansowanie w latach 2012-2017 przeznaczone na wzmocnienie potencjału naukowego i badawczego, rozwój kadry naukowej, kreowanie atrakcyjnych warunków pracy badawczej, budowanie silnej i rozpoznawalnej marki, a także na wyższe wynagrodzenia naukowców czy zatrudnienie w polsce zagranicznych uczonych'
        )

    # 65
    def test_65_1(self):
        self.check_phrase_response(
            'co jest miernikiem poziomu zaawansowania pracowni uczelnianej',
            'miejsce publikacji wyników badań jest stosowanym w uczelni miernikiem poziomu zaawansowania pracowni'
        )

    def test_65_2(self):
        self.check_phrase_response(
            'gdzie publikowane są wyniki badań dokonanych w laboratoriach agh',
            'wyniki badań dokonanych w laboratoriach agh publikowane są w najlepszych czasopismach o zasięgu światowym'
        )

    def test_65_3(self):
        self.check_phrase_response(
            'jakie typu laboratoriów funkcjonują w agh',
            'oprócz laboratoriów badawczych w agh funkcjonują także laboratoria technologiczno-naukowe o charakterze usługowym'
        )

    def test_65_4(self):
        self.check_phrase_response(
            'iloma laboratoriami dysponuje uczelnia',
            'uczelnia dysponuje ponad 700 laboratoriami'
        )

    def test_65_5(self):
        self.check_phrase_response(
            'co jest niezbędne w drodze do naukowego sukcesu',
            'w drodze do naukowego sukcesu niezbędnym narzędziem jest nowoczesna aparatura, stanowiąca kluczowe wsparcie dla prowadzonych badań'
        )

    def test_65_6(self):
        self.check_phrase_response(
            'jakie są przykłądy używania nowoczesnej aparatury w badaniach naukowych',
            'przykładami używania w badaniach naukowych nowoczesnej aparatury mogą być najpotężniejsze w tej części europy mikroskopy do badania struktury metali, czy tak zwana sztywna maszyna wytrzymałościowa, pozwalająca precyzyjnie badać krytyczne dla bezpiecznego górnictwa procesy pękania i kruszenia skał, mikroskopy elektronowe, aparatury do kompleksowych badań ciał stałych, a w szczególności ich powierzchni, spektrometry masowe, liczne urządzenia do badań środowiskowych i tym podobne'
        )

    def test_65_7(self):
        self.check_phrase_response(
            'jaka jest najbardziej unikatowa w skali świata aparatura stosowana w agh',
            'najbardziej unikatowa w skali światowej aparatura stosowana w agh to: jeden z kilku najpotężniejszych na świecie – analityczny transmisyjny mikroskop elektronowy (s)tem fei titancubed g-2 60-300, a także rentgenowski fluorescencyjny mikroskop konfokalny'
        )

    def test_65_8(self):
        self.check_phrase_response(
            'czym jest kopalnia doświadczalna',
            'w agh znajduje się kopalnia doświadczalna – unikatowe laboratorium badawczo-dydaktyczne'
        )

    def test_65_9(self):
        self.check_phrase_response(
            'czym jest komora bezechowa',
            'w agh znajduje się komora bezechowa, będąca jednym z najcichszych miejsc w polsce'
        )

    def test_65_10(self):
        self.check_phrase_response(
            'gdzie znajduje się wykaz aparatury naukowo-badawczej',
            'wykaz aparatury znajduje się w sieciowym katalogu aparatury naukowo-badawczej i stanowisk badawczych; zawiera on podstawowe informacje o sprzęcie, którym dysponują poszczególne jednostki uczelni'
        )

    def test_65_11(self):
        self.check_phrase_response(
            'co zawiera wykaz aparatury naukowo-badawczej i stanowisk badawczych',
            'wykaz aparatury znajduje się w sieciowym katalogu aparatury naukowo-badawczej i stanowisk badawczych; zawiera on podstawowe informacje o sprzęcie, którym dysponują poszczególne jednostki uczelni'
        )

    # 66
    def test_66_1(self):
        self.check_phrase_response(
            'w czym znajduje odzwierciedlenie aktywność naukowa pracowników agh',
            'aktywność naukowa pracowników agh znajduje odzwierciedlenie między innymi w publikowanych rocznie ponad 1600 artykułach w czasopismach naukowych krajowych i zagranicznych oraz około 2000 referatów na konferencjach, z tego około 600 publikowanych w czasopismach o zasięgu międzynarodowym'
        )

    def test_66_2(self):
        self.check_phrase_response(
            'ile rocznie jest publikowanych artykułów w czasopismach naukowych',
            'aktywność naukowa pracowników agh znajduje odzwierciedlenie między innymi w publikowanych rocznie ponad 1600 artykułach w czasopismach naukowych krajowych i zagranicznych oraz około 2000 referatów na konferencjach, z tego około 600 publikowanych w czasopismach o zasięgu międzynarodowym'
        )

    def test_66_3(self):
        self.check_phrase_response(
            'ile rocznie jest publikowanych artykółów w czasopismach o zasięgu międzynarodowym',
            'aktywność naukowa pracowników agh znajduje odzwierciedlenie między innymi w publikowanych rocznie ponad 1600 artykułach w czasopismach naukowych krajowych i zagranicznych oraz około 2000 referatów na konferencjach, z tego około 600 publikowanych w czasopismach o zasięgu międzynarodowym'
        )

    # 67
    def test_67_1(self):
        self.check_phrase_response(
            'w czym wyraża się potencjał innowacyjny agh',
            'potencjał innowacyjny agh wyraża się w wymiarze własności intelektualnej, która obejmuje patenty, znaki towarowe, wzory użytkowe oraz projekty wynalazcze'
        )

    def test_67_2(self):
        self.check_phrase_response(
            'co zrobiono by ułatwić transfer innowacyjnych technologii do przedsiębiorstw',
            'w celu stworzenia mechanizmów ułatwiających i intensyfikujących transfer innowacyjnych technologii i wiedzy z agh do przedsiębiorców i innych instytucji zewnętrznych powołano centrum transferu technologii agh'
        )

    # 68
    def test_68_1(self):
        self.check_phrase_response(
            'jakie możliwości stwarzają studenckie koła naukowe',
            'studenckie koła naukowe stwarzają możliwość poszerzania wiedzy i umiejętności pod kierunkiem najlepszych naukowców'
        )

    def test_68_2(self):
        self.check_phrase_response(
            'ile kół naukowych działa w agh',
            'obecnie w agh działa łącznie blisko 120 studenckich kół naukowych'
        )

    def test_68_3(self):
        self.check_phrase_response(
            'jakie są najczęściej stosowane formy działalności kół naukowych',
            'do najczęściej stosowanych form działalności kół naukowych można zaliczyć: cykliczne spotkania szkoleniowe; uczestnictwo w badaniach teoretycznych i doświadczalnych prowadzonych przez katedry i zakłady; organizację konferencji, seminariów i obozów naukowych; udział w konferencjach krajowych i międzynarodowych, w studenckiej wymianie międzynarodowej; wyjazdy badawczo-szkoleniowe, naukowo-turystyczne i rekreacyjne'
        )

    # 69
    def test_69_1(self):
        self.check_phrase_response(
            'ile projektów realizuje uczelnia wspólnie z partnerami zagranicznymi',
            'uczelnia realizuje ponad 100 projektów prowadzonych wspólnie z partnerami zagranicznymi między innymi w ramach następujących programów: programy ramowe ue w tym horyzont 2020, kic innoenergy, kic rawmaterials, europejska agencja kosmiczna, fundusz wyszehradzki, fundusz węgla i stali, eureka, cost, era, programy współpracy bilateralnej, erasmus+, europejski fundusz społeczny po wer'
        )

    def test_69_2(self):
        self.check_phrase_response(
            'w ramach jakich programów uczelnia realizuje projekty z partnerami zagranicznymi',
            'uczelnia realizuje ponad 100 projektów prowadzonych wspólnie z partnerami zagranicznymi między innymi w ramach następujących programów: programy ramowe ue w tym horyzont 2020, kic innoenergy, kic rawmaterials, europejska agencja kosmiczna, fundusz wyszehradzki, fundusz węgla i stali, eureka, cost, era, programy współpracy bilateralnej, erasmus+, europejski fundusz społeczny po wer'
        )

    def test_69_3(self):
        self.check_phrase_response(
            'ile umów z zagranicznymi uniwersytetami posiada akademia',
            'akademia posiada ponad 250 umów generalnych z zagranicznymi uniwersytetami, politechnikami i instytutami badawczymi w europie, ameryce północnej i południowej oraz azji, dotyczących wielokierunkowych działań w zakresie kształcenia i badań naukowych, a także ponad 450 umów z uczelniami w ramach programu erasmus+'
        )

    def test_69_4(self):
        self.check_phrase_response(
            'ile umów posiada uczelnia w ramach programu erasmus+',
            'akademia posiada ponad 250 umów generalnych z zagranicznymi uniwersytetami, politechnikami i instytutami badawczymi w europie, ameryce północnej i południowej oraz azji, dotyczących wielokierunkowych działań w zakresie kształcenia i badań naukowych, a także ponad 450 umów z uczelniami w ramach programu erasmus+'
        )

    def test_69_5(self):
        self.check_phrase_response(
            'ile umów o podwójnym dyplomowaniu posiada agh ',
            'agh jest stroną 26 umów o podwójnym dyplomowaniu z prestiżowymi uczelniami niemiec, francji, japonii, ukrainy oraz finlandii, w ramach których studenci zdobywają wiedzę na dwóch uczelniach wyższych równolegle'
        )

    def test_69_6(self):
        self.check_phrase_response(
            'czy agh posiada umowy z zakładami przemysłowymi',
            'akademia posiada umowy z zakładami przemysłowymi, w tym dużymi międzynarodowymi korporacjami, przedmiotem umów jest współpraca naukowa, badawcza i edukacyjna, a celem wszechstronne wykorzystanie wzajemnych możliwości partnerów'
        )

    def test_69_7(self):
        self.check_phrase_response(
            'co jest przedmiotem umów akademii z zakładami przemysłowymi',
            'akademia posiada umowy z zakładami przemysłowymi, w tym dużymi międzynarodowymi korporacjami, przedmiotem umów jest współpraca naukowa, badawcza i edukacyjna, a celem wszechstronne wykorzystanie wzajemnych możliwości partnerów'
        )

    # 70
    def test_70_1(self):
        self.check_phrase_response(
            'czy agh dysponuje ofertą współpracy z partnerami zewnętrznymi',
            'agh dysponuje szeroką ofertą obszarów współpracy z partnerami zewnętrznymi'
        )

    def test_70_2(self):
        self.check_phrase_response(
            'czy uczelnia jest silnie związana z przemysłem',
            'Uczelnia od momentu powstania jest silnie związana z przemysłem, co skutkuje uczestnictwem przedstawicieli firm w życiu Akademii'
        )

    def test_70_3(self):
        self.check_phrase_response(
            'w jakim celu powołano radę społeczną i konwent agh',
            'W celu uczestnictwa przedstawicieli firm w życiu akademii powołano Radę Społeczną AGH oraz Konwent AGH'
        )

    def test_70_4(self):
        self.check_phrase_response(
            'co jest zadaniem konwentu i rady społecznej agh',
            'Zadaniem konwentu oraz rady społecznej agh jest między innymi kształtowanie modelu kształcenia pod kątem przyszłego pracodawcy oraz opiniowanie kierunków działalności naukowo-badawczej AGH'
        )

    def test_70_5(self):
        self.check_phrase_response(
            'czym zajmuje się dział współpracy z administracją i gospodarką',
            'Dział Współpracy z Administracją i Gospodarką jest jednostką prowadzącą działania wspierające współpracę społeczności uczelnianej z przedsiębiorcami, instytucjami otoczenia  biznesu, jednostkami administracji państwowej i samorządowej, uczelniami oraz instytucjami badawczo-rozwojowymi'
        )

    def test_70_6(self):
        self.check_phrase_response(
            'przez jaką jednostkę koordynowana jest współpraca z instytucjami naukowymi i edukacyjnymi za granicą',
            'Współpraca z instytucjami naukowymi i edukacyjnymi za granicą koordynowana jest przez Dział Współpracy z Zagranicą'
        )

    def test_70_7(self):
        self.check_phrase_response(
            'czym zajmuje się dział współpracy z zagranicą',
            'Współpraca z instytucjami naukowymi i edukacyjnymi za granicą koordynowana jest przez Dział Współpracy z Zagranicą'
        )

    # 71
    def test_71_1(self):
        self.check_phrase_response(
            'jaki dział zajmuje się funduszami strukturalnymi w agh',
            'Funduszami strukturalnymi w AGH zajmuje się Dział Obsługi Funduszy Strukturalnych COP AGH - w obszarze Europejskiego Funduszu Rozwoju Regionalnego (EFRR) oraz w obszarze Europejskiego Funduszu Społecznego (EFS)'
        )

    def test_71_2(self):
        self.check_phrase_response(
            'czym zajmuje się dział obsługi funduszy strukturalnych',
            'Funduszami strukturalnymi w AGH zajmuje się Dział Obsługi Funduszy Strukturalnych COP AGH - w obszarze Europejskiego Funduszu Rozwoju Regionalnego (EFRR) oraz w obszarze Europejskiego Funduszu Społecznego (EFS)'
        )

    def test_71_3(self):
        self.check_phrase_response(
            'czym zajmuje się centrum obsługi projektów agh',
            'centrum obsługi projektów agh zajmuje się między innymi obsługą projektów naukowych, badawczych i edukacyjnych finansowanych ze źródeł zewnętrznych: krajowych, unijnych oraz międzynarodowych'
        )

    def test_71_4(self):
        self.check_phrase_response(
            'jaka jednostka w agh zajmuje się obsługą projektów naukowych badawczych i edukacyjnych finansowanych ze źródeł zewnętrznych',
            'centrum obsługi projektów agh zajmuje się między innymi obsługą projektów naukowych, badawczych i edukacyjnych finansowanych ze źródeł zewnętrznych: krajowych, unijnych oraz międzynarodowych'
        )

    # 72
    def test_72_1(self):
        self.check_phrase_response(
            'co należy do zadań działu obsługi programów międzynarodowych',
            'do zadań działu obsługi programów międzynarodowych (dopm) należy między innymi pozyskiwanie i rozpowszechnianie informacji na temat możliwości i procedur finansowania projektów z udziałem partnerów zagranicznych z programów międzynarodowych, obsługa formalno-prawna aplikowania i realizacji projektów międzynarodowych, prowadzenie doradztwa i konsultacji dla pracowników agh, tworzenie i bieżąca aktualizacja baz danych w zakresie pozyskiwania środków pozabudżetowych'
        )

    def test_72_2(self):
        self.check_phrase_response(
            'czym jest dział obsługi programów międzynarodowych',
            'do zadań działu obsługi programów międzynarodowych (dopm) należy między innymi pozyskiwanie i rozpowszechnianie informacji na temat możliwości i procedur finansowania projektów z udziałem partnerów zagranicznych z programów międzynarodowych, obsługa formalno-prawna aplikowania i realizacji projektów międzynarodowych, prowadzenie doradztwa i konsultacji dla pracowników agh, tworzenie i bieżąca aktualizacja baz danych w zakresie pozyskiwania środków pozabudżetowych'
        )

    def test_72_3(self):
        self.check_phrase_response(
            'jakie są możliwości uzyskania środków finansowych potrzebnych na realizację projektów',
            'programy ramowe, kic, inicjatywy wspólnotowe to niektóre z możliwości uzyskania środków finansowych potrzebnych na realizację projektów'
        )

    # 73
    def test_73_1(self):
        self.check_phrase_response(
            'kiedy powołano centrum transferu technologii agh',
            'w celu stworzenia mechanizmów ułatwiających i intensyfikujących transfer innowacyjnych technologii z agh do przedsiębiorców i innych instytucji zewnętrznych, w 2007 roku powołano centrum transferu technologii akademii górniczo-hutniczej w krakowie (ctt agh)'
        )

    def test_73_2(self):
        self.check_phrase_response(
            'w jakim celu powołano centrum transferu technologii agh',
            'w celu stworzenia mechanizmów ułatwiających i intensyfikujących transfer innowacyjnych technologii z agh do przedsiębiorców i innych instytucji zewnętrznych, w 2007 roku powołano centrum transferu technologii akademii górniczo-hutniczej w krakowie (ctt agh)'
        )

    def test_73_3(self):
        self.check_phrase_response(
            'co jest zadaniem centrum transferu technologii agh',
            'Zadaniem centrum transferu technologii CTT AGH jest wsparcie procesów komercjalizacji i transferu innowacyjnych technologii i wiedzy'
        )

    def test_73_4(self):
        self.check_phrase_response(
            'w jakich obszarach działa centrum transferu technologii agh',
            'Centrum Transferu Technologii AGH działa w obszarach marketingu nauki w środowisku przedsiębiorców, ochrony własności intelektualnej oraz obsługi i finansowania transferu technologii'
        )

    def test_73_5(self):
        self.check_phrase_response(
            'co jest zadaniem spółki krakowskie centrum innowacyjnych technologii innoagh',
            'głównym, choć nie jedynym zadaniem spółki krakowskie centrum innowacyjnych technologii innoagh jest obejmowanie w miejsce uczelni udziałów w nowych firmach, powstających na bazie wyników prac badawczych oraz ogólnej wiedzy pochodzącej z jednostek naukowo-badawczych, w tak zwany spółkach spin-off'
        )

    def test_73_6(self):
        self.check_phrase_response(
            'jaki jest cel spółki krakowskie centrum innowacyjnych technologii innoagh',
            'celem spółki krakowskie centrum innowacyjnych technologii innoagh jest doradztwo i wsparcie dla pracowników naukowych zainteresowanych zakładaniem innowacyjnych przedsiębiorstw tworzonych w oparciu o własność intelektualną powstającą na uczelni'
        )

    def test_73_7(self):
        self.check_phrase_response(
            'czym jest spółka krakowskie centrum innowacyjnych technologii innoagh',
            'celem spółki krakowskie centrum innowacyjnych technologii innoagh jest doradztwo i wsparcie dla pracowników naukowych zainteresowanych zakładaniem innowacyjnych przedsiębiorstw tworzonych w oparciu o własność intelektualną powstającą na uczelni'
        )

    # 74
    def test_74_1(self):
        self.check_phrase_response(
            'czy agh jest członkiem acru',
            'AGH jest członkiem ACRU (Association of the Carpathian Region Universities)'
        )

    def test_74_2(self):
        self.check_phrase_response(
            'czy agh jest członkiem Association of the Carpathian Region Universities',
            'AGH jest członkiem ACRU (Association of the Carpathian Region Universities)'
        )

    def test_74_3(self):
        self.check_phrase_response(
            'czy agh jest członkiem eua',
            'AGH jest członkiem EUA (European University Association)'
        )

    def test_74_4(self):
        self.check_phrase_response(
            'czy agh jest członkiem European University Association',
            'AGH jest członkiem EUA (European University Association)'
        )

    def test_74_5(self):
        self.check_phrase_response(
            'czy agh jest członkiem iau',
            'AGH jest członkiem IAU (International Association of Universities)'
        )

    def test_74_6(self):
        self.check_phrase_response(
            'czy agh jest członkiem International Association of Universities',
            'AGH jest członkiem IAU (International Association of Universities)'
        )

    def test_74_7(self):
        self.check_phrase_response(
            'czy agh jest członkiem sefi',
            'AGH jest członkiem SEFI ( Société Européenne pour la Formation des Ingénieurs)'
        )

    def test_74_8(self):
        self.check_phrase_response(
            'czy agh jest członkiem Société Européenne pour la Formation des Ingénieurs',
            'AGH jest członkiem SEFI ( Société Européenne pour la Formation des Ingénieurs)'
        )

    def test_74_9(self):
        self.check_phrase_response(
            'czy agh jest członkiem aeua',
            'AGH jest członkiem AEUA (Arab and European Universities Association)'
        )

    def test_74_10(self):
        self.check_phrase_response(
            'czy agh jest członkiem Arab and European Universities Association',
            'AGH jest członkiem AEUA (Arab and European Universities Association)'
        )

    def test_74_11(self):
        self.check_phrase_response(
            'czy agh jest członkiem KMM-VIN AISBL',
            'AGH jest członkiem KMM-VIN AISBL (European Virtual Institute on Knowledge-based Multifunctional Material AISBL)'
        )

    def test_74_12(self):
        self.check_phrase_response(
            'czy agh jest członkiem European Virtual Institute on Knowledge-based Multifunctional Material AISBL',
            'AGH jest członkiem KMM-VIN AISBL (European Virtual Institute on Knowledge-based Multifunctional Material AISBL)'
        )

    def test_74_13(self):
        self.check_phrase_response(
            'czy agh jest członkiem C-MAC NSU NPO',
            'AGH jest członkiem C-MAC NSU NPO (European Intigrated Centre for the Development of New Metallic Alloys and Compounds)'
        )

    def test_74_14(self):
        self.check_phrase_response(
            'czy agh jest członkiem European Intigrated Centre for the Development of New Metallic Alloys and Compounds',
            'AGH jest członkiem C-MAC NSU NPO (European Intigrated Centre for the Development of New Metallic Alloys and Compounds)'
        )

    def test_74_15(self):
        self.check_phrase_response(
            'czy agh jest członkiem TIME',
            'AGH jest członkiem TIME (Top Industrial Managers for Europe)'
        )

    def test_74_16(self):
        self.check_phrase_response(
            'czy agh jest członkiem Top Industrial Managers for Europe',
            'AGH jest członkiem TIME (Top Industrial Managers for Europe)'
        )

    def test_74_17(self):
        self.check_phrase_response(
            'czy agh jest członkiem Magalhaes Network',
            'AGH jest członkiem Magalhaes Network'
        )

    def test_74_18(self):
        self.check_phrase_response(
            'czy agh jest członkiem KIC InnoEnergy',
            'AGH jest członkiem KIC InnoEnergy (Knowledge Innovation Community)'
        )

    def test_74_19(self):
        self.check_phrase_response(
            'czy agh jest członkiem Knowledge Innovation Community InnoEnergy',
            'AGH jest członkiem KIC InnoEnergy (Knowledge Innovation Community)'
        )

    def test_74_20(self):
        self.check_phrase_response(
            'czy agh jest członkiem CEEPUS',
            'AGH jest członkiem CEEPUS (Central European Exchange Program for University Studies)'
        )

    def test_74_21(self):
        self.check_phrase_response(
            'czy agh jest członkiem Central European Exchange Program for University Studies',
            'AGH jest członkiem CEEPUS (Central European Exchange Program for University Studies)'
        )

    def test_74_22(self):
        self.check_phrase_response(
            'czy agh jest członkiem IROs Forum',
            'AGH jest członkiem IROs Forum (International Relations Offices Forum)'
        )

    def test_74_23(self):
        self.check_phrase_response(
            'czy agh jest członkiem International Relations Offices Forum',
            'AGH jest członkiem IROs Forum (International Relations Offices Forum)'
        )

    def test_74_24(self):
        self.check_phrase_response(
            'czy agh jest członkiem NAFSA',
            'AGH jest członkiem NAFSA (Association of International Educators)'
        )

    def test_74_25(self):
        self.check_phrase_response(
            'czy agh jest członkiem Association of International Educators',
            'AGH jest członkiem NAFSA (Association of International Educators)'
        )

    # 75
    def test_75_1(self):
        self.check_phrase_response(
            'jakiemu standardowi odpowiada system punktowy stosowany w uczelni',
            'system punktowy stosowany w uczelni odpowiada standardowi ects (european credit transfer system)'
        )

    def test_75_2(self):
        self.check_phrase_response(
            'czy uczelnia stosuje standard ects',
            'system punktowy stosowany w uczelni odpowiada standardowi ects (european credit transfer system)'
        )

    def test_75_3(self):
        self.check_phrase_response(
            'czy uczelnia stosuje standard european credit transfer system',
            'system punktowy stosowany w uczelni odpowiada standardowi ects (european credit transfer system)'
        )

    # 76
    def test_76_1(self):
        self.check_phrase_response(
            'kto został wybrany na stanowisko rzecznika praw studenta agh',
            'na stanowisko rzecznika praw studenta została powołana doktor habilitowany inżynier manuela reben, profesor agh'
        )

    def test_76_2(self):
        self.check_phrase_response(
            'kto tworzy zespół rzecznika praw studenta',
            'zespół rzecznika praw studenta tworzą: doktor habilitowany inżynier Manuela Reben, profesor AGH – pracownik Wydziału Inżynierii Materiałowej i Ceramiki, Kierownik Katedry Technologii Szkła i Powłok Amorficznych; Marzena Stupkiewicz (asystentka rzecznika) – studentka czwartego roku z Wydziału Inżynierii Metali i Informatyki Przemysłowej; Mikołaj Gralczyk (asystent rzecznika) – student drugiego roku drugiego stopnia studiów na Wydziale Fizyki i Informatyki Stosowanej'
        )

    def test_76_3(self):
        self.check_phrase_response(
            'przez kogo został powołany rzecznik praw studenta',
            'rzecznik praw studenta został powołany przez rektora agh, a jego głównym zadaniem jest pomoc studentom w egzekwowaniu ich praw, w tym między innymi w sprawach dotyczących regulaminu studiów bądź stypendiów'
        )

    def test_76_4(self):
        self.check_phrase_response(
            'jakie jest główne zadanie rzecznika praw studenta',
            'rzecznik praw studenta został powołany przez rektora agh, a jego głównym zadaniem jest pomoc studentom w egzekwowaniu ich praw, w tym między innymi w sprawach dotyczących regulaminu studiów bądź stypendiów'
        )

    # 77
    def test_77_1(self):
        self.check_phrase_response(
            'kiedy potrwa semestr zimowy w obecnym roku akademickim',
            'Semestr zimowy obecnego roku akademickiego potrwa od 1 października do 16 lutego'
        )

    def test_77_2(self):
        self.check_phrase_response(
            'kiedy potrwają zajęcia semestru zimowego w obecnym roku akademickim',
            'zajęcia semestru zimowego obecnego roku akademickiego potrwają od 1 października do 28 stycznia'
        )

    def test_77_3(self):
        self.check_phrase_response(
            'kiedy potrwają wakacje zimowe w obecnym roku akademickim',
            'wakacje zimowe (ferie świąteczne) w obecnym roku akademickim potrwają od 23 grudnia do 2 stycznia'
        )

    def test_77_4(self):
        self.check_phrase_response(
            'kiedy potrwają ferie świąteczne zimowe w obecnym roku akademickim',
            'wakacje zimowe (ferie świąteczne) w obecnym roku akademickim potrwają od 23 grudnia do 2 stycznia'
        )

    def test_77_5(self):
        self.check_phrase_response(
            'kiedy potrwa zimowa sesja egzaminacyjna część podstawowa w obecnym roku akademickim',
            'zimowa sesja egzaminacyjna – część podstawowa w obecnym roku akademickim potrwa od 29 stycznia do 9 lutego'
        )

    def test_77_6(self):
        self.check_phrase_response(
            'kiedy potrwa zimowa sesja egzaminacyjna część poprawkowa w obecnym roku akademickim',
            'zimowa sesja egzaminacyjna – część poprawkowa w obecnym roku akademickim potrwa od 10 lutego do 16 lutego'
        )

    def test_77_7(self):
        self.check_phrase_response(
            'kiedy będzie przerwa międzysemestralna w obecnym roku akademickim',
            'przerwa międzysemestralna w obecnym roku akademickim potrwa od 17 lutego do 23 lutego'
        )

    def test_77_8(self):
        self.check_phrase_response(
            'kiedy potrwa semestr letni w obecnym roku akademickim',
            'semestr letni w obecnym roku akademickim potrwa od 24 lutego do 30 września'
        )

    def test_77_9(self):
        self.check_phrase_response(
            'kiedy potrwają zajęcia semestru letniego w obecnym roku akademickim',
            'zajęcia semestru letniego w obecnym roku akademickim potrwają od 24 lutego do 14 czerwca'
        )

    def test_77_10(self):
        self.check_phrase_response(
            'kiedy będą wakacje wiosenne w obecnym roku akademickim',
            'wakacje wiosenne (ferie świąteczne) w obecnym roku akademickim potrwają od 9 kwietnia do 14 kwietnia'
        )

    def test_77_11(self):
        self.check_phrase_response(
            'kiedy będą ferie świąteczne wiosenne w obecnym roku akademickim',
            'wakacje wiosenne (ferie świąteczne) w obecnym roku akademickim potrwają od 9 kwietnia do 14 kwietnia'
        )

    def test_77_12(self):
        self.check_phrase_response(
            'kiedy będzie letnia sesja egzaminacyjna część podstawowa w obecnym roku akademickim',
            'letnia sesja egzaminacyjna – część podstawowa w obecnym roku akademickim potrwa od 15 czerwca do 30 czerwca'
        )

    def test_77_13(self):
        self.check_phrase_response(
            'kiedy będą wakacje letnie w obecnym roku akademickim',
            'wakacje letnie w obecnym roku akademickim potrwają od 1 lipca do 31 sierpnia'
        )

    def test_77_14(self):
        self.check_phrase_response(
            'kiedy będzie letnia sesja egzaminacyjna część poprawkowa w obecnym roku akademickim',
            'letnia sesja egzaminacyjna – część poprawkowa w obecnym roku akademickim potrwa od 1 września do 15 września'
        )

    def test_77_15(self):
        self.check_phrase_response(
            'w jakich terminach odbędą się zajęcia według planu dla innego dnia w obecnym roku akademickim',
            'zajęcia odbywające się według planu innego dnia w obecnym roku akademickim w następujących terminach: 7 stycznia 2020 roku (wtorek) zajęcia odbywają się według harmonogramu zajęć ustalonych dla poniedziałku, 10 czerwca 2020 roku (środa) zajęcia odbywają się według harmonogramu zajęć ustalonego dla piątku'
        )

    def test_77_16(self):
        self.check_phrase_response(
            'jakie są dni ustawowo wolne od zajęć dydaktycznych',
            'Dni ustawowo wolne od zajęć dydaktycznych: 1 listopada, 11 listopada, 1 stycznia, 6 stycznia, 1 maja, 3 maja, 11 czerwca'
        )

    def test_77_17(self):
        self.check_phrase_response(
            'jakie będą dni dodatkowo wolne od zajęć dydaktycznych w obecnym roku akademickim',
            'Dni dodatkowo wolne od zajęć dydaktycznych w obecnym roku akademickim to: 18 października, 31 października, 12 czerwca'
        )

    def test_77_18(self):
        self.check_phrase_response(
            'kiedy przeprowadzane będą czynności związane z zakończeniem roku akademickiego 2019/2020',
            'Okres od 16 do 30 września 2020 roku przeznaczony jest na przeprowadzenie czynności związanych z zakończeniem roku akademickiego 2019/2020 i rozpoczęciem roku akademickiego 2020/2021'
        )

    def test_77_19(self):
        self.check_phrase_response(
            'kiedy przeprowadzane będą czynności związane z rozpoczęciem roku akademickiego 2020/2021',
            'Okres od 16 do 30 września 2020 roku przeznaczony jest na przeprowadzenie czynności związanych z zakończeniem roku akademickiego 2019/2020 i rozpoczęciem roku akademickiego 2020/2021'
        )

    # 78
    def test_78_1(self):
        self.check_phrase_response(
            'co obejmuje system pomocy materialnej dla studentów agh',
            'system pomocy materialnej dla studentów w akademii górniczo-hutniczej obejmuje wiele form stypendiów oraz zapomóg, w tym także dofinansowanie do wyżywienia w stołówkach agh'
        )

    def test_78_2(self):
        self.check_phrase_response(
            'gdzie dostępna jest informacja na temat stypendiów',
            'informacja na temat stypendiów, zapomóg dostępna jest w dziekanatach oraz w Dziale Spraw Studenckich'
        )

    # 79
    def test_79_1(self):
        self.check_phrase_response(
            'czym jest program AGH uczelnią przyjazną wobec osób niepełnosprawnych',
            'Nasza Uczelnia od 2000 roku realizuje program „AGH uczelnią przyjazną wobec osób niepełnosprawnych”, którego celem jest kompleksowe rozwiązywanie problemów, z którymi zmagają się studenci z różnymi niepełnosprawnościami'
        )

    def test_79_2(self):
        self.check_phrase_response(
            'jaki jest cel programu AGH uczelnią przyjazną wobec osób niepełnosprawnych',
            'Nasza Uczelnia od 2000 roku realizuje program „AGH uczelnią przyjazną wobec osób niepełnosprawnych”, którego celem jest kompleksowe rozwiązywanie problemów, z którymi zmagają się studenci z różnymi niepełnosprawnościami'
        )

    def test_79_3(self):
        self.check_phrase_response(
            'kto koordynnuje działania na rzecz osób niepełnosprawnych',
            'Działania AGH na rzecz osób niepełnosprawnych koordynuje Biuro do spraw Osób Niepełnosprawnych, które również wspiera inicjatywy Zrzeszenia Studentów Niepełnosprawnych - pierwszej tego typu organizacji w Polsce'
        )

    def test_79_4(self):
        self.check_phrase_response(
            'ilu studentów z niepełnosprawnościami studiuje na agh',
            'W naszej społeczności akademickiej studiuje znacząca liczba (około 500) studentów o różnym stopniu i rodzaju niepełnosprawności'
        )

    def test_79_5(self):
        self.check_phrase_response(
            'jak rozwija się oferta wsparcia studentów i doktorantów z niepełnosprawnościami',
            'Z roku na rok oferta wsparcia studentów i doktorantów z niepełnosprawnościami ulega rozszerzeniu, a działania uczelni stają się coraz bardziej profesjonalne'
        )

    # 80
    def test_80_1(self):
        self.check_phrase_response(
            'w jakich obszarach działa program adapter',
            'Program ADAPTER powstał w odpowiedzi na oczekiwania studentów z zakresu potrzeb w obszarach: zdrowotnym, społecznym, psychologicznym'
        )

    def test_80_2(self):
        self.check_phrase_response(
            'co jest celem programu adapter',
            'Celem Programu adapter jest promocja zdrowych i aktywnych postaw w środowisku akademickim, a także udzielanie wsparcia psychologicznego osobom doświadczającym trudności w adaptacji do warunków życia studenckiego'
        )

    def test_80_3(self):
        self.check_phrase_response(
            'jakie warsztaty prowadzone sa w ramach programu adapter',
            'W ramach Programu adapter prowadzone są warsztaty rozwijające umiejętności psychologiczne i interpersonalne oraz Punkt Konsultacyjny z dyżurem psychologa'
        )

    def test_80_4(self):
        self.check_phrase_response(
            'czy program adapter zapewnia dyżur psychologa',
            'W ramach Programu adapter prowadzone są warsztaty rozwijające umiejętności psychologiczne i interpersonalne oraz Punkt Konsultacyjny z dyżurem psychologa'
        )

    # 81
    def test_81_1(self):
        self.check_phrase_response(
            'czym są juwenalia',
            'Juwenalia to najważniejsze wydarzenie roku akademickiego, kiedy uczelnią i miastem rządzą studenci: Barwny pochód na Rynek Główny, koncerty, kabaretony, imprezy sportowe to tylko część juwenaliowych atrakcji'
        )

    def test_81_2(self):
        self.check_phrase_response(
            'jakie są juwenaliowe atrakcje',
            'Juwenalia to najważniejsze wydarzenie roku akademickiego, kiedy uczelnią i miastem rządzą studenci: Barwny pochód na Rynek Główny, koncerty, kabaretony, imprezy sportowe to tylko część juwenaliowych atrakcji'
        )

    def test_81_3(self):
        self.check_phrase_response(
            'czym są beanalia',
            'Beanalia są to otrzęsiny studentów I roku; podczas tej imprezy nowo przyjęci studenci wstępują w pełni w szeregi braci studenckiej'
        )

    def test_81_4(self):
        self.check_phrase_response(
            'czym jest babski comber',
            'Babski comber to stara krakowska tradycja Akademii Górniczo-Hutniczej, wiąże się ona z Barbórką, czyli świętem stanu górniczego; Podczas niego kobiety biesiadują na Babskim combrze, natomiast mężczyźni świętują w ramach Karczmy piwnej'
        )

    def test_81_5(self):
        self.check_phrase_response(
            'jakie są tradycje związane z barbórką',
            'Babski comber to stara krakowska tradycja Akademii Górniczo-Hutniczej, wiąże się ona z Barbórką, czyli świętem stanu górniczego; Podczas niego kobiety biesiadują na Babskim combrze, natomiast mężczyźni świętują w ramach Karczmy piwnej'
        )

    def test_81_6(self):
        self.check_phrase_response(
            'jakie są przykładowe bale organizowane przez wydziały',
            'Ważnym elementem tradycji są bale organizowane cyklicznie przez Wydziały, na przykład Bal Ceramika, Elektryka, Mechanika'
        )

    # 82
    def test_82_1(self):
        self.check_phrase_response(
            'gdzie można zadbać o swoją kondycję',
            'O swoją kondycję zadbać można, korzystając z następujących obiektów: basen, nowoczesne siłownie, łaźnia parowa, boisko piłkarskie, nowoczesna hala ze sztuczną nawierzchnią i wiele innych'
        )

    def test_82_2(self):
        self.check_phrase_response(
            'ile sekcji sportowych ma azs agh',
            'Uczelniany Klub AZS AGH to największy w środowisku akademickim Krakowa i jeden z największych w Polsce klub sportowy mający aż 20 sekcji sportowych'
        )

    def test_82_3(self):
        self.check_phrase_response(
            'czym jest klub azs agh',
            'Uczelniany Klub AZS AGH to największy w środowisku akademickim Krakowa i jeden z największych w Polsce klub sportowy mający aż 20 sekcji sportowych'
        )

    def test_82_4(self):
        self.check_phrase_response(
            'jakie wydarzenia organizuje azs agh',
            'Klub AZS AGH wspólnie ze Studium Wychowania Fizycznego i Sportu (SWFiS) organizuje między innymi szkoleniowe obozy narciarskie, żeglarskie, kajakowe, turystykę górską, Dzień Sportu AGH, Mistrzostwa AGH w narciarstwie alpejskim i snowboardzie, w tenisie stołowym, kolarstwie górskim i w pływaniu, a także turnieje z okazji Dnia Górnika i Dnia Hutnika'
        )

    def test_82_5(self):
        self.check_phrase_response(
            'jakie lokaty zajmują sportowcy azs agh',
            'Najlepsi sportowcy Klubu AZS AGH biorą udział w rozgrywkach Małopolskiej Ligi Akademickiej, Akademickich Mistrzostwach Polski, Biegu Kościuszkowskim i innych zawodach, zajmując czołowe lokaty tak w środowisku krakowskim, jak i na arenie ogólnopolskiej'
        )

    # 83
    def test_83_1(self):
        self.check_phrase_response(
            'czym jest program legia akademicka',
            '„Legia Akademicka” to uruchomiony w 2017 roku przez MON pilotażowy program skierowany do studentów'
        )

    def test_83_2(self):
        self.check_phrase_response(
            'czym jest legia akademicka',
            '„Legia Akademicka” to uruchomiony w 2017 roku przez MON pilotażowy program skierowany do studentów'
        )

    # 84
    def test_84_1(self):
        self.check_phrase_response(
            'jakie są organizacje związane z kulturą studencką',
            'Kultura studencka agh to między innymi organizacje: Chór i Orkiestra Smyczkowa „Con Fuoco” AGH; orkiestra reprezentacyjna agh; studencki klub taneczny agh; Zespół Pieśni i Tańca AGH „KRAKUS”'
        )

    # 85
    def test_85_1(self):
        self.check_phrase_response(
            'czym jest con fuoco',
            '„Con Fuoco” to uczelniany Chór i Orkiestra Smyczkowa Akademii Górniczo-Hutniczej'
        )

    def test_85_2(self):
        self.check_phrase_response(
            'w którym roku został założony zespół con fuoco',
            'Zespół Con Fuoco został założony w 2009 roku'
        )

    def test_85_3(self):
        self.check_phrase_response(
            'ilu członków tworzy zepół con fuoco',
            'Zespół con fuoco tworzy ponad 50 studentów i absolwentów uczelni'
        )

    def test_85_4(self):
        self.check_phrase_response(
            'kto jest dyrygentem chóru con fuoco',
            'Dyrygentem chóru Con Fuoco jest Diana Mrugała-Gromek'
        )

    def test_85_5(self):
        self.check_phrase_response(
            'jakie utwory znajdują się w repertuarze chóru con fuoco',
            'W repertuarze chóru Con Fuoco znajduje się wiele utworów, od średniowiecznych psalmów, poprzez klasyczne utwory z renesansu i baroku, skończywszy na cztero- lub nawet ośmiogłosowych aranżacjach muzyki współczesnej'
        )

    def test_85_6(self):
        self.check_phrase_response(
            'jaki tytuł nosi płyta zespołu con fuoco',
            'Zwieńczeniem pracy twórczej zespołu Con Fuoco jest płyta pod tytułem „Z ogniem”, która została wydana w październiku 2012 roku'
        )

    def test_85_7(self):
        self.check_phrase_response(
            'kieyd została wydana płyta zespołu con fuoco',
            'Zwieńczeniem pracy twórczej zespołu Con Fuoco jest płyta pod tytułem „Z ogniem”, która została wydana w październiku 2012 roku'
        )

    # 86
    def test_86_1(self):
        self.check_phrase_response(
            'gdzie występuje orkiestra reprezentacyjna agh',
            'Orkiestra Reprezentacyjna AGH występuje zarówno w krakowskich klubach studenckich, jak i na międzynarodowych festiwalach, nawiązując zawsze rewelacyjny kontakt z publicznością'
        )

    def test_86_2(self):
        self.check_phrase_response(
            'jakie wydarzenia agh wiążą się z występami orkiestry reprezentacyjnej agh',
            'Występy muzyków Orkiestry Reprezentacyjnej AGH uświetniają wszystkie ważne wydarzenia w Akademii Górniczo-Hutniczej, takie jak: Barbórka, Dni Otwarte, Dzień Hutnika, Juwenalia czy wreszcie Dzień AGH'
        )

    def test_86_3(self):
        self.check_phrase_response(
            'jaką muzykę wykonuje orkiestra reprezentacyjna agh',
            'Artyści Orkiestry Reprezentacyjnej AGH wykonują głównie muzykę rozrywkową, filmową, jak również popularne marsze'
        )

    def test_86_4(self):
        self.check_phrase_response(
            'jaka jest dźwiękowa paleta barw orkiestry reprezentacyjnej agh',
            'Dźwiękowa paleta barw Orkiestry Reprezentacyjnej AGH składa się z takich instrumentów jak: flet, klarnet, saksofon, trąbka, puzon, waltornia, obój, fagot, tuba, instrumenty perkusyjne oraz gitara'
        )

    def test_86_5(self):
        self.check_phrase_response(
            'na jakich instrumentach gra orkiestra reprezentacyjna agh',
            'Dźwiękowa paleta barw Orkiestry Reprezentacyjnej AGH składa się z takich instrumentów jak: flet, klarnet, saksofon, trąbka, puzon, waltornia, obój, fagot, tuba, instrumenty perkusyjne oraz gitara'
        )

    # 87
    def test_87_1(self):
        self.check_phrase_response(
            'kiedy powstał studencki klub taneczny agh',
            'Studencki Klub Taneczny AGH powstał w 1955 roku i jest najstarszym klubem tego typu w Polsce'
        )

    def test_87_2(self):
        self.check_phrase_response(
            'kto sprawował opiekę nad działalnością studenckiego klubu tanecznego agh gdy był zakładany',
            'Opiekę nad działalnością studenckiego klubu tanecznego agh podczas jego założenia sprawował profesor Marian Wieczysty'
        )

    def test_87_3(self):
        self.check_phrase_response(
            'jak długo klub taneczny agh prowadzi kursy tańca',
            'Od blisko 60 lat klub taneczny agh prowadzi kursy tańca, a także szkoli tancerzy w sekcji turniejowej'
        )

    def test_87_4(self):
        self.check_phrase_response(
            'kto jest instruktorem studenckiego klubu tanecznego',
            'Uczestnicy zajęć studenckiego klubu tanecznego doskonalą swoje umiejętności pod okiem doświadczonych instruktorów – państwa Anny i Stanisława Smoroniów, którzy również są wychowankami studenckiego klubu tanecznego'
        )

    def test_87_5(self):
        self.check_phrase_response(
            'gdzie znajduje się siedziba studenckiego klubu tanecznego',
            'Siedziba studenckiego klubu tanecznego jest zlokalizowana przy ulicy Reymonta 15, gdzie znajduje się jedna z sal ćwiczeniowych'
        )

    # 88
    def test_88_1(self):
        self.check_phrase_response(
            'czym jest Zespół Pieśni i Tańca AGH',
            'Zespół Pieśni i Tańca AGH „Krakus” jest najstarszym studenckim zespołem folklorystycznym w Polsce'
        )

    def test_88_2(self):
        self.check_phrase_response(
            'kto założył Zespół Pieśni i Tańca AGH „Krakus”',
            'Zespół Pieśni i Tańca AGH „Krakus” został założony przez Wiesława Białowąsa przy Akademii Górniczo-Hutniczej w Krakowie w 1949 roku'
        )

    def test_88_3(self):
        self.check_phrase_response(
            'kiedy został założony Zespół Pieśni i Tańca AGH „Krakus”',
            'Zespół Pieśni i Tańca AGH „Krakus” został założony przez Wiesława Białowąsa przy Akademii Górniczo-Hutniczej w Krakowie w 1949 roku'
        )

    def test_88_4(self):
        self.check_phrase_response(
            'co prezentuje Zespół Pieśni i Tańca AGH „Krakus”',
            'Zespół Pieśni i Tańca AGH „Krakus” prezentuje oryginalny polski folklor ludowy, przetworzony i przystosowany artystycznie do wymogów sceny'
        )

    # 89
    def test_89_1(self):
        self.check_phrase_response(
            'kiedy prowadzona jest rekrutacja do szkoły doktorskiej agh',
            'Rekrutacja do Szkoły Doktorskiej AGH, prowadzona jest raz do roku w okresie poprzedzającym rozpoczęcie semestru zimowego'
        )

    def test_89_2(self):
        self.check_phrase_response(
            'kto ustala limit miejsc dostępnych w Szkole doktorskiej agh',
            'Limit miejsc dostępnych w Szkole doktorskiej agh i listę dyscyplin, na które prowadzona będzie kwalifikacja ustala Prorektor do spraw Nauki po konsultacji z jednostkami zgłaszającymi zagadnienia'
        )

    def test_89_3(self):
        self.check_phrase_response(
            'kto ustala listę dyscyplin dostępnych w Szkole doktorskiej agh',
            'Limit miejsc dostępnych w Szkole doktorskiej agh i listę dyscyplin, na które prowadzona będzie kwalifikacja ustala Prorektor do spraw Nauki po konsultacji z jednostkami zgłaszającymi zagadnienia'
        )

    def test_89_4(self):
        self.check_phrase_response(
            'kto określa kalendarz rekrutacji do szkoły doktorskiej agh',
            'Kalendarz rekrutacji do Szkoły doktorskiej agh określa Dyrektor Szkoły Doktorskiej'
        )

    # 90
    def test_90_1(self):
        self.check_phrase_response(
            'ile trwa kształcenie w szkole doktorskiej agh',
            'Kształcenie w Szkole Doktorskiej AGH trwa osiem semestrów, z możliwością wcześniejszego zakończenia pod warunkiem zrealizowania programu kształcenia i osiągnięcia wszystkich efektów uczenia się'
        )

    def test_90_2(self):
        self.check_phrase_response(
            'w jakim języku prowadzone jest kształcenie w szkole doktorskiej agh',
            'Kształcenie w Szkole Doktorskiej AGH prowadzone jest w języku polskim i angielskim'
        )

    def test_90_3(self):
        self.check_phrase_response(
            'w jaki sposób kończy się kształcenie doktoranta szkoły doktorskiej agh',
            'Kształcenie doktoranta szkoły doktorskiej agh kończy się złożeniem rozprawy doktorskiej'
        )

    # 91
    def test_91_1(self):
        self.check_phrase_response(
            'kto jest dyrektorem szkoły doktorskiej agh',
            'Dyrektorem szkoły doktorskiej agh jest profesor doktor habilitowany marcin szpyrka'
        )

    def test_91_2(self):
        self.check_phrase_response(
            'kto jest zastępcą dyrektora szkoły doktorskiej agh',
            'zastępcą dyrektora szkoły doktorskiej agh jest profesor doktor habilitowany inżynier marta radecka'
        )

    # 92
    def test_92_1(self):
        self.check_phrase_response(
            'jakie świadczenia mogą otrzymywać doktoranci',
            'doktoranci, którzy rozpoczęli studia doktoranckie przed rokiem akademickim 2019/2020 mogą otrzymywać świadczenia: stypendium socjalne, stypendium dla osób niepełnosprawnych, zapomogę stypendium rektora'
        )

    # 93
    def test_93_1(self):
        self.check_phrase_response(
            'jakie jest minimalne stypendium doktoranckie',
            'minimalne stypendium doktoranckie nie może wynosić mniej niż 60% minimalnego wynagrodzenia asystenta ustalonego w przepisach o wynagradzaniu nauczycieli akademickich, aktualnie jest to kwota 1470 złotych'
        )

    def test_93_2(self):
        self.check_phrase_response(
            'kto podejmuje decyzję o przyznaniu stypendium doktoranckiego',
            'decyzję o przyznaniu i wysokości stypendium doktoranckiego podejmuje rektor'
        )

    def test_93_3(self):
        self.check_phrase_response(
            'czy doktorant na pierwszym roku może otrzymać stypendium',
            'Stypendium doktoranckie na pierwszym roku może otrzymać doktorant, który otrzymał bardzo dobre wyniki w postępowaniu rekrutacyjnym'
        )

    # 94
    def test_94_1(self):
        self.check_phrase_response(
            'jacy doktoranci powinni zgłosić się do ubezpieczenia zdrowotnego',
            'Doktoranci niepracujący, którzy ukończyli 26 rok życia powinni zgłosić się do ubezpieczenia zdrowotnego'
        )

    # 95
    def test_95_1(self):
        self.check_phrase_response(
            'czym kończy się ukończenie przewodu doktorskiego',
            'Ukończenie przewodu doktorskiego i obrona pracy doktorskiej kończą się nadaniem przez Radę Wydziału stopnia doktora'
        )

    def test_95_2(self):
        self.check_phrase_response(
            'czym kończy się obrona pracy doktorskiej',
            'Ukończenie przewodu doktorskiego i obrona pracy doktorskiej kończą się nadaniem przez Radę Wydziału stopnia doktora'
        )

    def test_95_3(self):
        self.check_phrase_response(
            'ilu osobom rocznie nadawane są stopnie doktora',
            'Co roku ponad stu kilkudziesięciu osobom w AGH nadawane są stopnie doktora'
        )

    def test_95_4(self):
        self.check_phrase_response(
            'co otrzymują osoby którym nadano stopień doktora',
            'Osoby, którym nadano stopień doktora otrzymują dyplom doktora'
        )

    def test_95_5(self):
        self.check_phrase_response(
            'kiedy wręczane są doktorom dyplomy',
            'Dyplomy wypisywane  w Zespole Studiów Doktoranckich wręczane są doktorom na uroczystości promocji doktorskich'
        )

    def test_95_6(self):
        self.check_phrase_response(
            'kiedy odbyły się ostatnie promocje doktorskie',
            'Ostatnie promocje doktorskie w roku 2019 odbyły się 8 listopada'
        )

    # 96
    def test_96_1(self):
        self.check_phrase_response(
            'czym jest konkurs o nagrodę imienia profesora henryka czeczotta',
            'konkurs o nagrodę imienia profesora henryka czeczotta nagradza za wybitne prace naukowe, obejmujące zagadnienia mieszczące się w zakresie górnictwa i dziedzin bezpośrednio z nim związanych, opublikowane w okresie ostatnich 4 lat (wlicza się rok ogłoszenia konkursu), zawierające wybitne elementy w stosunku do aktualnego stanu wiedzy i nauki w świecie'
        )

    # 97
    def test_97_1(self):
        self.check_phrase_response(
            'czym jest konkurs o nagrodę imienia profesora antoniego rodziewicza-bielewicza',
            'konkurs o nagrodę imienia profesora antoniego rodziewicza-bielewicza nagradza za wybitne prace naukowe, obejmujące zagadnienia mieszczące się w zakresie hutnictwa i dyscyplin ściśle związanych, zawierające elementy nowości w stosunku do aktualnego stanu wiedzy, nauki i techniki w świecie'
        )

    # 98
    def test_98_1(self):
        self.check_phrase_response(
            'co jest tytułem do nagrody imienia profesora Władysława Taklińskiego',
            'tytułem do nagrody imienia profesora Władysława Taklińskiego są wybitne osiągnięcia w dziedzinie dydaktyki, na które mogą się składać między innymi: tworzenie nowych metod w dydaktyce i nowych unikalnych kierunków kształcenia; przygotowanie wykładów z nowych dyscyplin; opracowanie uznanych podręczników i skryptów; wyróżniająca się działalność w tworzeniu nowoczesnych laboratoriów i pracowni problemowych dla celów dydaktyki; wyróżniająca się współpraca z kołami naukowymi i uznanie społeczności studenckiej wyrażonej w ocenie'
        )

    def test_98_2(self):
        self.check_phrase_response(
            'za co nadaje się nagrodę imienia profesora Władysława Taklińskiego',
            'tytułem do nagrody imienia profesora Władysława Taklińskiego są wybitne osiągnięcia w dziedzinie dydaktyki, na które mogą się składać między innymi: tworzenie nowych metod w dydaktyce i nowych unikalnych kierunków kształcenia; przygotowanie wykładów z nowych dyscyplin; opracowanie uznanych podręczników i skryptów; wyróżniająca się działalność w tworzeniu nowoczesnych laboratoriów i pracowni problemowych dla celów dydaktyki; wyróżniająca się współpraca z kołami naukowymi i uznanie społeczności studenckiej wyrażonej w ocenie'
        )

    def test_98_3(self):
        self.check_phrase_response(
            'kto zgłasza kandydatów do nagrody imienia profesora Władysława Taklińskiego',
            'kandydatów do nagrody imienia profesora Władysława Taklińskiego zgłaszają rady wydziałów oraz ich odpowiedniki w jednostkach pozawydziałowych'
        )

    # 99
    def test_99_1(self):
        self.check_phrase_response(
            'czym jest centrum karier agh ',
            'Centrum Karier agh jest jednostką Uczelni zajmującą się wszechstronnym doradztwem zawodowym, pomocą psychologiczną oraz organizacją warsztatów,szkoleń i wykładów (między innymi z zagadnień doskonalenia umiejętności interpersonalnych)'
        )

    def test_99_2(self):
        self.check_phrase_response(
            'czym zajmuje się centrum karier agh',
            'Centrum Karier agh jest jednostką Uczelni zajmującą się wszechstronnym doradztwem zawodowym, pomocą psychologiczną oraz organizacją warsztatów,szkoleń i wykładów (między innymi z zagadnień doskonalenia umiejętności interpersonalnych)'
        )

    def test_99_3(self):
        self.check_phrase_response(
            'jakie bazy prowadzi centrum karier agh',
            'Centrum karier agh prowadzi bank ofert pracy, praktyk i staży zawodowych oraz bazę CV poszukujących pracy studentów i absolwentów'
        )

    def test_99_4(self):
        self.check_phrase_response(
            'jakie informacje można uzyskać w centrum karier agh',
            'W Centrum Karier AGH można uzyskać informacje o firmach i zasadach rekrutacji oraz o programach edukacyjnych, unijnych, wymianach zagranicznych, kursach i innych'
        )

    def test_99_5(self):
        self.check_phrase_response(
            'jaki jest cel działania akademickiego inkubatora przedsiębiorczości agh',
            'Celem działania Akademickiego inkubatora przedsiębiorczości AGH jest propagowanie wśród studentów, doktorantów, absolwentów i pracowników małopolskich szkół wyższych kreatywności i samodzielności zawodowej oraz świadczenie bezpośredniej pomocy w założeniu i prowadzeniu własnej działalności gospodarczej'
        )

    def test_99_6(self):
        self.check_phrase_response(
            'komu udziela wsparcia akademicki inkubator przedsiębiorczości AGH',
            'akademicki inkubator przedsiębiorczości AGH udziela wsparcia osobom zakładającym działalność gospodarczą, tak aby zniwelować do minimum koszty wynajmu i wyposażenia biura, porad prawnych, koszty prowadzenia księgowości i tym podobne'
        )

    def test_99_7(self):
        self.check_phrase_response(
            'w jaki sposób udziela wsparcia akademicki inkubator przedsiębiorczości AGH',
            'akademicki inkubator przedsiębiorczości AGH udziela wsparcia osobom zakładającym działalność gospodarczą, tak aby zniwelować do minimum koszty wynajmu i wyposażenia biura, porad prawnych, koszty prowadzenia księgowości i tym podobne'
        )

    def test_99_8(self):
        self.check_phrase_response(
            'co jest ideą akademickiego Inkubatora przedsiębiorczości',
            'Ideą akademickiego Inkubatora przedsiębiorczości jest umożliwienie kreatywnym i ambitnym ludziom założenia własnej firmy przy minimalnych nakładach finansowych, by po okresie inkubacji mogli już samodzielnie funkcjonować w zwykłych warunkach gospodarczych, wykorzystując zdobyte w Inkubatorze doświadczenia oraz niezbędną wiedzę'
        )

    def test_99_9(self):
        self.check_phrase_response(
            'na jakich etapach tworzenia firmy wsparcia udziela akademicki Inkubator przedsiębiorczości',
            'akademicki Inkubator przedsiębiorczości jest instytucją wspomagającą swoich beneficjentów na każdym etapie tworzenia firmy, od pomysłu na biznes, poprzez jego urealnienie, do wdrożenia'
        )

if __name__ == '__main__':
    unittest.main()