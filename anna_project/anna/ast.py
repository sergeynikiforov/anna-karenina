# Classes needed to build Abstract Syntax Tree (AST)
# Objects of these classes will correspond to nodes in the resulting AST
# based on http://jayconrod.com/posts/39/a-simple-interpreter-from-scratch-in-python-part-3

from .models import Word, Paragraph


class WordExpression:
    """Word Expression"""
    def __init__(self, i):
        self.i = i

    def __repr__(self):
        return 'WordExpression({})'.format(self.i.__repr__())

    def eval(self):
        try:
            obj = Word.objects.get(word=self.i.lower())
            par_list = obj.paragraphs.all()
        except Word.DoesNotExist:
            return set([])
        return set(par_list)


class BinopWordExpression:
    """Binary Word Expression, i.e. `w1 AND w2`"""
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

    def __repr__(self):
        return 'BinopWordExpression({operator}, {left}, {right})'.format(operator=self.op, left=self.left, right=self.right)

    def eval(self):
        left_value = self.left.eval()
        right_value = self.right.eval()
        if self.op == 'AND':
            value = left_value & right_value
        elif self.op == 'OR':
            value = left_value | right_value
        else:
            raise RuntimeError('Unknown operator: ' + self.op)
        return value


class NotWordExpression:
    """Represents NOT expression"""
    def __init__(self, exp):
        self.exp = exp

    def __repr__(self):
        return 'NotWordExpression({})'.format(self.exp)

    def eval(self):
        all_par = set(Paragraph.objects.all())
        exp_par = self.exp.eval()
        return all_par - exp_par
