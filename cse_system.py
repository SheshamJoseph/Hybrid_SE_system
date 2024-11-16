from matplotlib import axis
import pandas as pd

class CSESystem:
    """
    A system that combines a rule-based engine and a machine learning model to detect potentially suspicious messages.
    
    The rule engine acts as a filter to quickly assess whether a message is suspicious. If the rule engine flags a
    message as suspicious, it is then passed to a machine learning model for further analysis. The model provides
    a more detailed classification, with results indicating whether a message is suspicious ('yes') or not ('no').
    """
    def __init__(self, model, engine):
        """
        Initializes the SuspiciousMessageSystem with a rule-based engine and a machine learning model.
        Args:
            model (object): A trained machine learning model that returns an array with
                            probabilities or class predictions.
            engine (object): Instance of rule based engine
        """
        self.model = model
        self.engine = engine
        
    def predict(self, messages):
        """
        Predicts whether each message in a given list or pd.Series is suspicious
        It first passes each message to the rule engine, if the message is flagged as suspicous
        it is then passed to the model for deeper analysis
        Args:
            messages (str | list | pd.Series)

        Returns:
            list[str]: A list of labels('yes' or 'no') for each messgae
        """
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
                