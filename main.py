import time
import random
import json
import os

# configurações do jogo
symbols = ["💎", "💣", "💥", "🔥", "⚠️"]
symbol_weights = [1, 4, 3, 5, 5] 
initial_balance = 100
min_bet = 5
save_file = "saldo.json"

# os prêmios
prizes = {
    "💎": 10,  # jackpot - 10x a aposta
    "💥": 5,   # 5x a aposta
    "outros": 3  # 3x a aposta
}

def clear_screen():
    """limpa a tela do terminal"""
    os.system('cls' if os.name == 'nt' else 'clear')

def load_balance(username):
    """carrega o saldo do arquivo"""
    try:
        if os.path.exists(save_file):
            with open(save_file, 'r') as file:
                data = json.load(file)
                return data.get(username, initial_balance)
    except:
        pass
    return initial_balance

def save_balance(username, balance):
    """salva o saldo no arquivo"""
    data = {}
    try:
        if os.path.exists(save_file):
            with open(save_file, 'r') as file:
                data = json.load(file)
    except:
        pass
    data[username] = balance
    with open(save_file, 'w') as file:
        json.dump(data, file)

def show_header(username, balance):
    """cabeçalho do jogo"""
    clear_screen()
    print("\n" + "="*30)
    print("MÁQUINA DE CASSINO")
    print("="*30)
    print(f"Jogador: {username}")
    print(f"Saldo: R$ {balance}")
    print("="*30 + "\n")

def spin_animation():
    """animação do giro"""
    print("\nGirando", end="")
    for _ in range(3):
        time.sleep(0.5)
        print(".", end="", flush=True)
    print("\n")
    time.sleep(0.3)

def display_result(slot1, slot2, slot3):
    """mostra o resultado dos slots"""
    print("\n")
    print("=" * 30)
    print(f"        {slot1}    {slot2}    {slot3}")
    print("=" * 30)
    print("\n")

def check_win(slot1, slot2, slot3, bet):
    """
    confirma se o jogador ganhou, calcula e retorna:
    (ganhou: booleano
    premio: inteiro
    mensagem: string)

    """
    # prêmio de três símbolos iguais
    if slot1 == slot2 == slot3:
        if slot1 == "💎":
            prize = bet * prizes["💎"]
            message = f" JACKPOT!!! Você ganhou R$ {prize}! "
            return True, prize, message
        elif slot1 == "💥":
            prize = bet * prizes["💥"]
            message = f" SUPER PRÊMIO! Você ganhou R$ {prize}! "
            return True, prize, message
        else:
            prize = bet * prizes["outros"]
            message = f"TRÊS IGUAIS! Você ganhou R$ {prize}!"
            return True, prize, message
    
    # prêmio de dois símbolos iguais
    elif slot1 == slot2 or slot2 == slot3 or slot1 == slot3:
        prize = bet * 2
        message = f"FOI QUASE! Você ganhou R$ {prize}!"
        return True, prize, message
    
    # não ganhou
    else:
        message = "Não foi dessa vez... Tente novamente!"
        return False, 0, message

def show_rules():
    """as regras do jogo são:"""
    clear_screen()
    print("\n" + "="*30)
    print("REGRAS DO JOGO ")
    print("="*30)
    print("\nOBJETIVO:")
    print("   Combinar símbolos nos 3 espaços para ganhar!")
    print("\n PRÊMIOS:")
    print("   💎💎💎 - Jackpot! (10x sua aposta)")
    print("   💥💥💥 - Super prêmio! (5x sua aposta)")
    print("   🔥🔥🔥/💣💣💣/⚠️⚠️⚠️ - (3x sua aposta)")
    print("   Dois iguais - (2x sua aposta)")
    print("\nAPOSTAS:")
    print(f"   Mínimo: R$ {min_bet}")
    print(f"   Máximo: Seu saldo disponível")
    print("\n" + "="*30)
    input("\nPressione ENTER para voltar...")

