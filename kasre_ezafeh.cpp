#include "hazm.h"

#include <iostream>
#include <string>
using namespace Hazm;

int main()
{
    Normalizer normalizer;
    POSTagger tagger("pos_tagger.model");
    std::cout << "Enter text:";
    std::string input;
    std::getline(std::cin, input);
    std::string normlized_text = normalizer.normalize(input);
    std::string  processed_sentences = "";
    for (auto &sentence: sent_tokenize(normlized_text)) {
        std::vector<std::string> words = word_tokenize(sentence);
        std::string fixed_words = "";
        for (auto &word: tagger.tag(words)) {
            if ((word.type).substr(word.type.length()-1,1) == "Z" ) { 
                if ((word.word).substr(word.word.length()-2,2) != "ِ")  {
                    if ( (word.word).substr(word.word.length()-2,2) == "ه" and (word.word).substr(word.word.length()-4,2) != "ا") { 
                        word.word += "‌ی";
                    }
                }
                word.word += "ِ";
            }
            fixed_words += word.word + " ";
        }
        processed_sentences += fixed_words;
        
    }
    std::cout << processed_sentences << std::endl;
    return 0;
}
