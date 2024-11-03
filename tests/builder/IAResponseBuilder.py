
class IAResponseBuilder:
    def __init__(self):
        self.answer = "Lorem ipsum"

    def with_answer(self, answer:str):
        self.answer = answer
        return self
    
    def build(self):
        return {
            "answer": self.answer
        }