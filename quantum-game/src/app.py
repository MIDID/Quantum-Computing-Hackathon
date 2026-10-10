import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import streamlit as st
from quantum_engine import QuantumTicTacToe
import matplotlib.pyplot as plt

# Page configuration
st.set_page_config(
    page_title="Quantum Tic-Tac-Toe | Qiskit Cyber Arena",
    page_icon="⚛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom High-Tech Cyber-Quantum Styling
st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@600;800;900&family=Rajdhani:wght@500;600;700&family=Inter:wght@400;500;700&display=swap" rel="stylesheet">

<style>
    /* Global Background & Typography */
    .stApp {
        background: radial-gradient(circle at 20% 20%, #0d1527 0%, #07090e 100%);
        font-family: 'Inter', sans-serif;
        color: #E2E8F0;
    }

    /* Titles */
    .hero-title {
        font-family: 'Orbitron', monospace;
        font-size: 2.8rem;
        font-weight: 900;
        text-align: center;
        letter-spacing: 2px;
        background: linear-gradient(135deg, #00F0FF 0%, #7928CA 50%, #FF007F 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.1rem;
        text-shadow: 0 0 35px rgba(0, 240, 255, 0.4);
    }
    .hero-sub {
        font-family: 'Rajdhani', sans-serif;
        font-size: 1.25rem;
        font-weight: 600;
        text-align: center;
        color: #94A3B8;
        letter-spacing: 1px;
        margin-bottom: 1.8rem;
    }

    /* Player Status Badges */
    .badge-turn-x {
        font-family: 'Orbitron', monospace;
        background: linear-gradient(90deg, rgba(255, 0, 127, 0.25), rgba(255, 65, 108, 0.4));
        border: 2px solid #FF007F;
        box-shadow: 0 0 15px rgba(255, 0, 127, 0.5);
        color: #FFF;
        padding: 8px 18px;
        border-radius: 30px;
        font-weight: 800;
        display: inline-block;
        letter-spacing: 1px;
    }
    .badge-turn-o {
        font-family: 'Orbitron', monospace;
        background: linear-gradient(90deg, rgba(0, 240, 255, 0.25), rgba(0, 114, 255, 0.4));
        border: 2px solid #00F0FF;
        box-shadow: 0 0 15px rgba(0, 240, 255, 0.5);
        color: #FFF;
        padding: 8px 18px;
        border-radius: 30px;
        font-weight: 800;
        display: inline-block;
        letter-spacing: 1px;
    }

    /* Quantum Containment Chambers (3x3 Cells) */
    .chamber-card {
        background: rgba(15, 23, 42, 0.75);
        border: 2px solid #1E293B;
        border-radius: 16px;
        padding: 16px 12px;
        min-height: 125px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        align-items: center;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
        backdrop-filter: blur(10px);
        position: relative;
        overflow: hidden;
    }
    .chamber-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0; height: 3px;
        background: linear-gradient(90deg, transparent, rgba(56, 189, 248, 0.3), transparent);
    }
    .chamber-card:hover {
        border-color: #38BDF8;
        box-shadow: 0 0 20px rgba(56, 189, 248, 0.25);
        transform: translateY(-2px);
    }
    .chamber-selected {
        border-color: #00F0FF !important;
        background: rgba(0, 240, 255, 0.12) !important;
        box-shadow: 0 0 25px rgba(0, 240, 255, 0.5) !important;
        transform: scale(1.02);
    }

    /* Classical Collapsed Marks */
    .classical-glyph-x {
        font-family: 'Orbitron', monospace;
        font-size: 2.8rem;
        font-weight: 900;
        color: #FF007F;
        text-shadow: 0 0 20px rgba(255, 0, 127, 0.8), 0 0 40px rgba(255, 0, 127, 0.4);
        line-height: 1;
        animation: pulse-glow 2s infinite alternate;
    }
    .classical-glyph-o {
        font-family: 'Orbitron', monospace;
        font-size: 2.8rem;
        font-weight: 900;
        color: #00F0FF;
        text-shadow: 0 0 20px rgba(0, 240, 255, 0.8), 0 0 40px rgba(0, 240, 255, 0.4);
        line-height: 1;
        animation: pulse-glow 2s infinite alternate;
    }

    /* Spooky Quantum Marks */
    .spooky-particle {
        font-family: 'Rajdhani', sans-serif;
        font-size: 1rem;
        font-weight: 700;
        color: #FCD34D;
        background: rgba(245, 158, 11, 0.15);
        border: 1px solid rgba(245, 158, 11, 0.4);
        padding: 3px 8px;
        border-radius: 8px;
        margin: 2px;
        display: inline-block;
        box-shadow: 0 0 8px rgba(245, 158, 11, 0.2);
    }
    .spooky-particle.teleported {
        border-color: #A855F7;
        color: #C084FC;
        background: rgba(168, 85, 247, 0.2);
    }

    /* Chamber Subtitles */
    .chamber-header {
        font-family: 'Orbitron', monospace;
        font-size: 0.72rem;
        font-weight: 700;
        color: #64748B;
        letter-spacing: 1px;
    }

    /* Glass Panels */
    .glass-panel {
        background: rgba(15, 23, 42, 0.65);
        border: 1px solid rgba(56, 189, 248, 0.2);
        border-radius: 16px;
        padding: 20px;
        backdrop-filter: blur(12px);
        margin-bottom: 20px;
    }

    /* Audio Sound Trigger */
    @keyframes pulse-glow {
        0% { filter: drop-shadow(0 0 5px currentColor); }
        100% { filter: drop-shadow(0 0 15px currentColor); }
    }
</style>

<!-- Audio Synthesizer Hook -->
<script>
    function playLaserSound() {
        try {
            const ctx = new (window.AudioContext || window.webkitAudioContext)();
            const osc = ctx.createOscillator();
            const gain = ctx.createGain();
            osc.type = 'sine';
            osc.frequency.setValueAtTime(800, ctx.currentTime);
            osc.frequency.exponentialRampToValueAtTime(200, ctx.currentTime + 0.15);
            gain.gain.setValueAtTime(0.1, ctx.currentTime);
            gain.gain.linearRampToValueAtTime(0, ctx.currentTime + 0.15);
            osc.connect(gain);
            gain.connect(ctx.destination);
            osc.start();
            osc.stop(ctx.currentTime + 0.15);
        } catch(e) {}
    }
</script>
""", unsafe_allow_html=True)

# Initialize Session State
if "game" not in st.session_state:
    st.session_state.game = QuantumTicTacToe()
    st.session_state.selected_squares = []

game: QuantumTicTacToe = st.session_state.game

# Hero Header
st.markdown('<div class="hero-title">⚛️ QUANTUM TIC-TAC-TOE</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">ENTANGLEMENT • SUPERPOSITION AMPLITUDES • 3-QUBIT TELEPORTATION • QISKIT AER COLLAPSE</div>', unsafe_allow_html=True)

# Layout Columns
col_arena, col_quantum = st.columns([1.25, 1], gap="large")

with col_arena:
    # Status Banner
    player_badge = (
        '<span class="badge-turn-x">PLAYER X (PLASMA)</span>'
        if game.current_player == 'X'
        else '<span class="badge-turn-o">PLAYER O (CYAN)</span>'
    )

    t_charge = game.teleport_charges[game.current_player]
    tun_charge = game.tunnel_charges[game.current_player]

    st.markdown(
        f"""
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 12px;">
            <div><span style="color:#94A3B8; font-weight:600;">ACTIVE TURN:</span> {player_badge}</div>
            <div style="font-family:'Rajdhani'; font-weight:700; font-size:1.1rem; color:#38BDF8;">
                🌌 Teleport Charges: <span style="color:#FFF;">{t_charge}</span> | ⚡ Tunnel Charges: <span style="color:#FFF;">{tun_charge}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    if game.game_over:
        st.balloons()
        st.success(f"🏆 {game.status_message}")
    else:
        st.info(f"💡 {game.status_message}")

    # Guide bar
    selected = st.session_state.selected_squares
    if len(selected) == 0:
        step_note = "⚡ **Action:** Click **any 2 chambers** on the grid below to create your quantum superposition."
    elif len(selected) == 1:
        step_note = f"⚡ **Chamber {selected[0] + 1} locked!** Click a **2nd chamber** to complete the superposition pair."
    else:
        step_note = f"✅ **Ready!** Pair locked across **Chamber {selected[0] + 1} & Chamber {selected[1] + 1}**. Choose your Quantum Protocol below."

    st.markdown(f"<div style='background:rgba(30, 41, 59, 0.7); border-left:4px solid #38BDF8; padding:10px 14px; border-radius:8px; margin-bottom:15px; font-size:0.95rem;'>{step_note}</div>", unsafe_allow_html=True)

    # 3x3 Grid of Futuristic Chambers
    for row in range(3):
        cols = st.columns(3)
        for col in range(3):
            sq_idx = row * 3 + col
            with cols[col]:
                classical = game.board_classical[sq_idx]
                if classical is not None:
                    sub = game.board_subscripts[sq_idx]
                    css_class = "classical-glyph-x" if classical == 'X' else "classical-glyph-o"
                    st.markdown(
                        f"""
                        <div class="chamber-card" style="border-color: {'#FF007F' if classical=='X' else '#00F0FF'};">
                            <span class="chamber-header">CHAMBER 0{sq_idx + 1} [COLLAPSED]</span>
                            <div class="{css_class}">{classical}<sub>{sub}</sub></div>
                            <span style="font-size:0.75rem; color:#64748B; font-weight:600;">EIGENSTATE STABLE</span>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                else:
                    spookies = game.get_cell_spooky_marks(sq_idx)
                    spooky_pills = "".join([
                        f'<span class="spooky-particle{" teleported" if m.teleported else ""}">{m.player}<sub>{m.move_id}</sub></span>'
                        for m in spookies
                    ])
                    is_sel = sq_idx in st.session_state.selected_squares
                    sel_class = " chamber-selected" if is_sel else ""

                    st.markdown(
                        f"""
                        <div class="chamber-card{sel_class}">
                            <div style="width:100%; display:flex; justify-content:space-between;">
                                <span class="chamber-header">CHAMBER 0{sq_idx + 1}</span>
                                <span style="font-size:0.7rem; color:{'#00F0FF' if is_sel else '#475569'}; font-weight:700;">{'LOCKED' if is_sel else 'EMPTY'}</span>
                            </div>
                            <div style="min-height:36px; display:flex; flex-wrap:wrap; align-items:center; justify-content:center;">
                                {spooky_pills if spooky_pills else '<span style="color:#475569; font-size:0.85rem; font-style:italic;">No superposition</span>'}
                            </div>
                            <span style="font-size:0.75rem; color:#94A3B8;">Select to Entangle</span>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    if not game.game_over:
                        btn_txt = f"✦ SELECTED ✦" if is_sel else f"⚡ Select Pod {sq_idx + 1}"
                        if st.button(btn_txt, key=f"pod_{sq_idx}", use_container_width=True):
                            if sq_idx in st.session_state.selected_squares:
                                st.session_state.selected_squares.remove(sq_idx)
                            else:
                                if len(st.session_state.selected_squares) >= 2:
                                    st.session_state.selected_squares.pop(0)
                                st.session_state.selected_squares.append(sq_idx)
                            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # ACTION DASHBOARD TABS
    tab_super, tab_teleport, tab_tunnel, tab_collapse = st.tabs([
        "🌀 Superposition Launch",
        "🌌 Quantum Teleportation",
        "⚡ Barrier Tunneling",
        "💥 Wavefunction Collapse"
    ])

    with tab_super:
        st.markdown("##### 🌀 Launch Superposition Particle Across 2 Chambers")
        prob_ratio = st.slider(
            "Quantum Probability Amplitude (|Chamber A⟩ vs |Chamber B⟩)",
            min_value=10, max_value=90, value=50, step=10,
            help="Choose the probability distribution. In pure quantum mechanics, this rotates the qubit vector via Ry(θ)!"
        )
        st.caption(f"State Vector: |ψ⟩ = √{prob_ratio/100:.2f}|Chamber A⟩ + √{(100-prob_ratio)/100:.2f}|Chamber B⟩")

        c_launch, c_clear = st.columns([2, 1])
        with c_launch:
            ready = (len(selected) == 2 and not game.game_over)
            if st.button("🚀 Fire Quantum Superposition", disabled=not ready, use_container_width=True, type="primary"):
                success, msg, cycle_found = game.place_quantum_move(selected[0], selected[1], prob_sq1=(prob_ratio / 100.0))
                st.session_state.selected_squares = []
                if success and cycle_found:
                    game.trigger_quantum_collapse()
                st.rerun()
            if not ready and not game.game_over:
                st.caption("Please select 2 chambers above to launch.")
        with c_clear:
            if st.button("Clear Selection", use_container_width=True):
                st.session_state.selected_squares = []
                st.rerun()

    with tab_teleport:
        st.markdown("##### 🌌 Authentic 3-Qubit Quantum Teleportation Protocol")
        st.caption("Teleports an uncollapsed particle branch from one chamber to a new empty chamber using a Bell State |Φ+⟩ and classical feedforward!")

        my_moves = [m for m in game.uncollapsed_moves if m.player == game.current_player]
        if not my_moves:
            st.warning(f"Player {game.current_player} has no uncollapsed marks on the board to teleport.")
        else:
            m_options = {f"{m.player}{m.move_id} (across Sq {m.sq1+1} & Sq {m.sq2+1})": m for m in my_moves}
            sel_move_label = st.selectbox("Select Spooky Mark to Teleport:", list(m_options.keys()))
            chosen_move = m_options[sel_move_label]

            col_src, col_dest = st.columns(2)
            with col_src:
                src_pod = st.selectbox("Source Chamber (Alice):", [chosen_move.sq1 + 1, chosen_move.sq2 + 1])
            with col_dest:
                avail_dest = [i + 1 for i in range(9) if game.board_classical[i] is None and i != chosen_move.sq1 and i != chosen_move.sq2]
                dest_pod = st.selectbox("Destination Chamber (Bob):", avail_dest if avail_dest else [1])

            can_teleport = (game.teleport_charges[game.current_player] > 0 and len(avail_dest) > 0 and not game.game_over)
            if st.button("⚡ Execute Qiskit Teleportation Circuit", disabled=not can_teleport, use_container_width=True):
                ok, tmsg, qc = game.quantum_teleport(chosen_move.move_id, src_pod - 1, dest_pod - 1)
                st.session_state.selected_squares = []
                st.rerun()

    with tab_tunnel:
        st.markdown("##### ⚡ Quantum Barrier Tunneling Protocol")
        st.caption("Simulates barrier penetration with 75% transmission probability. A wavepacket penetrates through the potential barrier to a new chamber!")
        my_moves = [m for m in game.uncollapsed_moves if m.player == game.current_player]
        if not my_moves:
            st.warning("No active marks available to tunnel.")
        else:
            m_options_t = {f"{m.player}{m.move_id}": m for m in my_moves}
            sel_m_t = st.selectbox("Select Mark to Tunnel:", list(m_options_t.keys()), key="tunnel_m")
            chosen_m_t = m_options_t[sel_m_t]
            avail_dest_t = [i + 1 for i in range(9) if game.board_classical[i] is None and i not in (chosen_m_t.sq1, chosen_m_t.sq2)]
            dest_pod_t = st.selectbox("Target Chamber to Infiltrate:", avail_dest_t if avail_dest_t else [1], key="tunnel_dest")

            can_tunnel = (game.tunnel_charges[game.current_player] > 0 and len(avail_dest_t) > 0 and not game.game_over)
            if st.button("🌀 Attempt Quantum Tunneling", disabled=not can_tunnel, use_container_width=True):
                ok, tmsg, qc = game.quantum_tunnel(chosen_m_t.move_id, dest_pod_t - 1)
                st.session_state.selected_squares = []
                st.rerun()

    with tab_collapse:
        st.markdown("##### 💥 Trigger Wavefunction Measurement")
        st.caption("Executes projective measurements ⟨M|ψ⟩ on the IBM AerSimulator, collapsing spooky marks into definitive classical states.")
        c_force, c_res = st.columns(2)
        with c_force:
            can_force = (len(game.uncollapsed_moves) > 0 and not game.game_over)
            if st.button("⚡ Force Measurement Collapse", disabled=not can_force, use_container_width=True, type="primary"):
                game.trigger_quantum_collapse(force_all=True)
                st.session_state.selected_squares = []
                st.rerun()
        with c_res:
            if st.button("🔄 Reset Quantum Board", use_container_width=True):
                game.reset()
                st.session_state.selected_squares = []
                st.rerun()

with col_quantum:
    st.markdown("### 🔬 Live Quantum Instrumentation")

    # Live Entanglement Network Graph
    with st.expander("🌌 Live Entanglement Network Graph", expanded=True):
        if len(game.uncollapsed_moves) > 0:
            fig_graph = game.get_entanglement_figure()
            st.pyplot(fig_graph)
            plt.close(fig_graph)
        else:
            st.info("No active entanglement edges yet. Place moves to observe the quantum graph.")

    # IBM Qiskit Quantum Circuit
    with st.expander("⚡ Latest Qiskit Quantum Circuit", expanded=True):
        if game.last_circuit is not None:
            st.caption(f"Protocol: **{game.last_action_type.upper()}** | Evaluated on IBM AerSimulator")
            fig_qc = game.last_circuit.draw(output='mpl', style='iqp')
            st.pyplot(fig_qc)
            plt.close(fig_qc)
            if game.last_measurement_result:
                st.success(f"**Measured Classical Bitstring:** `|{game.last_measurement_result}⟩`")
        else:
            st.info("Circuit will appear upon move, teleportation, or collapse.")

    # Quantum Physics Rules
    with st.expander("📚 Quantum Rules & Science Explainer"):
        st.markdown("""
        - **Superposition:** Particles do not have definite classical coordinates until measured.
        - **Quantum Teleportation:** Teleports unknown quantum state using EPR pairs ($|\\Phi^+\\rangle$) and classical communication without moving physical particles!
        - **Quantum Tunneling:** Finite barrier penetration described by Schrödinger wavepackets.
        - **Allan Goff Collapses:** Simultaneous 3-in-a-row resolved by earliest quantum subscript.
        """)
