def mensagem(mensagem=0, arquivo=""):
    msg = ""

    match mensagem:
        case 0:
            msg = "Pastas Fonte e Fechamento estão vazias!"
        case 1:
            msg = "Arquivos prontos para cópia!"
        case 2:
            msg = f"Arquivo {arquivo} lido com sucesso!"
        case 3:
            msg = "Selecione um pedido na barra lateral"
        case 4:
            msg = "Pastas OK"
    
    return msg