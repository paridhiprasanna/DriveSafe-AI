import streamlit as st
import pandas as pd
import sqlite3
import plotly.graph_objects as go
from datetime import datetime

DB_NAME = "drivesafe.db"

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="DriveSafe AI – Driver Monitoring",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- GLOBAL STYLES ----------
st.markdown("""
<style>
:root{
  --bg:#05070d;
  --bg-2:#0a0f1c;
  --panel: rgba(255,255,255,0.04);
  --panel-border: rgba(255,255,255,0.08);
  --text:#e6ecf5;
  --muted:#8a93a6;
  --safe:#00ffa3;
  --warn:#ffd84d;
  --danger:#ff4d6d;
  --accent:#22d3ee;
}

html, body, [class*="css"], .stApp{
  background: radial-gradient(1200px 600px at 10% -10%, #0d1b3a 0%, transparent 60%),
              radial-gradient(900px 500px at 100% 0%, #15123a 0%, transparent 55%),
              linear-gradient(180deg, #05070d 0%, #03050a 100%) !important;
  color: var(--text);
  font-family: 'Inter', -apple-system, system-ui, sans-serif;
}

/* Hide Streamlit chrome */
#MainMenu, footer {visibility: hidden;}
.block-container{
    padding-top: 5rem !important;
    padding-left: 2rem;
    padding-right: 2rem;
    padding-bottom: 3rem;
    max-width: 100%;
}

/* Sidebar */
section[data-testid="stSidebar"]{
    width:280px !important;
    background:#06080f !important;
    border-right:1px solid rgba(255,255,255,0.08);
}
section[data-testid="stSidebar"] .stRadio label{
  color: var(--muted); font-weight: 500; padding: 10px 12px; border-radius: 10px;
  transition: all .2s ease;
}
section[data-testid="stSidebar"] .stRadio label:hover{
  background: rgba(34,211,238,0.06); color: var(--text);
}

/* Top Navbar */
.navbar{
    display:flex;
    justify-content:space-between;
    align-items:center;
    padding:14px 22px;
    margin:0 0 22px 0;      /* remove left margin */
    width:100%;             /* take full container width */
    background:var(--panel);
    border:1px solid var(--panel-border);
    border-radius:16px;
    backdrop-filter:blur(14px);
    box-sizing:border-box;
}
.brand{display:flex; align-items:center; gap:14px;}
.brand-logo{
  width:40px;height:40px;border-radius:12px;
  background: linear-gradient(135deg, var(--accent), #6366f1);
  display:flex;align-items:center;justify-content:center;font-size:20px;
  box-shadow: 0 0 24px rgba(34,211,238,0.35);
}
.brand-title{
    font-size:15px;
    font-weight:700;
}

.brand-sub{
    font-size:11px;
}


.live-pill{
  display:flex;align-items:center;gap:8px;
  background: rgba(0,255,163,0.08); color: var(--safe);
  border:1px solid rgba(0,255,163,0.25);
  padding:6px 12px;border-radius:999px;font-size:12px;font-weight:600;
}
.live-dot{
  width:8px;height:8px;border-radius:50%;background:var(--safe);
  box-shadow:0 0 0 0 rgba(0,255,163,.7);
  animation: pulse 1.6s infinite;
}
@keyframes pulse{
  0%{box-shadow:0 0 0 0 rgba(0,255,163,.6);}
  70%{box-shadow:0 0 0 10px rgba(0,255,163,0);}
  100%{box-shadow:0 0 0 0 rgba(0,255,163,0);}
}

/* Glass card */
.card{
  background: var(--panel);
  border:1px solid var(--panel-border);
  border-radius:18px; padding:20px 22px;
  backdrop-filter: blur(14px);
  transition: transform .25s ease, border-color .25s ease;
  height:100%;
}
.card:hover{ transform: translateY(-2px); border-color: rgba(34,211,238,0.25);}
.card-label{color:var(--muted); font-size:12px; text-transform:uppercase; letter-spacing:1.2px; font-weight:600;}
.card-value{font-size:34px; font-weight:700; margin-top:6px; line-height:1.1;}
.card-sub{color:var(--muted); font-size:12px; margin-top:6px;}
.card-icon{
  width:38px;height:38px;border-radius:10px;
  display:flex;align-items:center;justify-content:center;font-size:18px;
  background: rgba(34,211,238,0.1); color: var(--accent);
}
.card-head{display:flex;justify-content:space-between;align-items:flex-start;}

.badge{display:inline-block;padding:4px 10px;border-radius:999px;font-size:11px;font-weight:700;letter-spacing:.5px;}
.badge-safe{background:rgba(0,255,163,0.12);color:var(--safe);border:1px solid rgba(0,255,163,0.3);}
.badge-warn{background:rgba(255,216,77,0.12);color:var(--warn);border:1px solid rgba(255,216,77,0.3);}
.badge-danger{background:rgba(255,77,109,0.12);color:var(--danger);border:1px solid rgba(255,77,109,0.3);}

.section-title{font-size:14px;font-weight:600;color:var(--muted);
  text-transform:uppercase;letter-spacing:1.4px;margin: 28px 0 12px;}

.summary-row{display:flex;justify-content:space-between;padding:10px 0;
  border-bottom:1px dashed rgba(255,255,255,0.06);font-size:14px;}
.summary-row:last-child{border-bottom:none;}
.summary-key{color:var(--muted);}
.summary-val{color:var(--text);font-weight:600;}

.alert-banner{
    display:flex;
    align-items:center;
    gap:12px;
    width:100%;
    box-sizing:border-box;
    background:linear-gradient(90deg, rgba(255,77,109,0.15), rgba(255,77,109,0.02));
    border:1px solid rgba(255,77,109,0.35);
    padding:14px 18px;
    border-radius:16px;
    margin-bottom:22px;
}
@keyframes fadeIn{from{opacity:0;transform:translateY(-4px);}to{opacity:1;transform:none;}}

div[data-testid="stDataFrame"]{border-radius:14px;overflow:hidden;border:1px solid var(--panel-border);}
[data-testid="stAppViewContainer"]{
    overflow-x:hidden;
}

[data-testid="stMain"]{
    padding-left:1rem;
}
</style>
""", unsafe_allow_html=True)

