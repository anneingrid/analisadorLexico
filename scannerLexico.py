import re

tokens = [
    ('palavra reservada', r'\bwhile\b'),
    ('palavra reservada', r'\bdo\b'),
    ('operador', r'[+\-*/%&|^!~<>=]'),
    ('identificador', r'\b[i|j]\b'),
    ('constante', r'\b\d+\b'),
    ('espaco', r'\s+'),
    ('terminador',r';')
]

def analisador(codigo):
    pos = 0
    tokens_lista = []
    tabela_simbolos = {}
    indice_simbolos = 1

    while pos < len(codigo):
        correspondente = None
        for tipo_token, padrao in tokens:
            regex = re.compile(padrao)
            correspondente = regex.match(codigo, pos)
            if correspondente:
                texto = correspondente.group(0)
                if tipo_token != 'espaco':
                    tokens_lista.append((tipo_token, texto))
                    if tipo_token == 'identificador' or tipo_token == 'constante':
                        if texto not in tabela_simbolos:
                            tabela_simbolos[texto] = indice_simbolos
                            indice_simbolos += 1
                break
        if not correspondente:
            print(f"Erro: Token não reconhecido na posição {pos}")
            return [], {}
        else:
            pos = correspondente.end(0)
    
    return tokens_lista, tabela_simbolos

def main():
    codigo = """
    while i < 100 do
        i = i + j;
    """
    
    tokens_lista, tabela_simbolos = analisador(codigo)
    
    if not tokens_lista and not tabela_simbolos:
        print("Erro na análise léxica.")
        return
    
    with open('tokens.txt', 'w', encoding='utf-8') as f:
        f.write("> Tokens\n")
        f.write("token | identificação | tamanho | posição\n")
        for token in tokens_lista:
            f.write(f"{token[1]} | {token[0]} | {len(token[1])} | \n")

    with open('simbolos.txt', 'w', encoding='utf-8') as f:
        f.write("> Tabela de símbolos\n")
        f.write("índice | símbolo\n")
        for simbolo, indice in sorted(tabela_simbolos.items(), key=lambda item: item[1]):
            f.write(f"{indice} | {simbolo}\n")

    
    print("Análise léxica concluída. Tabelas geradas em 'tokens.txt' e 'simbolos.txt'.")

if __name__ == '__main__':
    main()
