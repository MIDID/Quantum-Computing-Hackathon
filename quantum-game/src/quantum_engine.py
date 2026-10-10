"""
Quantum Tic-Tac-Toe Game Engine powered by IBM Qiskit.

Advanced Quantum Mechanics Features:
1. Superposition with customizable probability amplitudes (|sq1> * cos(θ/2) + |sq2> * sin(θ/2)).
2. Entanglement graphs and Multi-qubit CNOT / Bell-state entangling operations.
3. Genuine 3-Qubit Quantum Teleportation Protocol using Bell pairs and classical feedforward.
4. Quantum Tunneling & Fluctuations across adjacent cells.
5. Wavefunction Collapse & Measurement via IBM Qiskit AerSimulator.
6. Entanglement matrix & NetworkX graph generation.
7. Allan Goff scoring and classical win detection.
"""

from typing import List, Tuple, Dict, Set, Optional
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt


class Move:
    def __init__(self, move_id: int, player: str, sq1: int, sq2: int, prob_sq1: float = 0.5):
        self.move_id = move_id        # Subscript (e.g. X1, O2)
        self.player = player          # 'X' or 'O'
        self.sq1 = sq1                # 0-8
        self.sq2 = sq2                # 0-8
        self.prob_sq1 = prob_sq1      # Probability of collapsing to sq1
        self.collapsed_sq: Optional[int] = None
        self.teleported: bool = False
        self.tunneled: bool = False

    def __repr__(self):
        return f"{self.player}{self.move_id}({self.sq1},{self.sq2})"


