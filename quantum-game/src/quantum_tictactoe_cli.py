import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from quantum_engine import QuantumTicTacToe


def print_board(game: QuantumTicTacToe):
    print("\n" + "=" * 55)
    print("           QUANTUM TIC-TAC-TOE BOARD")
    print("=" * 55)
    for r in range(3):
        row_str = []
        for c in range(3):
            idx = r * 3 + c
            classical = game.board_classical[idx]
            if classical is not None:
                sub = game.board_subscripts[idx]
                row_str.append(f" [{classical}{sub}] ".center(16))
            else:
                spookies = game.get_cell_spooky_marks(idx)
                if spookies:
                    spooky_text = ",".join(f"{m.player}{m.move_id}" for m in spookies)
                    row_str.append(f" {idx+1}:({spooky_text}) ".center(16))
                else:
                    row_str.append(f" [{idx+1}] ".center(16))
        print("|".join(row_str))
        if r < 2:
            print("-" * 55)
    print("=" * 55)
    print(f"Status: {game.status_message}\n")


def play_cli():
    print("Welcome to Quantum Tic-Tac-Toe powered by IBM Qiskit!")
    print("Rules:")
    print("1. Each turn, you place a quantum mark across TWO cells (e.g., '1 5').")
    print("2. Spooky marks exist in superposition until an entanglement cycle forms.")
    print("3. When a cycle forms, IBM Qiskit simulates the quantum collapse onto real states!")
    print("4. You can also type 'collapse' at any time to force a quantum measurement.")
    print("5. Type 'quit' to exit.\n")

    game = QuantumTicTacToe()

    while not game.game_over:
        print_board(game)
        prompt = f"Player {game.current_player}'s move (enter two square numbers 1-9 separated by space, or 'collapse'): "
        try:
            user_input = input(prompt).strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting game.")
            sys.exit(0)

        if user_input == 'quit':
            print("Thanks for playing!")
            break

        if user_input == 'collapse':
            print("\n>> Triggering Qiskit quantum measurement simulation...")
            msg, qc = game.trigger_quantum_collapse(force_all=True)
            print(msg)
            print("\nQiskit Quantum Circuit:")
            print(qc.draw(output='text'))
            continue

        parts = user_input.split()
        if len(parts) != 2:
            print("Invalid input! Please enter two numbers (1-9), e.g., '1 2' or '4 9'.")
            continue

        try:
            sq1 = int(parts[0]) - 1
            sq2 = int(parts[1]) - 1
        except ValueError:
            print("Please enter valid integer square numbers.")
            continue

        success, msg, cycle = game.place_quantum_move(sq1, sq2)
        print(f"\n>> {msg}")

        if cycle:
            print("\n Entanglement cycle detected! Automatic quantum collapse initiated with Qiskit Aer...")
            collapse_msg, qc = game.trigger_quantum_collapse()
            print(collapse_msg)
            print("\nGenerated Qiskit Circuit:")
            print(qc.draw(output='text'))

    if game.game_over:
        print_board(game)
        print(f"GAME OVER! Winner: {game.winner}")
        print(game.status_message)


if __name__ == "__main__":
    play_cli()
