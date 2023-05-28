from interface import RuleInterface


class Rule:
    """
    Rule class, every new rule must extend from this class
    """

    def __init__(self, param: RuleInterface):
        self.val = 0.00             # default value
        self.param = param          # parameter object, retrieved from the main script
        self.rule_name = 'defaultrule'
        self.max_value = 1
        self.param_min = 'min'
        self.param_max = 'max'
        self.best = 'right'

    def calculate(self) -> float | int:
        """Implement
        ----
        Override this function! Put the calculations in self.val
        """
        print("empty rule!")
        quit()

    def setup_param(self):
        """Implement
        ---- 
        Implement this function by override the values below \n
        @param self.rule_name: str\\
             name of the rule, abbreviation only \n
        @param self.max_value: float | str\\
            maximum value, use '+' if towards positive infinity \n
        @param self.param_min: str \\
            minimum parameter if value near min_value \n
        @param self.param_max: str \\
            maximum parameter if value near max_value \n
        @param self.best: str ('left' or 'right') \\
            better quality moving towards minimum (left) or maximum (right) \n
        """
        print("empty rule!")
        quit()

    def print(self):
        self.setup_param()
        self.val = self.calculate()
        self._print_value()
        self._print_progress()

    def _print_value(self):
        print(f"{self.rule_name} Value: " + str(self.val))

    def _print_progress(self):
        if self.best == 'left':
            left = "better"
            right = "worse"
        elif self.best == 'right':
            left = 'worse'
            right = 'better'
        else:
            print("rule 'best' value must be either 'left' or 'right'!")
            quit()

        print(f"({left}) {self.param_min} [0] ", end='')
        self._progress_bar(
            self.max_value, self.val) if self.max_value != '+' else print('-', end='')
        print(f" [{self.max_value}] {self.param_max} ({right})")

    def _progress_bar(self, max, value):
        val = (value / max) * 15
        value = int(val)
        max = 15
        remaining = max - value
        filled = chr(0x2588) + chr(0x2502)
        empty = chr(0x2591) + chr(0x2502)
        filled_char = filled * value
        empty_char = empty * remaining
        print(filled_char + empty_char, end='')


def __init__(self, val, name, param_min, param_max, is_best_left, max):
    self.val = val
    self.name = name
    self.param_min = param_min
    self.param_max = param_max
    self.is_best_left = is_best_left
    self.max = max