# ---------- DATA ----------
@st.cache_data(ttl=10)
def load_data():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM sessions", conn)
    conn.close()
    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"Could not load database: {e}")
    st.stop()

if df.empty:
    st.warning("No session data found.")
    st.stop()

# ---------- DERIVED METRICS ----------
avg_risk = float(df["risk_score"].mean())
safety_score = max(0, 100 - int(avg_risk))
max_risk = int(df["risk_score"].max())
yawns = int((df["mar"] > 0.06).sum())
distraction_pct = float(
    (df["head_pose"].isin(["Looking Left", "Looking Right"])).mean() * 100
) if "head_pose" in df else 0


if avg_risk < 30:
    drowsy_status = "Drive Safe"
    drowsy_class = "badge-safe"
elif avg_risk < 60:
    drowsy_status = "Stay Alert"
    drowsy_class = "badge-warn"
else:
    drowsy_status = "Take a Break"
    drowsy_class = "badge-danger"

# ---------- SIDEBAR ----------
with st.sidebar:
    st.markdown("""
    <div style='padding:8px 4px 24px;'>
      <div style='display:flex;align-items:center;gap:10px;'>
        <div class='brand-title' style='padding-left:10px;>
                DriveSafe AI – Driver Monitoring System🛡️</div>
        <div>
          <div style='font-weight:700;font-size:15px;'>DriveSafe AI</div>
          <div style='font-size:11px;color:var(--muted);'>v2.4 · Monitoring</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    page = st.radio(
        "Navigation",
        ["Overview", "Live Session", "Analytics", "Alerts", "History"],
        label_visibility="collapsed",
    )

    st.markdown("---")
    st.markdown(f"<div style='font-size:12px;color:var(--muted);'>Session ID</div>"
                f"<div style='font-weight:600;'>#DS-{datetime.now().strftime('%H%M%S')}</div>",
                unsafe_allow_html=True)

# ---------- NAVBAR ----------
st.markdown(f"""
<div class='navbar'>
  <div class='brand'>
    <div class='brand-logo'>🛡️</div>
    <div>
      <div class='brand-title'>DriveSafe AI </div>
      <div class='brand-sub'>Driver Monitoring system</div>
    </div>
  </div>
  <div class='live-pill'><span class='live-dot'></span> LIVE · Streaming</div>
</div>
""", unsafe_allow_html=True)

# ---------- HIGH RISK BANNER ----------
if avg_risk >= 75 or max_risk >= 75:
    st.markdown(f"""
    <div class='alert-banner'>
      <span style='font-size:22px;'>⚠️</span>
      <div>
        <div style='font-weight:700;color:var(--danger);'>HIGH RISK DETECTED</div>
        <div style='font-size:12px;color:var(--muted);'>
          Peak risk score {max_risk}/100 · {yawns} yawning events · Immediate attention advised.
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

# ---------- HELPERS ----------
def ring(value, color):
    fig = go.Figure(go.Pie(
        values=[value, 100 - value], hole=.78, sort=False,
        marker_colors=[color, "rgba(255,255,255,0.06)"],
        textinfo="none", hoverinfo="skip",
    ))
    fig.update_layout(
        showlegend=False, margin=dict(l=0, r=0, t=0, b=0),
        height=140, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        annotations=[dict(text=f"<b>{value}</b>", showarrow=False,
                          font=dict(size=24, color="#e6ecf5"))],
    )
    return fig

def risk_color(v):
    return "#00ffa3" if v < 30 else "#ffd84d" if v < 60 else "#ff4d6d"

def gradient_line(x, y, name, color):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x, y=y, mode="lines", name=name, line=dict(color=color, width=2.5, shape="spline"),
        fill="tozeroy",
        fillgradient=dict(type="vertical",
                          colorscale=[(0, "rgba(0,0,0,0)"), (1, color)]),
        hovertemplate=f"<b>{name}</b>: %{{y:.2f}}<extra></extra>",
    ))
    fig.update_layout(
        height=280, margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#8a93a6", family="Inter"),
        xaxis=dict(gridcolor="rgba(255,255,255,0.04)", showline=False),
        yaxis=dict(gridcolor="rgba(255,255,255,0.04)", showline=False),
        hoverlabel=dict(bgcolor="#0a0f1c", bordercolor=color, font=dict(color="#fff")),
    )
    return fig

