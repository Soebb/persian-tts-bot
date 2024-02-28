import hazm
import typing

normalizer = hazm.Normalizer()
sent_tokenizer = hazm.SentenceTokenizer()
word_tokenizer = hazm.WordTokenizer()
tagger = hazm.POSTagger(model=str("pos_tagger.model"))


def preprocess_text(text: str) -> typing.List[typing.List[str]]:
    text = normalizer.normalize(text)
    processed_sentences = []
    for sentence in sent_tokenizer.tokenize(text):
        words = word_tokenizer.tokenize(sentence)
        processed_words = fix_words(words)
        processed_sentences.append(" ".join(processed_words))

    return  " ".join(processed_sentences)


def fix_words(words: typing.List[str]) -> typing.List[str]:
    fixed_words = []
    for word, pos in tagger.tag(words):
        if pos[-1] == "Z":
            if word[-1] != "ِ":
                if (word[-1] == "ه") and (word[-2] != "ا"):
                    word += "‌ی"
            word += "ِ"
                

        fixed_words.append(word)

    return fixed_words