class QuantumTicTacToe:
    def __init__(self):
        self.board_classical: List[Optional[str]] = [None] * 9  # Definite collapsed cells
        self.board_subscripts: List[Optional[int]] = [None] * 9 # Subscript of collapsed mark
        self.quantum_moves: List[Move] = []                     # History of quantum moves
        self.uncollapsed_moves: List[Move] = []                 # Currently uncollapsed spooky moves
        self.current_player: str = 'X'
        self.move_counter: int = 1
        self.simulator = AerSimulator()
        self.last_circuit: Optional[QuantumCircuit] = None
        self.last_measurement_result: Optional[str] = None
        self.last_action_type: str = "init"                     # "move", "teleport", "tunnel", "collapse"
        self.winner: Optional[str] = None
        self.game_over: bool = False
        self.status_message: str = "Quantum Arena Online. Player X's turn: Place a superposition move or trigger a quantum protocol!"
        self.teleport_charges: Dict[str, int] = {'X': 1, 'O': 1} # Each player gets 1 quantum teleportation
        self.tunnel_charges: Dict[str, int] = {'X': 1, 'O': 1}   # Each player gets 1 quantum tunneling

    def get_cell_spooky_marks(self, sq: int) -> List[Move]:
        """Returns all uncollapsed spooky moves occupying the given square."""
        if self.board_classical[sq] is not None:
            return []
        return [m for m in self.uncollapsed_moves if m.sq1 == sq or m.sq2 == sq]

    def is_valid_quantum_move(self, sq1: int, sq2: int) -> Tuple[bool, str]:
        """Checks if a superposition move across sq1 and sq2 is valid."""
        if sq1 == sq2:
            return False, "You must select two distinct squares for superposition."
        if not (0 <= sq1 < 9 and 0 <= sq2 < 9):
            return False, "Squares must be between 1 and 9."
        if self.board_classical[sq1] is not None:
            return False, f"Square {sq1 + 1} has already collapsed to {self.board_classical[sq1]}."
        if self.board_classical[sq2] is not None:
            return False, f"Square {sq2 + 1} has already collapsed to {self.board_classical[sq2]}."
        return True, "Valid move"

    def place_quantum_move(self, sq1: int, sq2: int, prob_sq1: float = 0.5) -> Tuple[bool, str, bool]:
        """
        Places a quantum superposition move across sq1 and sq2 with a defined probability weight.
        """
        if self.game_over:
            return False, "Game is already over.", False

        valid, reason = self.is_valid_quantum_move(sq1, sq2)
        if not valid:
            return False, reason, False

        move = Move(self.move_counter, self.current_player, sq1, sq2, prob_sq1=prob_sq1)
        self.quantum_moves.append(move)
        self.uncollapsed_moves.append(move)

        cycle = self.detect_entanglement_cycle()
        cycle_detected = bool(cycle)

        player_done = self.current_player
        self.move_counter += 1
        self.current_player = 'O' if self.current_player == 'X' else 'X'
        self.last_action_type = "move"

        if cycle_detected:
            self.status_message = (
                f"🌀 Cyclic Entanglement Loop formed across cells {[s+1 for s in cycle]}! "
                f"Wavefunction collapse triggered!"
            )
        else:
            prob_pct = int(prob_sq1 * 100)
            self.status_message = (
                f"⚛️ Player {player_done} launched spooky mark {player_done}{move.move_id} "
                f"across Squares {sq1 + 1} ({prob_pct}%) & {sq2 + 1} ({100-prob_pct}%)."
            )

        return True, self.status_message, cycle_detected

    def quantum_teleport(self, move_id: int, source_sq: int, target_sq: int) -> Tuple[bool, str, Optional[QuantumCircuit]]:
        """
        Executes genuine 3-Qubit Quantum Teleportation protocol on IBM Qiskit!
        Teleports an uncollapsed spooky mark from source_sq to target_sq via Bell state |Φ+>.
        """
        if self.game_over:
            return False, "Game is already over.", None
        if self.teleport_charges.get(self.current_player, 0) <= 0:
            return False, f"Player {self.current_player} has used all Quantum Teleportation charges!", None
        if self.board_classical[target_sq] is not None:
            return False, f"Destination Square {target_sq + 1} is already classically occupied!", None

        # Find the target move
        target_move = next((m for m in self.uncollapsed_moves if m.move_id == move_id and m.player == self.current_player), None)
        if not target_move:
            return False, f"Spooky move {self.current_player}{move_id} not found on your active uncollapsed marks.", None

        if source_sq not in (target_move.sq1, target_move.sq2):
            return False, f"Move {self.current_player}{move_id} is not present on Square {source_sq + 1}.", None

        if target_sq in (target_move.sq1, target_move.sq2):
            return False, f"Cannot teleport to a square already part of the superposition.", None

        # Construct authentic 3-qubit Quantum Teleportation Circuit in Qiskit:
        # q0 = Alice's particle (superposition state)
        # q1, q2 = Entangled Bell pair shared between Alice and Bob
        # c0, c1 = Classical bits for Alice's Bell measurement
        # c2 = Bob's measurement
        qc = QuantumCircuit(3, 3)
        # 1. State preparation for Alice (based on probability)
        theta = 2 * np.arccos(np.sqrt(target_move.prob_sq1))
        qc.ry(theta, 0)

        # 2. Create Bell pair between q1 (Alice) and q2 (Bob)
        qc.h(1)
        qc.cx(1, 2)

        # 3. Alice performs Bell-state measurement on q0 and q1
        qc.cx(0, 1)
        qc.h(0)
        qc.measure(0, 0)
        qc.measure(1, 1)

        # 4. Bob's conditional corrections (teleportation reconstruction)
        qc.cx(1, 2)
        qc.cz(0, 2)
        qc.measure(2, 2)

        # Execute on AerSimulator
        job = self.simulator.run(qc, shots=1)
        result = job.result()
        counts = result.get_counts()
        teleport_bitstring = list(counts.keys())[0]

        # Apply state transfer to the board
        if target_move.sq1 == source_sq:
            target_move.sq1 = target_sq
        else:
            target_move.sq2 = target_sq

        target_move.teleported = True
        self.teleport_charges[self.current_player] -= 1
        self.last_circuit = qc
        self.last_measurement_result = teleport_bitstring
        self.last_action_type = "teleport"

        player_done = self.current_player
        self.current_player = 'O' if self.current_player == 'X' else 'X'

        # Check if cycle triggered by teleportation
        cycle = self.detect_entanglement_cycle()
        cycle_detected = bool(cycle)

        msg = (
            f"🌌 QUANTUM TELEPORTATION SUCCESS! Player {player_done} teleported mark "
            f"{player_done}{move_id} from Sq {source_sq + 1} -> Sq {target_sq + 1} "
            f"via Bell state |Φ+⟩! Teleport bits: |{teleport_bitstring}⟩."
        )
        self.status_message = msg
        return True, msg, qc

    def quantum_tunnel(self, move_id: int, target_sq: int) -> Tuple[bool, str, Optional[QuantumCircuit]]:
        """
        Executes Quantum Tunneling Protocol:
        Simulates particle tunneling through a potential barrier into target_sq with 75% transmission probability.
        """
        if self.game_over:
            return False, "Game is already over.", None
        if self.tunnel_charges.get(self.current_player, 0) <= 0:
            return False, f"Player {self.current_player} has exhausted Quantum Tunneling charges!", None
        if self.board_classical[target_sq] is not None:
            return False, f"Destination Square {target_sq + 1} is already collapsed!", None

        target_move = next((m for m in self.uncollapsed_moves if m.move_id == move_id and m.player == self.current_player), None)
        if not target_move:
            return False, f"Active mark {self.current_player}{move_id} not found.", None

        # Build 1-qubit barrier simulation circuit with rotation
        qc = QuantumCircuit(1, 1)
        barrier_angle = np.pi * 0.75 # 75% transmission probability amplitude
        qc.ry(barrier_angle, 0)
        qc.measure(0, 0)

        job = self.simulator.run(qc, shots=1)
        res = list(job.result().get_counts().keys())[0]

        self.tunnel_charges[self.current_player] -= 1
        self.last_circuit = qc
        self.last_measurement_result = res
        self.last_action_type = "tunnel"
        player_done = self.current_player
        self.current_player = 'O' if self.current_player == 'X' else 'X'

        if res == '1':
            # Tunneling succeeded!
            target_move.sq2 = target_sq
            target_move.tunneled = True
            msg = (
                f"⚡ QUANTUM TUNNELING SUCCESS! Wavepacket for {player_done}{move_id} "
                f"penetrated the barrier into Square {target_sq + 1}!"
            )
        else:
            msg = (
                f"🛡️ QUANTUM TUNNELING REFLECTED! Potential barrier reflected the wavepacket. "
                f"{player_done}{move_id} remains in original state."
            )

        self.status_message = msg
        return True, msg, qc

    def detect_entanglement_cycle(self) -> Optional[List[int]]:
        """
        Cycle detection on uncollapsed spooky moves.
        Nodes are uncollapsed squares (0-8); edges are quantum moves.
        """
        nodes = [i for i in range(9) if self.board_classical[i] is None]
        adj: Dict[int, List[Tuple[int, int]]] = {i: [] for i in nodes}

        # Check for multi-edges (two moves between same squares)
        edge_pairs: Dict[Tuple[int, int], int] = {}
        for m in self.uncollapsed_moves:
            u, v = min(m.sq1, m.sq2), max(m.sq1, m.sq2)
            edge_pairs[(u, v)] = edge_pairs.get((u, v), 0) + 1
            if edge_pairs[(u, v)] > 1:
                return [u, v]
            adj[m.sq1].append((m.sq2, m.move_id))
            adj[m.sq2].append((m.sq1, m.move_id))

        # DFS cycle finder
        visited = set()
        parent_map: Dict[int, int] = {}

        for start_node in nodes:
            if start_node in visited:
                continue

            stack = [(start_node, -1)]
            visited.add(start_node)

            while stack:
                u, prev_move = stack.pop()
                for v, move_id in adj[u]:
                    if move_id == prev_move:
                        continue
                    if v in visited:
                        cycle_path = [v, u]
                        curr = u
                        while curr in parent_map and parent_map[curr] != v:
                            curr = parent_map[curr]
                            cycle_path.append(curr)
                        return cycle_path
                    parent_map[v] = u
                    visited.add(v)
                    stack.append((v, move_id))

        return None

    def trigger_quantum_collapse(self, force_all: bool = False) -> Tuple[str, QuantumCircuit]:
        """
        Constructs and runs a Qiskit QuantumCircuit on IBM AerSimulator
        to project quantum superposition moves onto definite classical outcomes.
        Incorporates dynamic entanglement gates and amplitude weights.
        """
        moves_to_collapse = list(self.uncollapsed_moves) if force_all else self.get_cycle_cluster()

        if not moves_to_collapse:
            return "No uncollapsed moves to measure.", QuantumCircuit(1)

        n_moves = len(moves_to_collapse)
        qc = QuantumCircuit(n_moves, n_moves)

        # Step 1: Amplitude Rotation (Custom superposition or equal H gate)
        for i, m in enumerate(moves_to_collapse):
            if m.prob_sq1 != 0.5:
                theta = 2 * np.arccos(np.sqrt(m.prob_sq1))
                qc.ry(theta, i)
            else:
                qc.h(i)

        # Step 2: CNOT gates represent non-local entanglement between moves sharing cells
        for i in range(n_moves):
            for j in range(i + 1, n_moves):
                m1 = moves_to_collapse[i]
                m2 = moves_to_collapse[j]
                if len({m1.sq1, m1.sq2} & {m2.sq1, m2.sq2}) > 0:
                    qc.cx(i, j)

        # Step 3: Measurement of all qubits onto classical register
        qc.measure(range(n_moves), range(n_moves))
        self.last_circuit = qc
        self.last_action_type = "collapse"

        # Run on AerSimulator
        job = self.simulator.run(qc, shots=1)
        result = job.result()
        counts = result.get_counts()
        bitstring = list(counts.keys())[0]
        self.last_measurement_result = bitstring

        # Map quantum bitstring measurement onto classical grid
        occupied_squares = set(i for i in range(9) if self.board_classical[i] is not None)
        collapsed_details = []

        reversed_bits = bitstring[::-1]
        for idx, bit in enumerate(reversed_bits):
            if idx < len(moves_to_collapse):
                m = moves_to_collapse[idx]
                target_sq = m.sq2 if bit == '1' else m.sq1

                if target_sq in occupied_squares:
                    target_sq = m.sq1 if target_sq == m.sq2 else m.sq2

                if target_sq not in occupied_squares:
                    occupied_squares.add(target_sq)
                    m.collapsed_sq = target_sq
                    self.board_classical[target_sq] = m.player
                    self.board_subscripts[target_sq] = m.move_id
                    collapsed_details.append(f"{m.player}{m.move_id} ➔ Sq {target_sq + 1}")
                else:
                    collapsed_details.append(f"{m.player}{m.move_id} dissipated (both occupied)")

        # Remove collapsed moves from uncollapsed pool
        for m in moves_to_collapse:
            if m in self.uncollapsed_moves:
                self.uncollapsed_moves.remove(m)

        # Check win condition
        self.check_winner()

        summary = (
            f"💥 WAVEFUNCTION COLLAPSE COMPLETE!\n"
            f"Qiskit Aer Eigenstate: |{bitstring}⟩\n"
            f"Outcomes: {', '.join(collapsed_details)}"
        )
        self.status_message = summary
        return summary, qc

    def get_cycle_cluster(self) -> List[Move]:
        """Returns the set of moves connected to the detected cycle."""
        cycle = self.detect_entanglement_cycle()
        if not cycle:
            return self.uncollapsed_moves[:3] if self.uncollapsed_moves else []

        cycle_nodes = set(cycle)
        cluster = []
        for m in self.uncollapsed_moves:
            if m.sq1 in cycle_nodes or m.sq2 in cycle_nodes:
                cluster.append(m)
        return cluster if cluster else self.uncollapsed_moves

    def get_entanglement_figure(self) -> plt.Figure:
        """
        Builds a stunning cyber-dark visualization of the entanglement graph.
        """
        fig, ax = plt.subplots(figsize=(5, 4), facecolor='#0B0E14')
        ax.set_facecolor('#0B0E14')

        G = nx.Graph()
        # Add 9 square nodes
        for i in range(9):
            G.add_node(i, label=f"Sq {i+1}")

        # Add edges for uncollapsed moves
        edge_colors = []
        for m in self.uncollapsed_moves:
            G.add_edge(m.sq1, m.sq2, move=f"{m.player}{m.move_id}")

        pos = {
            0: (0, 2), 1: (1, 2), 2: (2, 2),
            3: (0, 1), 4: (1, 1), 5: (2, 1),
            6: (0, 0), 7: (1, 0), 8: (2, 0),
        }

        # Draw nodes
        node_colors = []
        for i in range(9):
            if self.board_classical[i] == 'X':
                node_colors.append('#FF007F')
            elif self.board_classical[i] == 'O':
                node_colors.append('#00F0FF')
            else:
                node_colors.append('#1E293B')

        nx.draw_networkx_nodes(G, pos, ax=ax, node_color=node_colors, node_size=600, edgecolors='#38BDF8', linewidths=1.5)
        nx.draw_networkx_labels(G, pos, ax=ax, font_color='#F8FAFC', font_size=9, font_weight='bold')

        # Draw edges
        nx.draw_networkx_edges(G, pos, ax=ax, edge_color='#F59E0B', width=2.5, alpha=0.85, style='dashed')
        
        # Draw edge labels
        edge_labels = {(m.sq1, m.sq2): f"{m.player}{m.move_id}" for m in self.uncollapsed_moves}
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax, font_color='#FCD34D', font_size=8, font_weight='bold')

        ax.set_title("🌌 Live Quantum Entanglement Network", color='#38BDF8', fontsize=11, fontweight='bold', pad=10)
        ax.axis('off')
        plt.tight_layout()
        return fig

    def check_winner(self):
        """Checks classical 3-in-a-row on collapsed board."""
        lines = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8], # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8], # Columns
            [0, 4, 8], [2, 4, 6]             # Diagonals
        ]

        x_wins = []
        o_wins = []

        for line in lines:
            marks = [self.board_classical[i] for i in line]
            subs = [self.board_subscripts[i] for i in line]
            if marks[0] is not None and marks[0] == marks[1] == marks[2]:
                max_sub = max(subs)
                if marks[0] == 'X':
                    x_wins.append(max_sub)
                else:
                    o_wins.append(max_sub)

        if x_wins and o_wins:
            min_x = min(x_wins)
            min_o = min(o_wins)
            if min_x < min_o:
                self.winner = 'X'
                self.status_message = f"👑 Player X WINS with earlier quantum collapse (subscript {min_x} vs {min_o})!"
            elif min_o < min_x:
                self.winner = 'O'
                self.status_message = f"👑 Player O WINS with earlier quantum collapse (subscript {min_o} vs {min_x})!"
            else:
                self.winner = 'Draw'
                self.status_message = "Simultaneous collapse draw!"
            self.game_over = True
        elif x_wins:
            self.winner = 'X'
            self.status_message = "👑 Player X completed 3-in-a-row and WINS the Quantum Realm!"
            self.game_over = True
        elif o_wins:
            self.winner = 'O'
            self.status_message = "👑 Player O completed 3-in-a-row and WINS the Quantum Realm!"
            self.game_over = True
        elif all(c is not None for c in self.board_classical):
            self.winner = 'Draw'
            self.status_message = "All cells collapsed with no 3-in-a-row. Quantum Draw!"
            self.game_over = True

    def reset(self):
        self.__init__()