def play_game():
    """função principal do jogo"""
    clear_screen()
    
    # boas vindas
    print("\nBEM VINDO AO CASSINO!\n")
    username = input("Digite seu nome: ").strip()
    
    if not username:
        username = "Jogador"
    
    # carrega / cria saldo do jogador
    balance = load_balance(username)
    time.sleep(1)
    print(f"\nBoa sorte, {username}! \n")
    time.sleep(1)
    
    # loop principal do cassino
    games_played = 0
    total_won = 0
    total_lost = 0
    
    while True:
        show_header(username, balance)
        
        # verifica se o jogador ainda tem grana para gastar
        if balance <= 0:
            print("\n Você ficou sem dinheiro! ")
            print(f"\nEstatísticas da sessão:")
            print(f"  Jogadas: {games_played}")
            print(f"  Total ganho: R$ {total_won}")
            print(f"  Total perdido: R$ {total_lost}")
            print("\nGame Over! Obrigado por jogar!\n")
            save_balance(username, 0)
            break
        
        # menu de opções
        print("(1)  Jogar")
        print("(2)  Ver estatísticas")
        print("(3)  Ver regras")
        print("(4)  Sair")
        
        choice = input("\nEscolha uma opção: ").strip()
        choice = choice.replace("(", "").replace(")", "")
        
        if choice == "1":
            # loop externo, continua jogando até o jogador querer parar
            keep_playing = True
            
            while keep_playing:
                show_header(username, balance)
                
                # verifica se ainda tem saldo
                if balance <= 0:
                    print("\nVocê ficou sem dinheiro!")
                    keep_playing = False
                    input("\nPressione ENTER para voltar ao menu...")
                    break
                
                # loop interno só pra aposta
                while True:
                    try:
                        bet = int(input(f"\nQuanto você vai apostar? (R$ {min_bet} - R$ {balance}): R$ "))
                    except ValueError:
                        print("Digite um valor válido!")
                        time.sleep(1)
                        continue
                    
                    # validações
                    if bet < min_bet:
                        print(f"A aposta mínima é R$ {min_bet}!")
                        time.sleep(1)
                        continue
                    
                    if bet > balance:
                        print("Você não tem dinheiro suficiente!")
                        time.sleep(1)
                        continue
                    
                    # se chegou aqui, a aposta é válida. Sai do loop interno
                    break

                clear_screen()

                # desconta a aposta
                balance -= bet
                games_played += 1

                # animação do giro
                spin_animation()
                
                # gera os símbolos
                slot1 = random.choices(symbols, weights=symbol_weights)[0]
                slot2 = random.choices(symbols, weights=symbol_weights)[0]
                slot3 = random.choices(symbols, weights=symbol_weights)[0]
                
                # dá o resultado
                display_result(slot1, slot2, slot3)
                
                # verifica se o jogador ganhou
                won, prize, message = check_win(slot1, slot2, slot3, bet)
                
                print(message)
                
                if won:
                    balance += prize
                    total_won += prize
                    print(f"\nNovo saldo: R$ {balance}")
                else:
                    total_lost += bet
                    print(f"\nSaldo restante: R$ {balance}")
                
                # salva o saldo
                save_balance(username, balance)
                
                # pergunta se quer jogar de novo
                print("\n" + "="*30)
                play_again = input("\nJogar novamente? (S/N): ").strip().upper()
                
                if play_again != "S":
                    keep_playing = False
                    print("\nVoltando ao menu...\n")
                    time.sleep(1)
            
        elif choice == "2":
            clear_screen()
            print("\n" + "="*30)
            print("ESTATÍSTICAS DA SESSÃO ")
            print("="*30)
            print(f"\nJogadas realizadas: {games_played}")
            print(f"Total ganho: R$ {total_won}")
            print(f"Total perdido: R$ {total_lost}")
            print(f"Saldo atual: R$ {balance}")
            
            if games_played > 0:
                net = total_won - total_lost
                if net > 0:
                    print(f"\nVocê está ganhando R$ {net}!")
                elif net < 0:
                    print(f"\nVocê está perdendo R$ {abs(net)}")
                else:
                    print(f"\nVocê ainda não ganhou nada!")
            
            print("\n" + "="*30)
            input("\nPressione ENTER para voltar...")
            
        elif choice == "3":
            show_rules()
            
        elif choice == "4":
            clear_screen()
            print(f"\nAté logo, {username}!")
            print(f"Você saiu com R$ {balance}")
            print(f"\nEstatísticas finais:")
            print(f"  Jogadas: {games_played}")
            print(f"  Total ganho: R$ {total_won}")
            print(f"  Total perdido: R$ {total_lost}")
            save_balance(username, balance)
            print("\nVolte sempre!\n")
            break
            
        else:
            print("Opção inválida!")
            time.sleep(1)

# começa o jogo
if __name__ == "__main__":
    try:
        play_game()
    except KeyboardInterrupt:
        print("\n\nJogo interrompido! Até mais!\n")
