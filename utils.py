import hazm
import typing
import subprocess
import os

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

def wav2mp3(wav_filename, mp3_filename):
    subprocess.run([
        "static_ffmpeg", "-y", "-i", wav_filename,
        "-codec:a", "libmp3lame", "-qscale:a", "2",
        mp3_filename
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    os.remove(wav_filename)
