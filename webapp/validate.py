from django.core.exceptions import ValidationError

BAD_WORDS = ['bomb', 'asshole', 'bitch', 'bullshit', 'fuck', 'motherfucker', 'wtf']
BAD_CHARS = ['+', '(', ')', '%', '*', '@', '#']


def bad_words(text):
    for i in BAD_WORDS:
        if i.lower() in text.lower():
            raise ValidationError(f'Description should not contain "{i}!". Forbidden words {BAD_WORDS}')


def bad_chars(name):
    for i in BAD_CHARS:
        if i in name:
            raise ValidationError(f'Summary should not contain "{i}"!. Forbidden symbols {BAD_CHARS}')


def check_count(list):
    if len(list) == 3:
        raise ValidationError(f'"type" cannot be equal to 3')
