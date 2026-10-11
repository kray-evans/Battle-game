import random
import streamlit as st

# Cấu hình trang Streamlit
st.set_page_config(
    page_title="JoJo: Bizarre Battle", page_icon="⭐", layout="centered"
)

# Khởi tạo trạng thái trò chơi (Game State)
if "initialized" not in st.session_state:
  st.session_state.p1_hp = 100
  st.session_state.p2_hp = 100
  st.session_state.p1_energy = 0
  st.session_state.p2_energy = 0
  st.session_state.game_over = False
  st.session_state.winner = ""
  st.session_state.log = (
      "Trận chiến bắt đầu! Jotaro Kujo đối đầu với DIO tại Cairo."
  )
  st.session_state.initialized = True


def reset_game():
  st.session_state.p1_hp = 100
  st.session_state.p2_hp = 100
  st.session_state.p1_energy = 0
  st.session_state.p2_energy = 0
  st.session_state.game_over = False
  st.session_state.winner = ""
  st.session_state.log = "Trận đấu mới bắt đầu! ORA ORA vs MUDA MUDA!"


# Giao diện chính
st.title("⭐ JoJo's Bizarre Adventure: Stand Battle ⭐")
st.markdown("---")

# Hiển thị thông số 2 nhân vật
col1, col2 = st.columns(2)

with col1:
  st.subheader("Jotaro Kujo")
  st.caption("Stand: Star Platinum")
  st.metric(label="Máu (HP)", value=f"{st.session_state.p1_hp}/100")
  st.progress(max(0, st.session_state.p1_hp) / 100)
  st.write(f"⚡ Năng lượng Stand: {st.session_state.p1_energy}/100")

with col2:
  st.subheader("DIO")
  st.caption("Stand: The World")
  st.metric(label="Máu (HP)", value=f"{st.session_
