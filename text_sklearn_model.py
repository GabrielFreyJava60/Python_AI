from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import heapq


class TextModel:
    
    def __init__(self, text: str):
        sentences = [
            sentence.strip() 
            for sentence in text.split('.') 
            if sentence.strip()
        ]
        
        self.sentences = sentences
        self.vectorizer = TfidfVectorizer(stop_words="english")
        
        if self.sentences:
            self.sentence_vectors = self.vectorizer.fit_transform(self.sentences)
        else:
            self.sentence_vectors = None
    
    def getAnswers(self, question: str, nAnswers: int) -> list[str]:
        if not self.sentences or self.sentence_vectors is None:
            return []
        
        question_vector = self.vectorizer.transform([question])
        similarities = cosine_similarity(question_vector, self.sentence_vectors)[0]
        
        similarity_sentence_pairs = [
            (similarity, sentence) 
            for similarity, sentence in zip(similarities, self.sentences) 
            if similarity > 0
        ]
        
        if not similarity_sentence_pairs:
            return []
        
        top_results = heapq.nlargest(
            nAnswers, 
            similarity_sentence_pairs, 
            key=lambda pair: pair[0]
        )
        
        answers = [sentence for similarity, sentence in top_results]
        
        return answers
