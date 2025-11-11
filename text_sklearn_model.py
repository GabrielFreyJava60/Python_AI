from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class TextModel:
    
    def __init__(self, text: str):
        sentences = [s.strip() for s in text.split('.') if s.strip()]
        self.sentences = sentences
        self.vectorizer = TfidfVectorizer()
        if self.sentences:
            self.sentence_vectors = self.vectorizer.fit_transform(self.sentences)
        else:
            self.sentence_vectors = None
    
    def getAnswers(self, question: str, nAnswers: int) -> list[str]:
        if not self.sentences or self.sentence_vectors is None:
            return []
        question_vector = self.vectorizer.transform([question])
        similarities = cosine_similarity(question_vector, self.sentence_vectors)[0]
        sentence_similarities = [(sim, sentence) for sim, sentence in zip(similarities, self.sentences)]
        filtered_similarities = [(sim, sentence) for sim, sentence in sentence_similarities if sim > 0]
        filtered_similarities.sort(key=lambda x: x[0], reverse=True)
        answers = [sentence for _, sentence in filtered_similarities[:nAnswers]]
        return answers

