import re


class PersianEditor:
    """
    A class for Persian Text Sanitization
    """
    def __init__(self, text):
        """
        This is the base part of the class
        """

        self.text = text
        self._cleanup_zwnj = False
        self._fix_dashes = True
        self._fix_three_dots = True
        self._fix_hamzeh = True
        self._hamzeh_with_yeh = True
        self._fix_prefix_spacing = True
        self._fix_prefix_separate = True
        self._fix_suffix_spacing = True
        self._fix_suffix_separate = True
        self._aggresive = True
        self._cleanup_kashidas = True
        self._fix_english_quotes = True
        self._cleanup_extra_marks = True
        self._cleanup_spacing = True
        self._fix_spacing_for_braces_and_quotes = True
        self._fix_arabic_numbers = True
        self._fix_english_numbers = True
        self._fix_misc_non_persian_chars = True
        self._trim_leading_trailing_whitespaces = True

        UnTouchable() # to generate the untouchable words
        self.cleanup()

    def cleanup(self):
        if self._fix_dashes: self.fix_dashes()
        if self._fix_three_dots: self.fix_three_dots()
        if self._fix_english_quotes: self.fix_english_quotes()
        if self._fix_hamzeh: self.fix_hamzeh()
        if self._cleanup_zwnj: self.cleanup_zwnj()
        if self._fix_misc_non_persian_chars: self.char_validator()
        if self._fix_arabic_numbers: self.fix_arabic_numbers()
        if self._fix_english_numbers: self.fix_english_numbers()
        if self._fix_prefix_spacing: self.fix_prefix_spacing()
        if self._fix_prefix_separate: self.fix_prefix_separate()
        if self._fix_suffix_spacing: self.fix_suffix_spacing()
        if self._fix_suffix_separate: self.fix_suffix_separate()
        if self._aggresive: self.aggressive()
        if self._cleanup_spacing: self.cleanup_spacing()
        if self._fix_spacing_for_braces_and_quotes:
            self.fix_spacing_for_braces_and_quotes()
        if self._trim_leading_trailing_whitespaces:
            self.text = '\n'.join([line.strip() for line in self.text.split('\n')])
        self.cleanup_redundant_zwnj()

        return self.text

    def __str__(self):
        return self.text

    __repr__ = __str__

    def fix_dashes(self):
        """Replaces double and triple dashes with `ndash` and `mdash`, respectively."""
        self.text = re.sub(r'-{3}', r'—', self.text)
        self.text = re.sub(r'-{2}', r'–', self.text)

    def fix_three_dots(self):
        """Replaces three dots with an ellipsis."""
        self.text = re.sub(r'\s*\.{3,}', r'…', self.text)

    def fix_english_quotes(self):
        """Replaces English quotes with their Persian counterparts."""
        self.text = re.sub(r"([\"'`]+)(.+?)(\1)", r'«\2»', self.text)

    def fix_hamzeh(self):
        """Replaces trailing 'ه ی' with 'هٔ' or 'ه‌ی'--the last one is achievable if hamzeh_with_yeh set."""
        if self._hamzeh_with_yeh:
            self.text = re.sub(r'(\S)(ه[\s]+[یي])(\b)',r'\1ه‌ی\3',self.text)
        else:
            self.text = re.sub(r'(\S)(ه[\s]+[یي])(\b)',r'\1هٔ\3', self.text)

    def cleanup_zwnj(self):
        """Removes unnecessary ZWNJ that are succeeded/preceded by a space."""
        self.text = re.sub(r'\s+|\s+', r' ', self.text)

    def cleanup_redundant_zwnj(self):
        """Removes unwanted ZWNJs which are added by some sanitization tasks."""
        self.text = re.sub(r'([ءاأدذرزژوؤ])‌+', r'\1', self.text)
        self.text = re.sub(r'(‌)+', r'\1', self.text)

    def char_validator(self):
        """Replaces invalid characters with valid ones."""
        bad_chars  = ",;%يةك"
        good_chars = "،؛٪یهک"
        self.text = self.char_translator(bad_chars, good_chars, self.text)

    def fix_arabic_numbers(self):
        """Translates Arabic numbers to their Persian counterparts."""
        persian_numbers = "۱۲۳۴۵۶۷۸۹۰"
        arabic_numbers = "١٢٣٤٥٦٧٨٩٠"
        self.text = self.char_translator(
            arabic_numbers,
            persian_numbers,
            self.text
        )

    def fix_english_numbers(self):
        """Translates English numbers to their Persian counterparts."""
        persian_numbers = "۱۲۳۴۵۶۷۸۹۰"
        english_numbers = "1234567890"
        self.text = self.char_translator(
            english_numbers,
            persian_numbers,
            self.text
        )

        # Avoids to change English numbers in strings like 'Text12', 'Text_12', or 'A4'
        self.text = re.sub(
            r'[۰-۹]+[a-zA-Z_]{1,}[۰-۹]+|[a-zA-Z_]{1,}[۰-۹]+|[۰-۹]+[a-zA-Z_]{1,}',
            lambda m:
            self.char_translator(persian_numbers, english_numbers, m.group()),
            self.text
        )

    def fix_prefix_spacing(self):
        """Puts ZWNJ between a word and its prefix (mi* nemi* bi*)"""
        self.text = re.sub(r"\b(ن?می|بی)‌*(\s+)",r'\1‌', self.text)

    def fix_prefix_separate(self):
        """Puts ZWNJ between a word and its prefix (mi* nemi* bi*)"""
        regex = re.compile(r"\b(بی|ن?می)‌*([^\[\]\(\)\s]+)") #  \b for words like سهمیه

        wlist = self.text.split(" ")
        for word in wlist:
            regx_iter = regex.finditer(word)
            for p in regx_iter:
                # Checks that the prefix (mi* nemi* bi*) is part a a word or not, like میلاد.
                if p.group() not in UnTouchable.words:
                    self.text = re.sub(
                        re.escape( p.group() ),
                        p.group(1) + r"‌" + p.group(2),
                        self.text
                    )

    def fix_suffix_spacing(self):
        """Puts ZWNJ between a word and its suffix (*ha[ye] *tar[in])"""
        regex = re.compile(
            r"""\s+
            (تر(ی(ن)?)?
            |[تمش]ان
            |ها(ی(ی|ت|م|ش|تان|شان)?)?)
            \b""",
            re.VERBOSE
        )
        self.text = re.sub(regex, r'‌\1', self.text)

        # Some special cases like و شان خود
        regex = re.compile(r"\b(\w)‌([تمش]ان)\b", re.VERBOSE)
        self.text = re.sub(regex, r'\1 \2', self.text)

        # Ash(=اش) at the end of some words like خانه‌اش or پایانی‌اش
        regex = re.compile(r"\b(\w+)(ه|ی)\s+(اش)\b", re.VERBOSE)
        self.text = re.sub(regex, r'\1\2‌\3', self.text)

    def fix_suffix_separate(self):
        """Puts ZWNJ between a word with its suffix (haye, ...)"""
        regex = re.compile(
            r"""(\S+?) # not-greedy fetch to handle some case like هایشان instead شان
            (تر(ی(ن)?)?
            |[تمش]ان
            |ها(ی(ی|ت|م|ش|تان|شان)?)?)\b""",
            re.VERBOSE
        )
        wlist = self.text.split(" ")
        for word in wlist:
            regx_iter = regex.finditer(word)
            for p in regx_iter:
                # Checks that the suffix (tar* haye*) is part of a word or not, like بهتر.
                if p.group() not in UnTouchable.words:
                    self.text = re.sub(
                        re.escape( p.group() ),
                        p.group(1) + r"‌" + p.group(2) ,
                        self.text
                    )

    def aggressive(self):
        """Reduces Aggressive Punctuation to one sign."""
        if self._cleanup_extra_marks:
            self.text = re.sub(r'(!){2,}[!\s]*', r'\1', self.text)
            self.text = re.sub(r'(؟){2,}[؟\s]*', r'\1', self.text)

        if self._cleanup_kashidas:
            self.text = re.sub(r'ـ+', "", self.text)

    def fix_spacing_for_braces_and_quotes(self):
        """Fixes the braces and quotes spacing problems."""
        # ()[]{}""«» should have one space before and no space after (inside)
        self.text = re.sub(
            r'[ ‌]*(\()\s*([^)]+?)\s*?(\))[ ‌]*',
            r' \1\2\3 ',
            self.text
        )
        self.text = re.sub(
            r'[ ‌]*(\[)\s*([^)]+?)\s*?(\])[ ‌]*',
            r' \1\2\3 ',
            self.text
        )
        self.text = re.sub(
            r'[ ‌]*(\{)\s*([^)]+?)\s*?(\})[ ‌]*',
            r' \1\2\3 ',
            self.text
        )
        self.text = re.sub(
            r'[ ‌]*(“)\s*([^)]+?)\s*?(”)[ ‌]*',
            r' \1\2\3 ',
            self.text
        )
        self.text = re.sub(
            r'[ ‌]*(«)\s*([^)]+?)\s*?(»)[ ‌]*',
            r' \1\2\3 ',
            self.text
        )
        # : ; , ! ? and their Persian counterparts should have one space after and no space before
        self.text = re.sub(
            r'[ ‌ ]*([:;,؛،.؟!]{1})[ ‌ ]*',
            r'\1 ',
            self.text
        )
        self.text = re.sub(
            r'[ ‌ ]*((؟\s+!){1})[ ‌ ]*',
            r'؟!',
            self.text
        )
        self.text = re.sub(
            r'([۰-۹]+):\s+([۰-۹]+)',
            r'\1:\2',
            self.text
        )
        # Fixes inside spacing for () [] {} "" «»
        self.text = re.sub(
            r'(\()\s*([^)]+?)\s*?(\))',
            r'\1\2\3',
            self.text
        )
        self.text = re.sub(
            r'(\[)\s*([^)]+?)\s*?(\])',
            r'\1\2\3',
            self.text
        )
        self.text = re.sub(
            r'(\{)\s*([^)]+?)\s*?(\})',
            r'\1\2\3',
            self.text
        )
        self.text = re.sub(
            r'(“)\s*([^)]+?)\s*?(”)',
            r'\1\2\3',
            self.text
        )
        self.text = re.sub(
            r'(«)\s*([^)]+?)\s*?(»)',
            r'\1\2\3',
            self.text
        )

    def cleanup_spacing(self):
        """Reduces multiple consecutive spaces to one."""
        self.text = re.sub(r'[ ]+', r' ', self.text)
        # self.text = re.sub(r'([\n]+)[ ‌]', r'\1', self.text)
        self.text = re.sub(r'\n{2,}', r'\n\n', self.text)

    @classmethod
    def char_translator(cls, fromchar, tochar, string):
        """Translates the 'string' character by character from 'fromchar' to 'tochar'."""
        newstring = string
        for fc, tc in zip(fromchar, tochar):
            newstring = re.sub(fc, tc, newstring)
        return newstring


class UnTouchable:
    DATAFILE = "untouchable.dat"
    words = set() # a set storing all untouchable words

    @classmethod
    def __init__(cls):
        cls.generate()

    @classmethod
    def get(cls):
        return cls.words

    @classmethod
    def add(cls, word_list):
        # TODO: What da fuck? No write access to file-system
        # Should be changed to another way
        with open(cls.DATAFILE, "a", encoding="utf8") as f:
            for word in word_list:
                if word not in cls.words:
                    f.write(word+"\n")
                    cls.words.add(word)

    @classmethod
    def generate(cls):
        """
        This method generates a Unicode list from 'data/untouchable.dat'
        containing such words like 'بهتر' or 'میلاد' which suffixes/prefixes functions
        should not have to touch them
        """
        with open(cls.DATAFILE, encoding='utf8') as f:
            for line in f:
                # I had to strip the f.readline() to prevent white spaces
                cls.words.add(line.strip())
