from durable.lang import *
from durable.engine import MessageNotHandledException
import re
import pandas as pd

class SuspiciousMessageEngine:
    _rules_initialized = False  # Class-level flag to track if rules have been initialized
    
    def __init__(self):
        self.phrases = []
        self.words = []
        
        # Load phrases and words
        self._load_words_phrases()
        
        # Initialize rules only once across instances
        if not SuspiciousMessageEngine._rules_initialized:
            self._initialize_rules()
            SuspiciousMessageEngine._rules_initialized = True
        
    def _load_words_phrases(self):
        # Load suspicious words
        with open("common_suspicious_words.txt", 'r') as file:
            for word in file:
                self.words.append(word.strip())
                
        # Load suspicious phrases
        with open("common_suspicious_phrases.txt", 'r') as file:
            for line in file:
                self.phrases.append(line.strip())
                
    def _initialize_rules(self):
        with ruleset("suspicious_message_detection"):
            
            # Rule for detecting common suspicious phrases
            @when_all(m.text.matches('|'.join(self.phrases)))
            def common_phrases_detected(c):
                c.s['is_suspicious'] = True  # Set flag when suspicious phrase is detected
            
            # Rule for detecting URLs
            @when_all(m.text.matches(r'https?://[^\s]+') | m.text.matches(r'www\.[^\s]+') | m.text.matches(r'[^\s]+\.(com|org|net|io|gov|edu|info)'))
            def url_detected(c):
                c.s['is_suspicious'] = True  # Set flag when URL is detected
            
            # Rule for detecting suspicious words
            @when_all(m.text.matches('|'.join(self.words)))
            def suspicious_words_detected(c):
                c.s['is_suspicious'] = True  # Set flag when suspicious word is detected
    
    def predict(self, message):
        # If `message` is a single string, process it as a single message
        if isinstance(message, str):
            return self.predict_single_message(message)
        
        # If `message` is a pandas Series, apply `predict_single_message` on each row
        elif isinstance(message, pd.Series):
            return message.map(self.predict_single_message)
    
    def predict_single_message(self, message_text):
        # Use a dictionary to track the flag
        state = {'text': message_text, 'is_suspicious': False}
        
        # Post the message to the rules engine
        try:
            post('suspicious_message_detection', state)
        except MessageNotHandledException:
            # If no rule matched, is_suspicious remains False
            pass
        
        # Return whether the message was flagged as suspicious
        return 'yes' if state['is_suspicious'] else 'no'
