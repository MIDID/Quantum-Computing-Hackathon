# Qiskit Fall Fest 2026 — Project Submission Template

## Project Title
**Quantum Tic-Tac-Toe: Superposition, Entanglement & Wavefunction Collapse**

---

### Project Metadata
- **Project Title:** Quantum Tic-Tac-Toe: Gamifying Quantum Mechanics
- **Team Name:** Quantum Pioneers
- **Track:** Track 2: Quantum Education & Games
- **Date Submitted:** October 10, 2026
- **Challenge Prompt:** Quantum Games & Interactive Puzzles — Gamifying Quantum Mechanics
- **Additional Frameworks & Tools:** IBM Qiskit 2.5, Qiskit Aer 0.17, Streamlit, Matplotlib, NetworkX, NumPy

---

### Team Members (Max 4 members)

| Name | Email | GitHub Username |
| --- | --- | --- |
| Jeswin Jerard (Lead) | jeswinjerard@gmail.com | MIDID |

---

## 1. Project Overview & Motivation

### Summary & Motivation
Quantum mechanics introduces counter-intuitive phenomena: particles can exist in superpositions of states, become entangled across distances, and collapse into definite outcomes upon measurement. Standard pedagogical introductions to quantum theory often rely heavily on abstract linear algebra and Dirac bra-ket notation, which can intimidate students and enthusiasts.

Our mission is to build a playable game where **quantum phenomena are core gameplay mechanics rather than cosmetic themes**. Quantum Tic-Tac-Toe bridges this gap by turning the classical 3×3 grid into a macroscopic quantum arena.

### What the problem / game is
In classical Tic-Tac-Toe, each move is deterministically placed into a single cell, quickly leading to trivial draws. In **Quantum Tic-Tac-Toe**:
1. Every move is placed in an equal quantum superposition across **two separate cells** (e.g., $X_1$ on cells 1 and 5).
2. As moves overlap across cells, they form non-local **quantum entanglements**.
3. When an entanglement loop (cycle) forms across cells, the superposition cannot be sustained.
4. **IBM Qiskit** simulates the quantum wavefunction collapse, projecting entangled moves onto definite classical outcomes via state measurement!
5. This introduces strategic depth, probability management, and intuitive quantum education.

---

## 2. Quantum Architecture & Mechanics

### Core Quantum Principles Used
- **Superposition ($\frac{1}{\sqrt{2}}(|0\rangle + |1\rangle)$):** Each turn, a spooky mark is placed across two cells $S_A$ and $S_B$. The particle's position is in an undetermined state until observation.
- **Entanglement (Bell States & GHZ-like correlations):** When multiple moves share squares, their fates are entangled. If Move 1 collapses to Square $A$, Move 2 is physically excluded and forced to collapse to Square $B$.
- **Wavefunction Collapse & Measurement:** An entanglement cycle triggers a quantum measurement using `qiskit_aer.AerSimulator`, executing projective measurements $\langle M | \psi \rangle$.

### How Quantum Mechanics are Integrated
The quantum logic is strictly enforced via real quantum circuits built using **IBM Qiskit**:
- For each uncollapsed move in an entangled cluster, a qubit $q_i$ is allocated.
- A **Hadamard gate ($H$)** puts each qubit into equal superposition.
- **Controlled-NOT ($CX$) gates** entangle qubits corresponding to moves that contest the same physical board squares.
- **Measurement operators** measure the register into classical bits, dictating which squares receive classical marks.

### Circuit Details
- **Number of Qubits:** Dynamic ($N$ qubits, where $N$ is the number of entangled moves in the cycle cluster, typically 2 to 6 qubits).
- **Quantum Gates Used:** `H` (Hadamard), `CX` (Controlled-NOT), `Measure`.
- **Quantum Circuit Diagram:**
```text
     ┌───┐          ┌─┐   
q_0: ┤ H ├──■───────┤M├───
     ├───┤┌─┴─┐     └╥┘┌─┐
q_1: ┤ H ├┤ X ├──■───╫─┤M├
     ├───┤└───┘┌─┴─┐ ║ └╥┘
q_2: ┤ H ├─────┤ X ├─╫──╫─
     └───┘     └───┘ ║  ║ 
c: 3/════════════════╩══╩═
                     0  1 
```

---

## 3. Repository Structure & How to Run

