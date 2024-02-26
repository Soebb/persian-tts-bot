#ifndef HAZM_H
#define HAZM_H

#include <string>
#include <vector>
#include <unordered_set>
#include <mutex>

typedef struct _object HazmPyObject;
namespace Hazm
{

class HazmObject
{
public:
    HazmObject(const std::string &py_name, const std::vector<std::pair<std::string, std::string>> &kwargs);
    virtual ~HazmObject();

protected:
    static HazmPyObject* vectorToPyObject(const std::vector<std::string> &data);
    static std::vector<std::string> pyObjectToVector(HazmPyObject* incoming);
protected:
    HazmPyObject *m_object = nullptr;
    static HazmPyObject *m_hazm_dict;
    static HazmPyObject *m_hazm_module;
    static std::mutex m_hazm_mutex;
    static std::unordered_set<HazmObject*> m_hazm_objects;
};


class Normalizer: public HazmObject
{
public:
    Normalizer();
    virtual ~Normalizer();

    std::string normalize(const std::string &text);

private:
    HazmPyObject *m_normalize_method = nullptr;
};


class Stemmer: public HazmObject
{
public:
    Stemmer();
    virtual ~Stemmer();

    std::string stem(const std::string &text);

private:
    HazmPyObject *m_stem_method = nullptr;
};


class Lemmatizer: public HazmObject
{
public:
    Lemmatizer();
    virtual ~Lemmatizer();

    std::string lemmatize(const std::string &text);

private:
    HazmPyObject *m_lemmatize_method = nullptr;
};


class SentenceTokenizer: public HazmObject
{
public:
    SentenceTokenizer();
    virtual ~SentenceTokenizer();

    std::vector<std::string> tokenize(const std::string &text);

private:
    HazmPyObject *m_tokenize_method = nullptr;
};

std::vector<std::string> sent_tokenize(const std::string &text);


class WordTokenizer: public HazmObject
{
public:
    WordTokenizer();
    virtual ~WordTokenizer();

    std::vector<std::string> tokenize(const std::string &text);

private:
    HazmPyObject *m_tokenize_method = nullptr;
};

std::vector<std::string> word_tokenize(const std::string &text);


class POSTagger: public HazmObject
{
    friend class Chunker;
public:
    struct TagItem {
        std::string type;
        std::string word;
    };

    POSTagger(const std::string &model);
    virtual ~POSTagger();

    std::vector<TagItem> tag(const std::vector<std::string> &tokens);

protected:
    static std::vector<POSTagger::TagItem> pyObjectToTagsVector(HazmPyObject* incoming);
    static HazmPyObject *tagsVectorToPyObject(const std::vector<POSTagger::TagItem> &tags);
private:
    HazmPyObject *m_tag_method = nullptr;
};


class Chunker: public HazmObject
{
public:
    struct TreeNode: POSTagger::TagItem {
        std::vector<TreeNode> childs;
    };

    Chunker(const std::string &model);
    virtual ~Chunker();

    TreeNode parse(const std::vector<POSTagger::TagItem> &tags);

protected:
    static TreeNode pyObjectToTreeNode(HazmPyObject* incoming);
private:
    HazmPyObject *m_parse_method = nullptr;
};

std::string tree2brackets(const Chunker::TreeNode &tree);
};

#endif // HAZM_H
