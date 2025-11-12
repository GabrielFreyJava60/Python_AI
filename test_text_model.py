from unittest import TestCase, main
from text_sklearn_model import TextModel

text = "I want to start working as a programmer. I'm learning programming at Tel-Ran course. The teacher says to us that for becoming a programmer you should perform Homeworks. But because of family and work I don't have time to do Homeworks"


class TestTextModel(TestCase):
    
    def setUp(self):
        self.textModel = TextModel(text)
    
    def test_two_answers_returned(self):
        expected = [
            'The teacher says to us that for becoming a programmer you should perform Homeworks',
            "But because of family and work I don't have time to do Homeworks"
        ]
        result = self.textModel.getAnswers("Should you perform Homeworks", 2)
        self.assertEqual(expected, result)
    
    def test_one_answer_returned(self):
        expected = [
            'The teacher says to us that for becoming a programmer you should perform Homeworks'
        ]
        result = self.textModel.getAnswers("What should you perform", 2)
        self.assertEqual(expected, result)
    
    def test_no_answer_returned(self):
        expected = []
        result = self.textModel.getAnswers("What desturbs me achieve the purpose? ", 2)
        self.assertEqual(expected, result)
    
    def test_empty_text(self):
        empty_model = TextModel("")
        result = empty_model.getAnswers("test question", 5)
        self.assertEqual([], result)
    
    def test_nAnswers_limit(self):
        long_text = ". ".join([f"Sentence {i} about programming" for i in range(10)])
        model = TextModel(long_text)
        result = model.getAnswers("programming", 3)
        self.assertLessEqual(len(result), 3)
    
    def test_zero_similarity_filtered(self):
        text = "The cat sat on the mat. Dogs bark loudly."
        model = TextModel(text)
        result = model.getAnswers("quantum physics", 5)
        self.assertEqual([], result)
    
    def test_sorted_by_relevance(self):
        text = "Machine learning uses algorithms. Deep learning is machine learning. Python is popular."
        model = TextModel(text)
        result = model.getAnswers("machine learning algorithms", 3)
        self.assertGreater(len(result), 0)
        self.assertLessEqual(len(result), 3)


if __name__ == "__main__":
    main()

