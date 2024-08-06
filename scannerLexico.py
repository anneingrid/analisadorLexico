import re

tokens = [
    ('palavra reservada', r'\bwhile\b'),
    ('palavra reservada', r'\bdo\b'),
    ('operador', r'[+\-*/%&|^!~<>=]'),
    ('identificador', r'\b[i|j]\b'),
    ('constante', r'\b\d+\b'),
    ('espaco', r'\s+'),
    ('terminador', r';')
]

def analisador(codigo):
    pos = 0
    linha = 0
    coluna = 0
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
                    if tipo_token == 'identificador' or tipo_token == 'constante':
                        if texto not in tabela_simbolos:
                            tabela_simbolos[texto] = indice_simbolos
                            indice_simbolos += 1
                            
                        tokens_lista.append((texto, [tipo_token ,tabela_simbolos[texto]], linha, coluna))
                    else:
                        tokens_lista.append((texto, tipo_token, linha, coluna))
                
                # Atualizar posição, linha e coluna
                for char in texto:
                    if char == '\n':
                        linha += 1
                        coluna = 0
                    else:
                        coluna += 1

                break
        if not correspondente:
            print(f"Erro: Token não reconhecido na posição {pos} na linha {linha}, coluna {coluna}")
            return [], {}
        else:
            pos = correspondente.end(0)
    
    return tokens_lista, tabela_simbolos

def main():
    codigo = """while i < 100 do
        i = i + j;"""
    
    tokens_lista, tabela_simbolos = analisador(codigo)

    print(tokens_lista)
    if not tokens_lista and not tabela_simbolos:
        print("Erro na análise léxica.")
        return
    
    with open('tokens.txt', 'w', encoding='utf-8') as f:
        f.write("> Tokens\n")
        f.write("-" * 50 + '\n')
        f.write(f"{'TOKEN':<6} | IDENTIFICADOR | TAMANHO | POSIÇÃO\n")
        f.write("-" * 50 + '\n')
        for token in tokens_lista:
            f.write(f"{token[0]:<6} | {token[1]} | {len(token[1])} | ({token[2]} , {token[3]})\n")

    with open('simbolos.txt', 'w', encoding='utf-8') as f:
        f.write("> Tabela de símbolos\n")
        f.write("-" * 20 + '\n')
        f.write(f"{'ÍNDICE':<7} | {'SÍMBOLO':<10}\n")
        f.write("-" * 20 + '\n')
        for simbolo, indice in sorted(tabela_simbolos.items(), key=lambda item: item[1]):
            f.write(f"{indice:<7} | {simbolo:<10}\n")

    print("Análise léxica concluída. Tabelas geradas em 'tokens.txt' e 'simbolos.txt'.")


main()
