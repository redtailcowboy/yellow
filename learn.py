import xgboost as xgb
import pandas as pd
from sklearn.model_selection import train_test_split
import os

class AIPlayer:
    def __init__(self):
        self.data_file = 'blackjack_data.csv'
        self.model_file = 'blackjack_model.json'
        self.model = None
        if os.path.exists(self.model_file):
            self.load_model()
        else:
            self.initialize_data_file()

    def initialize_data_file(self):
        if not os.path.exists(self.data_file):
            with open(self.data_file, 'w') as file:
                file.write('player_hand_value,dealer_visible_card_value,player_has_ace,decision,outcome\n')

    def load_model(self):
        self.model = xgb.Booster()
        self.model.load_model(self.model_file)

    def make_decision(self, game_state):
        if self.model:
            # Convert game_state to a DMatrix for prediction
            dmatrix = xgb.DMatrix(pd.DataFrame([game_state]))
            action_prob = self.model.predict(dmatrix)
            action = 'hit' if action_prob > 0.5 else 'stand'
        else:
            action = 'hit' if game_state['player_hand_value'] < 17 else 'stand'
        return action

    def record_decision(self, game_state, decision, outcome):
        with open(self.data_file, 'a') as file:
            file.write(f"{game_state['player_hand_value']},{game_state['dealer_visible_card_value']},{int(game_state['player_has_ace'])},{decision},{outcome}\n")
        self.train_model()

    def train_model(self):
        data = pd.read_csv(self.data_file)
        X = data.iloc[:, :-2]
        y = data['outcome'].apply(lambda x: 1 if x == 'win' else 0)
        if len(X) > 10:  # Ensure we have enough data to split
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            params = {'max_depth': 3, 'eta': 0.1, 'objective': 'binary:logistic', 'eval_metric': 'logloss'}
            if self.model is None:
                # Initialize model if not loaded
                self.model = xgb.train(params, xgb.DMatrix(X_train, label=y_train), num_boost_round=10)
            else:
                # Update model if already initialized
                self.model = xgb.train(params, xgb.DMatrix(X_train, label=y_train), num_boost_round=10, xgb_model=self.model)
            # Save the updated model
            self.model.save_model(self.model_file)

# Example usage
if __name__ == '__main__':
    ai_player = AIPlayer()
    game_state = {'player_hand_value': 18, 'dealer_visible_card_value': 10, 'player_has_ace': False}
    print(ai_player.make_decision(game_state))