### Project Structure
```text
├── .github/
│   └── workflows/
│       └── ci.yml
├── notebooks/
│   └── quantum_tictactoe_demo.ipynb
├── src/
│   ├── app.py                     # Streamlit Interactive Web Application
│   ├── quantum_engine.py          # Core Qiskit circuit & game mechanics
│   └── quantum_tictactoe_cli.py   # Terminal CLI Game
├── .gitignore
├── CODE_OF_CONDUCT.md
├── LICENSE
├── README.md                      # Project documentation and submission details
└── requirements.txt               # Dependencies (Qiskit, Aer, Streamlit, etc.)
```

### Installation & Run Instructions

#### 1. Clone Repository & Create Virtual Environment
```bash
git clone https://github.com/MIDID/quantum-tictactoe.git
cd quantum-tictactoe
python -m venv .venv

# On Windows (PowerShell):
.\.venv\Scripts\Activate.ps1

# On macOS/Linux:
source .venv/bin/activate
```

#### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 3. Run the Project / Game

##### Option A: Streamlit Interactive Web Application (Recommended)
```bash
streamlit run src/app.py
```

##### Option B: Terminal CLI Game
```bash
python src/quantum_tictactoe_cli.py
```

##### Option C: Interactive Jupyter Notebook
```bash
jupyter notebook notebooks/quantum_tictactoe_demo.ipynb
```

---

## 4. Implementation Walkthrough & Live Demo

### Walkthrough of Gameplay / Core Logic Routine
1. **Game Initialization:** `QuantumTicTacToe()` initializes an empty 9-cell classical board and empty quantum history.
2. **Superposition Turn:** Player 1 picks two squares (e.g., Sq 1 & Sq 5). A spooky mark $X_1$ is registered.
3. **Graph Entanglement Tracking:** As players place overlapping moves, an undirected multigraph tracks edges between cells.
4. **Cycle Detection:** A cycle detection algorithm monitors loops (e.g., $1 \leftrightarrow 2 \leftrightarrow 3 \leftrightarrow 1$).
5. **Qiskit Circuit Assembly:**
   - Qubits are assigned to each active move.
   - $H$ gates establish superposition.
   - $CX$ entangling gates enforce anti-correlation across contested cells.
6. **Execution on Qiskit Aer:** `AerSimulator().run(qc, shots=1)` samples the collapsed eigenstate.
7. **Scoring:** The classical board is checked for 3-in-a-row. If simultaneous lines occur from the same collapse, Allan Goff's quantum subscript rule decides the winner (earlier move wins).

---

## 5. Classical vs. Quantum Comparison

| Feature | Classical Tic-Tac-Toe | Quantum Tic-Tac-Toe (Qiskit) |
| --- | --- | --- |
| **Move Space** | Deterministic single square ($|0\rangle$ or $|1\rangle$) | Superposition of two squares $\frac{1}{\sqrt{2}}(\|A\rangle + \|B\rangle)$ |
| **Inter-cell Relation** | Independent classical cells | Non-local entanglement across multiple squares |
| **Collapse Dynamic** | None (instant classical state) | Wavefunction collapse triggered by entanglement loops |
| **Outcome Nature** | Purely deterministic (always ends in draw with optimal play) | Probabilistic quantum measurement with strategic depth |
| **Scoring** | Binary win/loss/draw | Simultaneous quantum win resolution via subscript precedence |

---

## 6. Performance, Results & Limitations

### Simulation & Observations
- Execution on IBM Qiskit's `AerSimulator` takes $< 15$ ms for standard 2–6 qubit entanglement clusters, providing instant real-time gameplay feedback.
- Superposition moves allow players to contest up to 4 squares simultaneously, delaying definite commitments until an entanglement collapse forces resolution.

### Critical Reflection & Limitations
- **Current Limitation:** Simulating large arbitrary graphs on hardware quantum backends incurs queue wait times (hence local AerSimulator is utilized for responsive gaming).
- **Future Work:** Integration with `qiskit-ibm-runtime` Sampler on actual IBM Falcon/Heron quantum hardware, and expanding the board to 4×4 or 3D Quantum Tic-Tac-Toe.

---

## 7. References & Acknowledgments
- **Allan Goff (2006):** *Quantum Tic-Tac-Toe, Spooky-Coins, and the Quantum State*, American Journal of Physics.
- **IBM Quantum & Qiskit Documentation:** [https://docs.quantum.ibm.com/](https://docs.quantum.ibm.com/)
- **Qiskit Fall Fest 2026 Community & Organizers.**
