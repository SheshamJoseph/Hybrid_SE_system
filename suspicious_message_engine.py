import re
import pandas as pd

class SuspiciousMessageEngine:
    def __init__(self):
        self.phrases = []
        self.words = []
        
        # Load phrases and words
        self._load_words_phrases()
        
        # Precompile regex patterns
        self.phrases_pattern = re.compile(r'|'.join(re.escape(phrase) for phrase in self.phrases), re.IGNORECASE)
        self.words_pattern = re.compile(r'|'.join(re.escape(word) for word in self.words), re.IGNORECASE)
        self.url_pattern = re.compile(r'(https?://[^\s]+|www\.[^\s]+|\b\w+\.(com|org|net|io|gov|edu|info|de|uk|co|us|ca|biz|tv|me|site|app|shop|xyz)\b)', re.IGNORECASE)
        
    def _load_words_phrases(self):
        # Load suspicious words
        print("Loading common words...")
        with open("common_suspicious_words.txt", 'r') as file:
            self.words = [word.strip() for word in file]
        print("Loaded common words.")
                
        # Load suspicious phrases
        print("Loading common phrases...")
        with open("common_suspicious_phrases.txt", 'r') as file:
            self.phrases = [line.strip() for line in file]
        print("Loaded common phrases.")
                
    def predict(self, messages):
        # Handle both single message strings and pandas Series of messages
        if isinstance(messages, str):
            messages = [messages]
        elif isinstance(messages, pd.Series):
            messages = messages.tolist()
        
        # Process each message
        results = []
        for message in messages:
            is_suspicious = self._is_suspicious(message)
            results.append({'text':message, 'is_suspicious':is_suspicious})
        return pd.DataFrame(results)
    
    def _is_suspicious(self, message_text):
        # Check for suspicious phrases
        if self.phrases_pattern.search(message_text):
            return 'yes'
        
        # Check for suspicious URLs
        if self.url_pattern.search(message_text):
            return 'yes'
        
        # Check for suspicious words
        if self.words_pattern.search(message_text):
            return 'yes'
        
        # Return 'no' if no suspicious patterns are matched
        return 'no'