# ---------- PAGES ----------
if page in ("Overview", "Live Session"):

    # KPI ROW
    st.markdown("<div class='section-title'>Key Metrics</div>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(f"""
        <div class='card'>
          <div class='card-head'>
            <div>
              <div class='card-label'>Risk Score</div>
              <div class='card-value' style='color:{risk_color(avg_risk)}'>{avg_risk:.0f}</div>
              <div class='card-sub'>Average · last session</div>
            </div>
            <div class='card-icon' style='background:rgba(255,77,109,.1);color:#ff4d6d;'>⚡</div>
          </div>
        </div>""", unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class='card'>
          <div class='card-head'>
            <div>
              <div class='card-value'>{drowsy_status}</div>
              <div class='card-value'>{drowsy_status.title()}</div>
              <div class='card-sub'><span class='badge {drowsy_class}'>{drowsy_status}</span></div>
            </div>
            <div class='card-icon'>👁️</div>
          </div>
        </div>""", unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class='card'>
          <div class='card-head'>
            <div>
              <div class='card-label'>Yawning Events</div>
              <div class='card-value' style='color:var(--warn)'>{yawns}</div>
              <div class='card-sub'>MAR threshold > 0.06</div>
            </div>
            <div class='card-icon' style='background:rgba(255,216,77,.1);color:#ffd84d;'>😮</div>
          </div>
        </div>""", unsafe_allow_html=True)

    with c4:
        st.markdown(f"""
        <div class='card'>
          <div class='card-head'>
            <div>
              <div class='card-label'>Distraction</div>
              <div class='card-value'>{distraction_pct:.0f}%</div>
              <div class='card-sub'>Off-center head pose</div>
            </div>
            <div class='card-icon' style='background:rgba(99,102,241,.12);color:#a5b4fc;'>🎯</div>
          </div>
        </div>""", unsafe_allow_html=True)

    # SAFETY SCORE + SUMMARY
    st.markdown("<div class='section-title'>Driver Safety Overview</div>", unsafe_allow_html=True)
    left, right = st.columns([1.3, 1])

    with left:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        a, b = st.columns([1, 1.4])
        with a:
            st.plotly_chart(ring(safety_score, risk_color(100 - safety_score)),
                            use_container_width=True, config={"displayModeBar": False})
        with b:
            st.markdown(f"""
            <div style='padding-top:14px;'>
              <div class='card-label'>Driver Safety Score</div>
              <div style='font-size:42px;font-weight:700;margin:6px 0;'>{safety_score}<span style='color:var(--muted);font-size:18px;'> / 100</span></div>
              <div class='card-sub'>Composite score from fatigue, attention & risk signals over the active session.</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        st.markdown(f"""
        <div class='card'>
          <div class='card-label'>Session Summary</div>
          <div style='margin-top:14px;'>
            <div class='summary-row'><span class='summary-key'>Records</span><span class='summary-val'>{len(df)}</span></div>
            <div class='summary-row'><span class='summary-key'>Avg Risk</span><span class='summary-val'>{avg_risk:.1f}</span></div>
            <div class='summary-row'><span class='summary-key'>Peak Risk</span><span class='summary-val'>{max_risk}</span></div>
            <div class='summary-row'><span class='summary-key'>Yawns Detected</span><span class='summary-val'>{yawns}</span></div>
            <div class='summary-row'><span class='summary-key'>Status</span><span class='summary-val'><span class='badge {drowsy_class}'>{drowsy_status}</span></span></div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    # CHARTS
    st.markdown("<div class='section-title'>Telemetry</div>", unsafe_allow_html=True)
    g1, g2 = st.columns(2)
    with g1:
        st.markdown("<div class='card'><div class='card-label'>Risk Score Over Time</div>", unsafe_allow_html=True)
        st.plotly_chart(gradient_line(df["timestamp"], df["risk_score"], "Risk", "#ff4d6d"),
                        use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)
    with g2:
        st.markdown("<div class='card'><div class='card-label'>Eye Aspect Ratio (EAR)</div>", unsafe_allow_html=True)
        st.plotly_chart(gradient_line(df["timestamp"], df["ear"], "EAR", "#22d3ee"),
                        use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    g3, g4 = st.columns(2)
    with g3:
        st.markdown("<div class='card'><div class='card-label'>Mouth Aspect Ratio (MAR)</div>", unsafe_allow_html=True)
        st.plotly_chart(gradient_line(df["timestamp"], df["mar"], "MAR", "#ffd84d"),
                        use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)
    with g4:
        st.markdown("<div class='card'><div class='card-label'>Head Pose Distribution</div>", unsafe_allow_html=True)
        pose = df["head_pose"].value_counts()
        fig = go.Figure(go.Bar(
            x=pose.index, y=pose.values,
            marker=dict(color="#22d3ee", line=dict(width=0)),
            hovertemplate="<b>%{x}</b>: %{y}<extra></extra>",
        ))
        fig.update_layout(
            height=280, margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#8a93a6"),
            xaxis=dict(gridcolor="rgba(255,255,255,0.04)"),
            yaxis=dict(gridcolor="rgba(255,255,255,0.04)"),
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

elif page == "Analytics":
    st.markdown("<div class='section-title'>Analytics Deep Dive</div>", unsafe_allow_html=True)
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.plotly_chart(gradient_line(df["timestamp"], df["risk_score"], "Risk Score", "#ff4d6d"),
                    use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)
    st.dataframe(df.describe(), use_container_width=True)

elif page == "Alerts":
    st.markdown("<div class='section-title'>Active Alerts</div>", unsafe_allow_html=True)
    alerts = df[df["risk_score"] >= 75].tail(20)
    if alerts.empty:
        st.markdown("<div class='card'>No high-risk events recorded.</div>", unsafe_allow_html=True)
    else:
        for _, r in alerts.iterrows():
            st.markdown(f"""
            <div class='card' style='margin-bottom:10px;display:flex;justify-content:space-between;align-items:center;'>
              <div>
                <span class='badge badge-danger'>HIGH RISK</span>
                <span style='margin-left:10px;color:var(--muted);font-size:13px;'>{r['timestamp']}</span>
              </div>
              <div style='font-weight:700;color:var(--danger);'>Risk {int(r['risk_score'])}</div>
            </div>
            """, unsafe_allow_html=True)

elif page == "History":
    st.markdown("<div class='section-title'>Session Logs</div>", unsafe_allow_html=True)
    st.dataframe(df.sort_values("timestamp", ascending=False), use_container_width=True, height=600)