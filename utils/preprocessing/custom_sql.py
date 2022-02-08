def preprocess_SQL(sentence, splitter='select'):
    sentence = sentence.strip()
    tokens = sentence.split()

    # Removing tables titles
    if ' as ' in sentence.lower():
        renaming = {}
        for i, _token in enumerate(tokens):
            if _token.lower() == 'as':
                sentence = sentence.replace(f'AS {tokens[i + 1]} ', '')
                sentence = sentence.replace(tokens[i + 1], tokens[i - 1])

                # Сортируем аргументы SELECT
    tokens = sentence.split()
    select_part = []
    select_tokens = []
    before_tokens = []
    after_tokens = []
    select_flag = 'before'
    for _token in tokens:
        if splitter in _token.lower():
            select_flag = 'during'
            before_tokens.append(_token)
        elif select_flag == 'during' and 'from' != _token.lower().strip():
            select_tokens.append(_token)
        else:
            if 'from' in _token.lower().strip():
                select_flag = 'after'
                after_tokens.append(_token)
            elif select_flag == 'after':
                after_tokens.append(_token)
            else:
                before_tokens.append(_token)

    select_part = ' '.join(select_tokens)
    select_tokens = select_part.split(',')
    select_tokens = sorted([_t.strip() for _t in select_tokens])
    select_part = ' , '.join(select_tokens)

    sentence = "{} {} {}".format(' '.join(before_tokens), select_part, ' '.join(after_tokens))

    # Remove name of the table, if there is only one table
    if '.' in sentence and not 'join' in sentence.lower():
        tokens = sentence.split()
        new_tokens = []
        for _token in tokens:
            if '.' in _token:
                new_tokens.append(_token.split('.')[1])
            else:
                new_tokens.append(_token)
        sentence = ' '.join(new_tokens)

    result = sentence.replace('* ', '*').replace(' * ', '*').replace(' ,', ',').replace('( ', '(').replace(' )', ')')
    return result