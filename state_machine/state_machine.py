import json


class StateMachine:
    def __init__(self, state_json, init_state):
        self.current_state = init_state
        self.state_history = [self.current_state]
        with open(state_json) as state_json:
            self.state_dict = json.load(state_json)

    def transition(self, new_state):
        if new_state not in self.state_dict[self.current_state]:
            raise ValueError('The new state is not a valid downstream state')
        else:
            self.current_state = new_state
            self.state_history.append(self.current_state)

