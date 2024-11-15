from matplotlib import axis
import pandas as pd

class CSESystem:
    def __init__(self, model, engine):
        """
            
        Args:
            model (_type_): _description_
            engine (_type_): _description_
        """
        self.model = model
        self.engine = engine
        
    def predict(self, messages):
        # Ensure input can be processed as a list of messages
        if isinstance(messages, str):
            messages = [messages]
        elif isinstance(messages, pd.Series):
            messages = messages.tolist()
        
        result = []
        for message in messages:
            rule_result = self.engine.predict(message)
            if rule_result == 'yes':
                model_prediction = self.model.predict([message])[0].argmax()
                label = 'yes' if model_prediction == 1 else 'no'
            else:
                label = 'no'
            
            result.append(label)
            
        return result
                