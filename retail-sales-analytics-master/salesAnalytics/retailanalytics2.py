# import pandas as pd 
# import numpy as np
# import seaborn as sb 
# import matplotlib.pyplot as plt
# import datetime 
# from scipy import stats ## this liibrary is used for using statistical functions
# from sklearn.model_selection import train_test_split
# from sklearn.ensemble import RandomForestRegressor
# from sklearn.metrics import mean_squared_error
# from sklearn.cluster import KMeans
# from sklearn.preprocessing import StandardScaler
# import streamlit as st


# st.title("Retail Sales Analytics")

# uploaded_file = st.file_uploader("Upload your csv file", type=["csv"])
# if not uploaded_file:
#     st.info("Please upload the Sample‑Superstore CSV to view charts.")
#     st.stop()

# def streamlit_config():

#     # page configuration
#     st.set_page_config(page_title='Forecast', layout="wide")

#     # page header transparent color
#     page_background_color = """
#     <style>

#     [data-testid="stHeader"] 
#     {
#     background: rgba(0,0,0,0);
#     }

#     </style>
#     """
#     st.markdown(page_background_color, unsafe_allow_html=True)


# # custom style for submit button - color and width

# def style_submit_button():

#     st.markdown("""
#                     <style>
#                     div.stButton > button:first-child {
#                                                         background-color: #367F89;
#                                                         color: white;
#                                                         width: 70%}
#                     </style>
#                 """, unsafe_allow_html=True)


# # custom style for prediction result text - color and position

# def style_prediction():

#     st.markdown(
#         """
#             <style>
#             .center-text {
#                 text-align: center;
#                 color: #20CA0C
#             }
#             </style>
#             """,
#         unsafe_allow_html=True
#     )


# # cleaning the data
# data = pd.read_csv(r'salesAnalytics/Sample - Superstore.csv', encoding='ISO-8859-1')
# print(data.head()) ## this step is done to see whether the data is loaded correrctly or not

# print(data.info())
# st.write("File loaded. First 5 rows:")
# st.dataframe(data.head())

# # now we will turn the data into a correlation matrix of heatmap
# num_data = data.select_dtypes(include='number') ## this helps in including only numeric data
# correlation_matrix = num_data.corr() ## this turns the data into correlation matrix mraniing a square matrix inform of i,j
# print(correlation_matrix)
# fig = plt.figure(figsize = (7,7)) ## helps to figure the size of matrix
# sb.heatmap(correlation_matrix,annot=True,cmap='coolwarm') ##converts matrix into heatmap matrix
# plt.title("Correlational Maatrix") ##Gives the title of matrix
# plt.show() ## to dispay the matrix
# st.pyplot(fig)


# # converting data types
# data.dropna(inplace=True)
# data['Order Date'] = pd.to_datetime(data['Order Date'])## this converts the data type of order data into date time data type
# print(data.info())

# # putting month and year o order date
# data['month'] = data['Order Date'].dt.month
# data['year'] = data['Order Date'].dt.year
# print(data.head())

# # describing the data
# print(data.describe())

# # performing exploratory data analysis (EDA)
# # a) using time series charts like axis graphs
# monthly_sales = data.groupby(['year', 'month'])['Sales'].sum().reset_index() ##this line groups the data into year and month and sums thier values and then resets it do that we can plot it properly
# print("::m", monthly_sales)
# fig2 = plt.figure(figsize=(14,7))
# sb.lineplot(data=monthly_sales, x="month", y="Sales", hue="year")
# plt.title("Monthly Sales Report")
# plt.show()
# st.pyplot(fig2)

# print(monthly_sales) 
# # from this we get a line chart
# # b) using bar and pie chart
# fig3=plt.figure(figsize=(12,6))
# sb.barplot(data=data, x ='Category', y='Sales', hue='Region')
# plt.title('Category wise Sales by Region')
# plt.show()
# st.pyplot(fig3)


# region_sales = data.groupby('Region') ['Sales'].sum()
# fig4, ax = plt.subplots()
# ax.pie(region_sales, labels=region_sales.index, autopct='%1.1f%%')
# ax.set_title('Sales Distribution by Region')
# # plt.pie(region_sales,labels=region_sales.index,autopct='%1.1f%%')
# # plt.title('Sales by Region')
# # plt.show()
# st.pyplot(fig4)

# # c) Scatter plot
# fig5=plt.figure(figsize=(8,6))
# sb.scatterplot(data=data, x='Sales',y='Profit',hue='Segment')
# plt.title("Sales vs Profit by Customer Segment")
# plt.show()
# st.pyplot(fig5)


# # d) performance analysis
# data.columns = data.columns.str.strip()
# # print(data.columns.tolist())
# product_performance = data.pivot_table(values='Sales',index='Category',columns='Sub-Category',aggfunc='sum')
# fig6=plt.figure(figsize=(12,8))
# sb.heatmap(product_performance,cmap='YlGnBu')
# plt.title('Product Performance Heatmap')
# plt.show()
# st.pyplot(fig6)

# # e) Hypothesis testing and statistical analysis
# region1 = 'East'
# region2 = 'South'

# threshold = 0.05
# region1_sales = data[data['Region'] == region1] ['Sales']
# region2_sales = data[data['Region'] == region2] ['Sales']
# t_stat, p_val = stats.ttest_ind(region1_sales, region2_sales)
# print(f'p-value = {p_val}')

# if(p_val < threshold):
#     print("Reject null hypothesis, there is significant difference between two regions")
# elif(p_val > threshold):
#     print("Did not reject null hypothesis, there is no significant difference between two regions")

# print(data)
# print(num_data.corr())
# print(data.describe())

# sb.histplot(data=data, x='Discount', bins=20, kde=True)

# ## starting the machine learning part
# ## starting randomforest to forecast  the future sales values
# #use montly sales data and create a feature set
# monthly_sales['year_month'] = monthly_sales['year']*100 + monthly_sales['month'] ## this line of code will turn the date  like jan 2025 to 202501
# # create feature and target
# x = monthly_sales[['year','month','year_month']] ## this is feature to use
# y = monthly_sales['Sales']
# #  use train test split
# x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.2,random_state=42)
# # now we train the random forest regressor
# model = RandomForestRegressor(n_estimators=100,random_state=42) ## n_estimators = 100 means the sellection will be going through 100 decision trees
# model.fit(x_train,y_train)
# # predict the model and evaluate
# y_pred = model.predict(x_test)
# rmse = np.sqrt(mean_squared_error(y_pred,y_test))
# st.write(f"Model RMSE: {rmse:.2f}")
# # now we predict the future sale values of next 6 months
# last_year = monthly_sales['year'].max()
# last_month = monthly_sales['month'].max()
# future_dates = []
# for i in range(1,7):
#     month = (last_month + i)%12
#     year = last_year + (last_month + i-1)//12
#     if month == 0:
#         month = 12
#     future_dates.append({'year' : year , 'month' : month, 'year_month' : year*100+month})

# future_df = pd.DataFrame(future_dates)
# future_sales_pred = model.predict(future_df)
# # visualization of randomforestregresser
# fig_forecast = plt.figure(figsize=(14,7))
# sb.lineplot(data=monthly_sales,x='year_month',y='Sales',label = 'Historical Sales')
# plt.plot(future_df['year_month'],future_sales_pred,color = "red", marker = "o", label = "Predicted Sales")
# plt.title("Retail Sales Forecast")
# plt.xlabel("YearMonth")
# plt.ylabel("Sales")
# plt.legend()
# plt.grid(True)
# plt.show()
# st.pyplot(fig_forecast)

# # we are adding clustering algorith for customer segmentation
# customer_data = data.groupby('Customer ID').agg({
#     'Sales': 'sum',
#     'Profit': 'sum'
# }).reset_index()

# x = customer_data[['Sales', 'Profit']]
# # we normalize the features
# scaler = StandardScaler()
# X_scaled = scaler.fit_transform(x)
# # apply KMeans algorithm
# kmeans = KMeans(n_clusters=3, random_state=42)
# customer_data['Cluster'] = kmeans.fit_predict(X_scaled)
# # visualize the kmeans 
# fig_cluster = plt.figure(figsize=(10, 6))
# sb.scatterplot(data=customer_data, x='Sales', y='Profit', hue='Cluster', palette='Set2', s=100, alpha=0.7)
# plt.title('Customer Segmentation Based on Sales and Profit')
# plt.xlabel('Total Sales')
# plt.ylabel('Total Profit')
# plt.legend(title='Cluster')
# plt.grid(True)
# plt.show()

# st.pyplot(fig_cluster)

# # Show cluster counts
# st.write(customer_data['Cluster'].value_counts())


import warnings, hashlib, json, datetime, io, time, re
warnings.filterwarnings("ignore")
 
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from scipy import stats
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, IsolationForest
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import requests
 
# ════════════════════════════════════════════════════════════════════
# DESIGN TOKENS
# ════════════════════════════════════════════════════════════════════
C = {
    "bg":      "#060B14",
    "surface": "#0D1421",
    "card":    "#111C2E",
    "border":  "#1A2B45",
    "hover":   "#162238",
    "cyan":    "#00E5FF",
    "violet":  "#7B61FF",
    "green":   "#00D68F",
    "amber":   "#FFB300",
    "red":     "#FF4757",
    "pink":    "#FF6B9D",
    "text":    "#E8F0FE",
    "muted":   "#5C7A9E",
    "dim":     "#2A3F5F",
    "seq": ["#00E5FF","#7B61FF","#00D68F","#FFB300","#FF4757","#FF6B9D","#38BDF8","#A78BFA"],
}
 
# ════════════════════════════════════════════════════════════════════
# GLOBAL CSS
# ════════════════════════════════════════════════════════════════════
def inject_css():
    st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');
 
*, *::before, *::after {{ box-sizing: border-box; margin: 0; }}
html, body, [data-testid="stAppViewContainer"] {{
  background: {C['bg']} !important;
  color: {C['text']} !important;
  font-family: 'Plus Jakarta Sans', sans-serif !important;
}}
[data-testid="stHeader"] {{ background: rgba(0,0,0,0) !important; height: 0 !important; }}
#MainMenu, footer, [data-testid="stToolbar"], [data-testid="stDecoration"] {{ display: none !important; }}
.block-container {{ padding: 0 !important; max-width: 100% !important; }}
 
[data-testid="stSidebar"] {{
  background: {C['surface']} !important;
  border-right: 1px solid {C['border']} !important;
  min-width: 240px !important; max-width: 240px !important;
}}
[data-testid="stSidebar"] * {{ color: {C['text']} !important; }}
[data-testid="stSidebar"] > div:first-child {{ padding: 0 !important; }}
section[data-testid="stSidebar"] > div {{ padding: 0 !important; }}
 
[data-testid="stMultiSelect"] span[data-baseweb="tag"] {{
  background: rgba(0,229,255,0.12) !important;
  border: 1px solid rgba(0,229,255,0.3) !important;
  color: {C['cyan']} !important; border-radius: 4px !important;
}}
[data-testid="stMultiSelect"] [data-baseweb="select"] > div,
[data-testid="stSelectbox"] [data-baseweb="select"] > div {{
  background: {C['card']} !important; border-color: {C['border']} !important;
  color: {C['text']} !important;
}}
 
[data-testid="stTabs"] > div:first-child {{
  background: {C['surface']}; border-bottom: 1px solid {C['border']};
  padding: 0 1.5rem; gap: 0;
}}
button[data-baseweb="tab"] {{
  font-family: 'Plus Jakarta Sans', sans-serif !important;
  font-weight: 600 !important; font-size: 0.78rem !important;
  letter-spacing: 0.02em !important; color: {C['muted']} !important;
  background: transparent !important; border-radius: 0 !important;
  padding: 0.85rem 1.1rem !important;
  border-bottom: 2px solid transparent !important; transition: all 0.2s !important;
}}
button[data-baseweb="tab"]:hover {{ color: {C['text']} !important; }}
button[data-baseweb="tab"][aria-selected="true"] {{
  color: {C['cyan']} !important; border-bottom: 2px solid {C['cyan']} !important;
}}
[data-testid="stTabsContent"] {{ padding: 1.5rem !important; background: {C['bg']}; }}
 
[data-testid="metric-container"] {{
  background: {C['card']} !important; border: 1px solid {C['border']} !important;
  border-radius: 12px !important; padding: 1rem 1.25rem !important;
}}
[data-testid="metric-container"] label {{
  color: {C['muted']} !important; font-size: 0.7rem !important;
  font-family: 'JetBrains Mono', monospace !important;
  text-transform: uppercase !important; letter-spacing: 0.1em !important;
}}
[data-testid="stMetricValue"] {{
  color: {C['text']} !important; font-family: 'Plus Jakarta Sans', sans-serif !important;
  font-weight: 800 !important; font-size: 1.6rem !important;
}}
 
[data-testid="stDataFrame"] {{
  background: {C['card']} !important; border-radius: 10px !important;
  border: 1px solid {C['border']} !important;
}}
 
.stButton > button {{
  background: linear-gradient(135deg, {C['cyan']}, {C['violet']}) !important;
  color: {C['bg']} !important; font-family: 'Plus Jakarta Sans', sans-serif !important;
  font-weight: 700 !important; font-size: 0.82rem !important;
  border: none !important; border-radius: 8px !important;
  padding: 0.55rem 1.5rem !important; transition: opacity 0.2s !important;
}}
.stButton > button:hover {{ opacity: 0.85 !important; }}
 
input[type="text"], input[type="password"] {{
  background: {C['card']} !important; border: 1px solid {C['border']} !important;
  border-radius: 8px !important; color: {C['text']} !important;
}}
[data-testid="stTextInput"] label, [data-testid="stPasswordInput"] label {{
  color: {C['muted']} !important; font-size: 0.78rem !important; font-weight: 600 !important;
}}
 
[data-testid="stSlider"] label, [data-testid="stSelectSlider"] label {{
  color: {C['muted']} !important; font-size: 0.78rem !important;
}}
[data-testid="stFileUploaderDropzone"] {{
  background: {C['card']} !important; border: 2px dashed {C['border']} !important;
  border-radius: 12px !important;
}}
::-webkit-scrollbar {{ width: 4px; height: 4px; }}
::-webkit-scrollbar-track {{ background: {C['surface']}; }}
::-webkit-scrollbar-thumb {{ background: {C['dim']}; border-radius: 2px; }}
</style>
""", unsafe_allow_html=True)
 
 
# ════════════════════════════════════════════════════════════════════
# AUTH SYSTEM
# ════════════════════════════════════════════════════════════════════
DEFAULT_USERS = {
    "demo@retailiq.ai": {
        "name": "Demo User", "password": hashlib.sha256(b"demo1234").hexdigest(),
        "plan": "Pro", "avatar": "D", "company": "RetailIQ Demo",
    },
    "admin@retailiq.ai": {
        "name": "Admin", "password": hashlib.sha256(b"admin123").hexdigest(),
        "plan": "Enterprise", "avatar": "A", "company": "RetailIQ Inc.",
    },
}
 
def hash_pw(pw):
    return hashlib.sha256(pw.encode()).hexdigest()
 
def get_users():
    if "users_db" not in st.session_state:
        st.session_state["users_db"] = dict(DEFAULT_USERS)
    return st.session_state["users_db"]
 
def login(email, password):
    users = get_users()
    u = users.get(email.lower().strip())
    if u and u["password"] == hash_pw(password):
        st.session_state["auth"] = {"email": email, **u}
        return True
    return False
 
def signup(name, email, password, company):
    users = get_users()
    email = email.lower().strip()
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return False, "Invalid email address."
    if len(password) < 8:
        return False, "Password must be at least 8 characters."
    if email in users:
        return False, "Account already exists."
    users[email] = {
        "name": name, "password": hash_pw(password),
        "plan": "Starter", "avatar": name[0].upper() if name else "U",
        "company": company or "—",
    }
    st.session_state["users_db"] = users
    st.session_state["auth"] = {"email": email, **users[email]}
    return True, "ok"
 
def logout():
    for k in ["auth", "df_raw", "df_bytes", "chat_history"]:
        st.session_state.pop(k, None)
 
def current_user():
    return st.session_state.get("auth")
 
 
# ════════════════════════════════════════════════════════════════════
# AUTH PAGE
# ════════════════════════════════════════════════════════════════════
def render_auth_page():
    st.markdown(f"""
<style>
[data-testid="stAppViewContainer"] {{
  background: radial-gradient(ellipse 120% 80% at 50% -20%,
    rgba(0,229,255,0.07) 0%, transparent 60%), {C['bg']} !important;
}}
</style>""", unsafe_allow_html=True)
 
    _, col, _ = st.columns([1, 2, 1])
    with col:
        st.markdown("<div style='height:8vh'></div>", unsafe_allow_html=True)
        st.markdown(f"""
<div style="text-align:center;margin-bottom:2rem;">
  <div style="font-family:'Plus Jakarta Sans',sans-serif;font-weight:800;font-size:2rem;
              letter-spacing:-0.04em;background:linear-gradient(135deg,{C['cyan']},{C['violet']});
              -webkit-background-clip:text;-webkit-text-fill-color:transparent;
              background-clip:text;margin-bottom:0.25rem;">RETAIL IQ</div>
  <div style="font-family:'JetBrains Mono',monospace;font-size:0.62rem;color:{C['muted']};
              letter-spacing:0.18em;text-transform:uppercase;">Enterprise Analytics Platform</div>
</div>""", unsafe_allow_html=True)
 
        st.markdown(f"""
<div style="background:{C['surface']};border:1px solid {C['border']};
            border-radius:20px;padding:2rem;">""", unsafe_allow_html=True)
 
        mode = st.radio("", ["Sign In", "Create Account"], horizontal=True,
                        label_visibility="collapsed", key="auth_mode")
 
        if mode == "Sign In":
            email    = st.text_input("Email", placeholder="you@company.com", key="li_email")
            password = st.text_input("Password", type="password", placeholder="••••••••", key="li_pw")
            if st.button("Sign In →", use_container_width=True, key="li_btn"):
                if login(email, password):
                    st.rerun()
                else:
                    st.error("Invalid credentials.")
            st.markdown(f"""
<div style="background:rgba(0,229,255,0.06);border:1px solid rgba(0,229,255,0.15);
            border-radius:8px;padding:0.75rem 1rem;margin-top:1rem;
            font-size:0.75rem;color:{C['muted']};line-height:1.8;">
  🔑 <b style="color:{C['cyan']}">demo@retailiq.ai</b> / demo1234<br>
  👑 <b style="color:{C['cyan']}">admin@retailiq.ai</b> / admin123
</div>""", unsafe_allow_html=True)
 
        else:
            name     = st.text_input("Full Name", placeholder="Jane Smith", key="su_name")
            email    = st.text_input("Work Email", placeholder="jane@company.com", key="su_email")
            company  = st.text_input("Company", placeholder="Acme Corp", key="su_company")
            password = st.text_input("Password", type="password", placeholder="Min. 8 characters", key="su_pw")
            if st.button("Create Account →", use_container_width=True, key="su_btn"):
                ok, msg = signup(name, email, password, company)
                if ok:
                    st.success("Welcome! Redirecting…")
                    time.sleep(0.8); st.rerun()
                else:
                    st.error(msg)
 
        st.markdown("</div>", unsafe_allow_html=True)
 
 
# ════════════════════════════════════════════════════════════════════
# DATA PIPELINE
# ════════════════════════════════════════════════════════════════════
@st.cache_data(show_spinner=False)
def load_data(raw_bytes):
    df = pd.read_csv(io.BytesIO(raw_bytes), encoding="ISO-8859-1")
    df.columns = df.columns.str.strip()
    df.dropna(inplace=True)
    df["Order Date"] = pd.to_datetime(df["Order Date"])
    df["Ship Date"]  = pd.to_datetime(df["Ship Date"])
    df["month"]      = df["Order Date"].dt.month
    df["year"]       = df["Order Date"].dt.year
    df["quarter"]    = df["Order Date"].dt.quarter
    df["ship_lag"]   = (df["Ship Date"] - df["Order Date"]).dt.days
    df["profit_margin"] = (df["Profit"] / df["Sales"].replace(0, np.nan)).fillna(0)
    return df
 
@st.cache_data(show_spinner=False)
def build_monthly(df_json):
    df = pd.read_json(io.StringIO(df_json))
    df["Order Date"] = pd.to_datetime(df["Order Date"])
    ms = df.groupby(["year","month"]).agg(
        Sales=("Sales","sum"), Profit=("Profit","sum"),
        Orders=("Order ID","nunique")
    ).reset_index()
    ms["year_month"] = ms["year"]*100 + ms["month"]
    ms["date"]       = pd.to_datetime(ms[["year","month"]].assign(day=1))
    ms["profit_margin"] = ms["Profit"] / ms["Sales"]
    return ms.sort_values("date").reset_index(drop=True)
 
 
# ════════════════════════════════════════════════════════════════════
# THEME HELPER
# ════════════════════════════════════════════════════════════════════
def theme(fig, title="", h=360):
    fig.update_layout(
        title=dict(text=title, font=dict(family="Plus Jakarta Sans", size=13,
                   color=C["text"], weight=700), x=0, pad=dict(l=2)),
        height=h, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Plus Jakarta Sans", color=C["muted"], size=11),
        legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor=C["border"], borderwidth=1,
                    font=dict(size=11), orientation="h", y=-0.15),
        margin=dict(l=8, r=8, t=42, b=8),
        xaxis=dict(gridcolor=C["border"], linecolor=C["border"], tickfont=dict(size=10)),
        yaxis=dict(gridcolor=C["border"], linecolor=C["border"], tickfont=dict(size=10)),
        colorway=C["seq"],
        hoverlabel=dict(bgcolor=C["card"], bordercolor=C["border"],
                        font=dict(family="Plus Jakarta Sans", size=12)),
    )
    return fig
 
def fmt_k(v):
    if abs(v) >= 1e6: return f"${v/1e6:.2f}M"
    if abs(v) >= 1e3: return f"${v/1e3:.1f}K"
    return f"${v:.0f}"
 
def section(title):
    st.markdown(f"""
<div style="display:flex;align-items:center;gap:0.75rem;margin:1.5rem 0 1rem;">
  <div style="width:3px;height:1rem;background:{C['cyan']};border-radius:2px;flex-shrink:0;"></div>
  <span style="font-family:'Plus Jakarta Sans',sans-serif;font-weight:700;
               font-size:0.95rem;color:{C['text']};">{title}</span>
</div>""", unsafe_allow_html=True)
 
def insight_box(text, color=None):
    color = color or C["cyan"]
    st.markdown(f"""
<div style="background:{C['card']};border:1px solid {C['border']};
            border-left:3px solid {color};border-radius:10px;
            padding:1rem 1.25rem;margin:0.75rem 0;font-size:0.84rem;line-height:1.7;">
  {text}
</div>""", unsafe_allow_html=True)
 
 
# ════════════════════════════════════════════════════════════════════
# CHART LIBRARY
# ════════════════════════════════════════════════════════════════════
def ch_trend(ms):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=ms["date"], y=ms["Sales"], name="Revenue",
        line=dict(color=C["cyan"], width=2.5), fill="tozeroy",
        fillcolor="rgba(0,229,255,0.05)",
        hovertemplate="<b>%{x|%b %Y}</b><br>Revenue: $%{y:,.0f}<extra></extra>"))
    fig.add_trace(go.Scatter(x=ms["date"], y=ms["Profit"], name="Profit",
        line=dict(color=C["green"], width=2),
        hovertemplate="<b>%{x|%b %Y}</b><br>Profit: $%{y:,.0f}<extra></extra>"))
    return theme(fig, "Monthly Revenue & Profit Trend", 340)
 
def ch_region_pie(df):
    grp = df.groupby("Region")["Sales"].sum().reset_index()
    fig = go.Figure(go.Pie(
        labels=grp["Region"], values=grp["Sales"], hole=0.58,
        marker=dict(colors=C["seq"], line=dict(color=C["bg"], width=2)),
        textfont=dict(family="Plus Jakarta Sans", size=11),
        hovertemplate="%{label}: $%{value:,.0f} (%{percent})<extra></extra>"))
    fig.update_layout(
        annotations=[dict(text="Region<br>Sales", x=0.5, y=0.5, font_size=10,
                          font_family="Plus Jakarta Sans", showarrow=False,
                          font_color=C["muted"])])
    return theme(fig, "Sales by Region", 320)
 
def ch_category(df):
    grp = df.groupby("Category").agg(Sales=("Sales","sum"), Profit=("Profit","sum")).reset_index()
    fig = go.Figure()
    fig.add_trace(go.Bar(name="Revenue", x=grp["Category"], y=grp["Sales"],
        marker_color=C["cyan"], hovertemplate="%{x}: $%{y:,.0f}<extra></extra>"))
    fig.add_trace(go.Bar(name="Profit", x=grp["Category"], y=grp["Profit"],
        marker_color=C["green"], hovertemplate="%{x}: $%{y:,.0f}<extra></extra>"))
    fig.update_layout(barmode="group")
    return theme(fig, "Category Performance", 300)
 
def ch_yoy(ms):
    fig = go.Figure()
    mo = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    for i, yr in enumerate(sorted(ms["year"].unique())):
        sub = ms[ms["year"]==yr].sort_values("month")
        fig.add_trace(go.Scatter(
            x=[mo[m-1] for m in sub["month"]], y=sub["Sales"],
            name=str(yr), line=dict(color=C["seq"][i % len(C["seq"])], width=2),
            mode="lines+markers", marker=dict(size=5),
            hovertemplate=f"<b>{yr} %{{x}}</b>: $%{{y:,.0f}}<extra></extra>"))
    return theme(fig, "Year-over-Year Comparison", 320)
 
def ch_scatter_profit(df):
    fig = px.scatter(df, x="Sales", y="Profit", color="Segment", size="Quantity",
                     color_discrete_sequence=C["seq"], opacity=0.6,
                     hover_data=["Category","Sub-Category"])
    return theme(fig, "Sales vs Profit by Segment", 360)
 
def ch_top_products(df, n=12):
    grp = df.groupby("Sub-Category").agg(
        Sales=("Sales","sum"), Profit=("Profit","sum")).nlargest(n,"Sales").reset_index()
    fig = px.bar(grp.sort_values("Sales"), x="Sales", y="Sub-Category", orientation="h",
                 color="Profit",
                 color_continuous_scale=[[0,C["red"]],[0.45,C["violet"]],[1,C["green"]]],
                 hover_data=["Profit"])
    # FIX: changed titlefont -> title_font (valid Plotly property)
    fig.update_coloraxes(colorbar=dict(thickness=8, len=0.7, title="Profit",
                                       tickfont=dict(size=9), title_font=dict(size=10)))
    return theme(fig, f"Top {n} Sub-Categories by Revenue", 360)
 
def ch_heatmap(df):
    pt = df.pivot_table(values="Profit", index="Category",
                        columns="Sub-Category", aggfunc="sum")
    fig = px.imshow(pt, aspect="auto",
                    color_continuous_scale=[[0,C["red"]],[0.5,C["surface"]],[1,C["green"]]],
                    text_auto=".0f")
    fig.update_coloraxes(showscale=False)
    fig.update_xaxes(tickangle=-35, tickfont=dict(size=9))
    return theme(fig, "Profit Heatmap: Category × Sub-Category", 260)
 
def ch_discount(df):
    df2 = df.copy()
    bins   = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 1.01]
    labels = ["0–10%","10–20%","20–30%","30–40%","40–50%",">50%"]
    df2["Band"] = pd.cut(df2["Discount"], bins=bins, labels=labels, include_lowest=True)
    grp = df2.groupby("Band", observed=True)["profit_margin"].mean().reset_index()
    colors = [C["green"] if v > 0 else C["red"] for v in grp["profit_margin"]]
    fig = go.Figure(go.Bar(x=grp["Band"], y=grp["profit_margin"]*100,
        marker_color=colors, hovertemplate="%{x}: %{y:.1f}%<extra></extra>"))
    fig.add_hline(y=0, line_color=C["muted"], line_width=1)
    return theme(fig, "Avg Profit Margin by Discount Band", 280)
 
def ch_shipmode(df):
    grp = df.groupby("Ship Mode")["Sales"].sum().sort_values().reset_index()
    fig = go.Figure(go.Bar(x=grp["Sales"], y=grp["Ship Mode"], orientation="h",
        marker=dict(color=C["seq"][:len(grp)]),
        hovertemplate="%{y}: $%{x:,.0f}<extra></extra>"))
    return theme(fig, "Revenue by Shipping Mode", 260)
 
def ch_geo(df):
    """Choropleth — maps full state names to 2-letter codes."""
    abbrev = {
        "Alabama":"AL","Alaska":"AK","Arizona":"AZ","Arkansas":"AR","California":"CA",
        "Colorado":"CO","Connecticut":"CT","Delaware":"DE","Florida":"FL","Georgia":"GA",
        "Hawaii":"HI","Idaho":"ID","Illinois":"IL","Indiana":"IN","Iowa":"IA","Kansas":"KS",
        "Kentucky":"KY","Louisiana":"LA","Maine":"ME","Maryland":"MD","Massachusetts":"MA",
        "Michigan":"MI","Minnesota":"MN","Mississippi":"MS","Missouri":"MO","Montana":"MT",
        "Nebraska":"NE","Nevada":"NV","New Hampshire":"NH","New Jersey":"NJ","New Mexico":"NM",
        "New York":"NY","North Carolina":"NC","North Dakota":"ND","Ohio":"OH","Oklahoma":"OK",
        "Oregon":"OR","Pennsylvania":"PA","Rhode Island":"RI","South Carolina":"SC",
        "South Dakota":"SD","Tennessee":"TN","Texas":"TX","Utah":"UT","Vermont":"VT",
        "Virginia":"VA","Washington":"WA","West Virginia":"WV","Wisconsin":"WI","Wyoming":"WY",
        "District of Columbia":"DC",
    }
    grp = df.groupby("State").agg(
        Sales=("Sales","sum"), Profit=("Profit","sum"),
        Orders=("Order ID","nunique")).reset_index()
    grp["code"] = grp["State"].map(abbrev)
    grp = grp.dropna(subset=["code"])
    fig = go.Figure(go.Choropleth(
        locations=grp["code"], z=grp["Sales"],
        locationmode="USA-states",
        colorscale=[[0, C["surface"]], [0.3, C["violet"]], [1, C["cyan"]]],
        marker_line_color=C["border"], marker_line_width=0.5,
        colorbar=dict(thickness=10, len=0.65, title="Sales",
                      tickfont=dict(size=9, color=C["muted"]),
                      title_font=dict(size=10, color=C["muted"])),
        hovertemplate="<b>%{location}</b><br>Sales: $%{z:,.0f}<extra></extra>",
    ))
    fig.update_layout(
        geo=dict(scope="usa", bgcolor="rgba(0,0,0,0)",
                 lakecolor="rgba(0,0,0,0)", landcolor=C["card"],
                 showlakes=False, subunitcolor=C["border"], showframe=False),
    )
    return theme(fig, "Geographic Revenue Distribution — USA", 420)
 
def ch_forecast(ms, future_df):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=ms["date"], y=ms["Sales"], name="Historical",
        line=dict(color=C["cyan"], width=2.5), fill="tozeroy",
        fillcolor="rgba(0,229,255,0.05)",
        hovertemplate="<b>%{x|%b %Y}</b><br>$%{y:,.0f}<extra></extra>"))
    lo = future_df["pred"] * 0.87; hi = future_df["pred"] * 1.13
    fig.add_trace(go.Scatter(
        x=list(future_df["date"]) + list(future_df["date"][::-1]),
        y=list(hi) + list(lo[::-1]),
        fill="toself", fillcolor="rgba(123,97,255,0.12)",
        line=dict(color="rgba(0,0,0,0)"), name="Confidence Band", hoverinfo="skip"))
    fig.add_trace(go.Scatter(x=future_df["date"], y=future_df["pred"],
        name="Forecast", line=dict(color=C["violet"], width=2.5, dash="dot"),
        mode="lines+markers", marker=dict(size=7, color=C["violet"]),
        hovertemplate="<b>%{x|%b %Y}</b><br>Forecast: $%{y:,.0f}<extra></extra>"))
    fig.add_vline(x=ms["date"].max().timestamp()*1000, line_dash="dash",
                  line_color=C["dim"], line_width=1)
    return theme(fig, "ML Sales Forecast", 400)
 
def ch_cluster(cdf):
    fig = px.scatter(cdf, x="Total_Sales", y="Total_Profit",
                     color=cdf["Cluster"].astype(str), size="Num_Orders", size_max=18,
                     color_discrete_sequence=C["seq"], opacity=0.75,
                     hover_data=["Customer ID","Num_Orders","Avg_Discount"])
    return theme(fig, "Customer Segmentation (K-Means)", 400)
 
def ch_pca(cdf):
    feats = cdf[["Total_Sales","Total_Profit","Num_Orders","Avg_Discount"]].fillna(0)
    pca = PCA(n_components=2, random_state=42)
    sc  = StandardScaler()
    comps = pca.fit_transform(sc.fit_transform(feats))
    cdf2 = cdf.copy(); cdf2["PC1"] = comps[:,0]; cdf2["PC2"] = comps[:,1]
    fig = px.scatter(cdf2, x="PC1", y="PC2", color=cdf2["Cluster"].astype(str),
                     size="Total_Sales", size_max=20,
                     color_discrete_sequence=C["seq"], opacity=0.75,
                     hover_data=["Customer ID"])
    ev = pca.explained_variance_ratio_
    fig.update_layout(xaxis_title=f"PC1 ({ev[0]*100:.1f}%)",
                      yaxis_title=f"PC2 ({ev[1]*100:.1f}%)")
    return theme(fig, "PCA Customer Cluster Projection", 360)
 
def ch_anomaly(df):
    iso = IsolationForest(contamination=0.05, random_state=42)
    scores = iso.fit_predict(df[["Sales","Profit"]].values)
    df2 = df.copy(); df2["anomaly"] = scores
    normal  = df2[df2["anomaly"]== 1]
    outlier = df2[df2["anomaly"]==-1]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=normal["Sales"], y=normal["Profit"], mode="markers",
        name="Normal", marker=dict(color=C["cyan"], size=4, opacity=0.45),
        hovertemplate="Sales: $%{x:,.0f}<br>Profit: $%{y:,.0f}<extra></extra>"))
    fig.add_trace(go.Scatter(x=outlier["Sales"], y=outlier["Profit"], mode="markers",
        name=f"Anomaly ({len(outlier)})", marker=dict(color=C["red"], size=7, symbol="x"),
        hovertemplate="⚠ Sales: $%{x:,.0f}<br>Profit: $%{y:,.0f}<extra></extra>"))
    return theme(fig, "Anomaly Detection — Isolation Forest", 320)
 
def ch_corr(df):
    cols = df[["Sales","Profit","Quantity","Discount","profit_margin","ship_lag"]].copy()
    cols.columns = ["Sales","Profit","Qty","Discount","Margin","ShipLag"]
    corr = cols.corr().round(3)
    fig = px.imshow(corr,
                    color_continuous_scale=[[0,C["red"]],[0.5,C["card"]],[1,C["cyan"]]],
                    text_auto=True, aspect="auto", zmin=-1, zmax=1)
    fig.update_coloraxes(colorbar=dict(thickness=8, len=0.8))
    return theme(fig, "Feature Correlation Matrix", 320)
 
def ch_violin(df):
    fig = go.Figure()
    for i, cat in enumerate(df["Category"].unique()):
        fig.add_trace(go.Violin(y=df[df["Category"]==cat]["Sales"], name=cat,
            box_visible=True, meanline_visible=True,
            line_color=C["seq"][i], fillcolor="rgba(0,0,0,0)"))
    return theme(fig, "Sales Distribution by Category", 280)
 
 
# ════════════════════════════════════════════════════════════════════
# ML ENGINE
# ════════════════════════════════════════════════════════════════════
@st.cache_data(show_spinner=False)
def train_models(ms_json):
    ms = pd.read_json(io.StringIO(ms_json))
    X  = ms[["year","month","year_month"]].values
    y  = ms["Sales"].values
    Xtr,Xte,ytr,yte = train_test_split(X, y, test_size=0.2, random_state=42)
    mdls = {
        "Random Forest":     RandomForestRegressor(n_estimators=200, random_state=42),
        "Gradient Boosting": GradientBoostingRegressor(n_estimators=200, random_state=42),
        "Ridge Regression":  Ridge(alpha=1.0),
    }
    results = {}; best_name, best_rmse, best_model = None, np.inf, None
    for name, m in mdls.items():
        m.fit(Xtr, ytr); preds = m.predict(Xte)
        rmse = np.sqrt(mean_squared_error(yte, preds))
        results[name] = {"rmse":rmse, "mae":mean_absolute_error(yte,preds),
                          "r2":r2_score(yte,preds), "model":m}
        if rmse < best_rmse: best_rmse=rmse; best_name=name; best_model=m
    return best_model, best_name, results
 
@st.cache_data(show_spinner=False)
def make_forecast(_model, ms_json, n):
    ms = pd.read_json(io.StringIO(ms_json))
    ly, lm = int(ms["year"].max()), int(ms["month"].max())
    rows = []
    for i in range(1, n+1):
        raw = lm+i; m = ((raw-1)%12)+1; y = ly+(raw-1)//12
        rows.append({"year":y,"month":m,"year_month":y*100+m})
    fdf = pd.DataFrame(rows)
    fdf["pred"] = _model.predict(fdf[["year","month","year_month"]].values)
    fdf["date"] = pd.to_datetime(fdf[["year","month"]].assign(day=1))
    return fdf
 
@st.cache_data(show_spinner=False)
def run_clustering(df_json, k):
    df = pd.read_json(io.StringIO(df_json))
    agg = df.groupby("Customer ID").agg(
        Total_Sales=("Sales","sum"), Total_Profit=("Profit","sum"),
        Num_Orders=("Order ID","nunique"), Avg_Discount=("Discount","mean")
    ).reset_index()
    feats = agg[["Total_Sales","Total_Profit","Num_Orders","Avg_Discount"]].fillna(0)
    sc = StandardScaler(); km = KMeans(n_clusters=k, random_state=42, n_init=10)
    agg["Cluster"] = km.fit_predict(sc.fit_transform(feats))
    return agg
 
 
# ════════════════════════════════════════════════════════════════════
# AI CHATBOT
# ════════════════════════════════════════════════════════════════════
def build_system(df, ms):
    ts = df["Sales"].sum(); tp = df["Profit"].sum()
    mg = tp/ts if ts else 0
    tc = df.groupby("Category")["Profit"].sum().idxmax()
    ws = df.groupby("Sub-Category")["Profit"].sum().idxmin()
    br = df.groupby("Region")["Sales"].sum().idxmax()
    bt = df.groupby("State")["Sales"].sum().idxmax()
    yrs = sorted(df["year"].unique().tolist())
    return f"""You are RetailIQ Assistant — an expert BI AI embedded in the RetailIQ SaaS platform.
 
LIVE DATASET SUMMARY:
- Total Revenue: ${ts:,.0f}  |  Total Profit: ${tp:,.0f}  |  Margin: {mg*100:.1f}%
- Orders: {df['Order ID'].nunique():,}  |  Customers: {df['Customer ID'].nunique():,}
- Years: {yrs}  |  Best Category: {tc}  |  Worst Sub-Cat: {ws}
- Top Region: {br}  |  Top State: {bt}
 
You can discuss: revenue trends, YoY growth, seasonality, product performance, discount impact,
customer segmentation (RFM/K-Means), ML forecasting (RF/GBM/Ridge), geographic analysis,
statistical tests, anomaly detection, and strategic business recommendations.
 
Be concise, data-driven, use bullet points for lists, cite numbers where relevant.
For forecasts, explain model confidence and limitations. Keep responses under 300 words."""
 
def chat_api(messages, system):
    try:
        r = requests.post("https://api.anthropic.com/v1/messages",
            headers={"Content-Type":"application/json"},
            json={"model":"claude-sonnet-4-20250514","max_tokens":1000,
                  "system":system,"messages":messages}, timeout=30)
        if r.status_code == 200:
            return r.json()["content"][0]["text"]
        return f"⚠️ API error {r.status_code}. Please try again."
    except Exception as e:
        return f"⚠️ Connection error: {str(e)[:100]}"
 
def render_chatbot(df, ms):
    section("🤖 AI Business Intelligence Assistant")
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []
 
    sys_prompt = build_system(df, ms)
 
    # Render chat history
    if not st.session_state["chat_history"]:
        st.markdown(f"""
<div style="background:{C['card']};border:1px solid {C['border']};border-radius:14px;
            padding:2rem;text-align:center;margin-bottom:1.25rem;">
  <div style="font-size:2.5rem;margin-bottom:0.75rem;">🤖</div>
  <div style="font-weight:700;font-size:1.05rem;margin-bottom:0.5rem;">RetailIQ AI Assistant</div>
  <div style="color:{C['muted']};font-size:0.83rem;line-height:1.7;max-width:480px;margin:0 auto;">
    Ask me anything — sales forecasts, product insights, customer behavior,
    regional performance, or strategic recommendations.
  </div>
</div>
<div style="display:flex;gap:0.5rem;flex-wrap:wrap;margin-bottom:1.25rem;">
  <span style="background:{C['card']};border:1px solid {C['border']};padding:0.4rem 0.9rem;
               border-radius:999px;font-size:0.75rem;color:{C['muted']};">
    📈 What are my top growth opportunities?</span>
  <span style="background:{C['card']};border:1px solid {C['border']};padding:0.4rem 0.9rem;
               border-radius:999px;font-size:0.75rem;color:{C['muted']};">
    🔮 Forecast next quarter revenue</span>
  <span style="background:{C['card']};border:1px solid {C['border']};padding:0.4rem 0.9rem;
               border-radius:999px;font-size:0.75rem;color:{C['muted']};">
    ⚠️ Which sub-categories lose money?</span>
</div>""", unsafe_allow_html=True)
 
    for msg in st.session_state["chat_history"]:
        if msg["role"] == "user":
            st.markdown(f"""
<div style="display:flex;justify-content:flex-end;margin-bottom:0.75rem;">
  <div style="background:linear-gradient(135deg,rgba(0,229,255,0.12),rgba(123,97,255,0.12));
              border:1px solid {C['border']};border-radius:14px 14px 4px 14px;
              padding:0.75rem 1rem;max-width:75%;font-size:0.85rem;line-height:1.55;">
    {msg['content']}</div></div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""
<div style="display:flex;gap:0.75rem;margin-bottom:0.75rem;align-items:flex-start;">
  <div style="width:28px;height:28px;min-width:28px;border-radius:50%;
              background:linear-gradient(135deg,{C['cyan']},{C['violet']});
              display:flex;align-items:center;justify-content:center;
              font-size:0.7rem;font-weight:700;color:{C['bg']};flex-shrink:0;">AI</div>
  <div style="background:{C['card']};border:1px solid {C['border']};
              border-radius:4px 14px 14px 14px;padding:0.75rem 1rem;
              max-width:85%;font-size:0.84rem;line-height:1.65;
              white-space:pre-wrap;">{msg['content']}</div>
</div>""", unsafe_allow_html=True)
 
    # Input
    c1, c2, c3 = st.columns([6,1,1])
    with c1:
        user_input = st.text_input("", placeholder="Ask about your data…",
                                   label_visibility="collapsed", key="chat_input")
    with c2:
        send = st.button("Send", use_container_width=True, key="chat_send")
    with c3:
        if st.button("Clear", use_container_width=True, key="chat_clear"):
            st.session_state["chat_history"] = []; st.rerun()
 
    if send and user_input.strip():
        st.session_state["chat_history"].append({"role":"user","content":user_input.strip()})
        with st.spinner("Thinking…"):
            reply = chat_api(
                [{"role":m["role"],"content":m["content"]}
                 for m in st.session_state["chat_history"]],
                sys_prompt)
        st.session_state["chat_history"].append({"role":"assistant","content":reply})
        st.rerun()
 
 
# ════════════════════════════════════════════════════════════════════
# TOP BAR
# ════════════════════════════════════════════════════════════════════
def render_topbar(u):
    st.markdown(f"""
<div style="background:{C['surface']};border-bottom:1px solid {C['border']};
            padding:0.7rem 1.75rem;display:flex;align-items:center;
            justify-content:space-between;">
  <div style="display:flex;align-items:center;gap:0.75rem;">
    <span style="font-family:'Plus Jakarta Sans',sans-serif;font-weight:800;font-size:1.1rem;
                 letter-spacing:-0.04em;
                 background:linear-gradient(135deg,{C['cyan']},{C['violet']});
                 -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                 background-clip:text;">RETAIL IQ</span>
    <span style="background:rgba(0,229,255,0.1);border:1px solid rgba(0,229,255,0.2);
                 color:{C['cyan']};font-family:'JetBrains Mono',monospace;font-size:0.58rem;
                 padding:0.15rem 0.5rem;border-radius:999px;font-weight:600;">v2.0</span>
  </div>
  <div style="display:flex;align-items:center;gap:1.25rem;">
    <span style="font-family:'JetBrains Mono',monospace;font-size:0.7rem;
                 color:{C['muted']};">{u['company']}</span>
    <span style="background:rgba(0,214,143,0.1);border:1px solid rgba(0,214,143,0.25);
                 color:{C['green']};font-family:'JetBrains Mono',monospace;
                 font-size:0.58rem;padding:0.2rem 0.55rem;border-radius:999px;font-weight:700;">
      ● LIVE</span>
  </div>
</div>""", unsafe_allow_html=True)
 
 
# ════════════════════════════════════════════════════════════════════
# SIDEBAR
# ════════════════════════════════════════════════════════════════════
def render_sidebar(df):
    u = current_user()
    with st.sidebar:
        st.markdown(f"""
<div style="padding:1.25rem 1.25rem 0.5rem;">
  <div style="font-family:'Plus Jakarta Sans',sans-serif;font-weight:800;font-size:1.2rem;
              letter-spacing:-0.04em;
              background:linear-gradient(135deg,{C['cyan']},{C['violet']});
              -webkit-background-clip:text;-webkit-text-fill-color:transparent;
              background-clip:text;margin-bottom:0.15rem;">RETAIL IQ</div>
  <div style="font-family:'JetBrains Mono',monospace;font-size:0.57rem;color:{C['muted']};
              letter-spacing:0.15em;text-transform:uppercase;">Analytics Platform</div>
</div>""", unsafe_allow_html=True)
 
        # User card
        st.markdown(f"""
<div style="margin:0.75rem 1rem;background:{C['card']};border:1px solid {C['border']};
            border-radius:10px;padding:0.7rem 0.9rem;
            display:flex;align-items:center;gap:0.7rem;">
  <div style="width:30px;height:30px;border-radius:50%;flex-shrink:0;
              background:linear-gradient(135deg,{C['cyan']},{C['violet']});
              display:flex;align-items:center;justify-content:center;
              font-weight:700;font-size:0.8rem;color:{C['bg']};">{u['avatar']}</div>
  <div>
    <div style="font-size:0.79rem;font-weight:600;">{u['name']}</div>
    <div style="font-size:0.63rem;color:{C['muted']};">{u['plan']} Plan</div>
  </div>
</div>""", unsafe_allow_html=True)
 
        st.markdown(f"""<div style="padding:0 1rem;font-family:'JetBrains Mono',monospace;
                         font-size:0.58rem;color:{C['muted']};letter-spacing:0.13em;
                         text-transform:uppercase;margin-bottom:0.4rem;margin-top:0.5rem;">
                         FILTERS</div>""", unsafe_allow_html=True)
 
        years    = sorted(df["year"].unique().tolist())
        regions  = sorted(df["Region"].unique().tolist())
        segments = sorted(df["Segment"].unique().tolist())
        cats     = sorted(df["Category"].unique().tolist())
 
        sel_y = st.multiselect("Year",     years,    default=years,    key="f_y")
        sel_r = st.multiselect("Region",   regions,  default=regions,  key="f_r")
        sel_s = st.multiselect("Segment",  segments, default=segments, key="f_s")
        sel_c = st.multiselect("Category", cats,     default=cats,     key="f_c")
 
        st.markdown("---")
        st.markdown(f"""
<div style="padding:0 1rem;font-size:0.77rem;color:{C['muted']};line-height:1.95;">
  📦 <b style="color:{C['text']}">{len(df):,}</b> orders<br>
  👥 <b style="color:{C['text']}">{df['Customer ID'].nunique():,}</b> customers<br>
  🗓️ <b style="color:{C['text']}">{df['year'].min()}–{df['year'].max()}</b><br>
  🏷️ <b style="color:{C['text']}">{df['Product Name'].nunique():,}</b> products
</div>""", unsafe_allow_html=True)
 
        st.markdown("---")
        if st.button("Sign Out", use_container_width=True, key="signout_btn"):
            logout(); st.rerun()
 
    mask = (df["year"].isin(sel_y) & df["Region"].isin(sel_r) &
            df["Segment"].isin(sel_s) & df["Category"].isin(sel_c))
    return df[mask]
 
 
# ════════════════════════════════════════════════════════════════════
# TABS
# ════════════════════════════════════════════════════════════════════
def tab_overview(df, ms):
    ts = df["Sales"].sum(); tp = df["Profit"].sum()
    mg = tp/ts if ts else 0
    od = df["Order ID"].nunique()
    av = ts/od if od else 0
 
    yrs = sorted(df["year"].unique())
    def yoy(col):
        if len(yrs) >= 2:
            c = df[df["year"]==yrs[-1]][col].sum()
            p = df[df["year"]==yrs[-2]][col].sum()
            return round((c-p)/p*100,1) if p else None
        return None
 
    k1,k2,k3,k4 = st.columns(4)
    k1.metric("Total Revenue",  fmt_k(ts), f"{yoy('Sales'):+.1f}% YoY" if yoy("Sales") else None)
    k2.metric("Total Profit",   fmt_k(tp), f"{yoy('Profit'):+.1f}% YoY" if yoy("Profit") else None)
    k3.metric("Profit Margin",  f"{mg*100:.1f}%")
    k4.metric("Avg Order Value", fmt_k(av))
    st.markdown("<div style='height:0.25rem'></div>", unsafe_allow_html=True)
 
    c1,c2 = st.columns([2,1])
    with c1: st.plotly_chart(ch_trend(ms), use_container_width=True, config={"displayModeBar":False})
    with c2: st.plotly_chart(ch_region_pie(df), use_container_width=True, config={"displayModeBar":False})
 
    c3,c4 = st.columns(2)
    with c3: st.plotly_chart(ch_category(df), use_container_width=True, config={"displayModeBar":False})
    with c4: st.plotly_chart(ch_yoy(ms), use_container_width=True, config={"displayModeBar":False})
 
    bc = df.groupby("Category")["Profit"].sum().idxmax()
    ws = df.groupby("Sub-Category")["Profit"].sum().idxmin()
    bs = df.groupby("State")["Sales"].sum().idxmax()
    insight_box(f"""
<span style="font-family:'JetBrains Mono',monospace;font-size:0.6rem;
             text-transform:uppercase;letter-spacing:0.12em;color:{C['cyan']};">
  ⚡ AI Snapshot</span><br>
<b>{bc}</b> leads all categories in profit.&nbsp;
<b style="color:{C['red']}">{ws}</b> is the top loss-generating sub-category — review pricing.&nbsp;
<b>{bs}</b> is your highest-revenue state.&nbsp;
Average order value: <b>{fmt_k(av)}</b>.""")
 
def tab_products(df):
    c1,c2 = st.columns([3,2])
    with c1: st.plotly_chart(ch_top_products(df), use_container_width=True, config={"displayModeBar":False})
    with c2: st.plotly_chart(ch_shipmode(df), use_container_width=True, config={"displayModeBar":False})
    st.plotly_chart(ch_heatmap(df), use_container_width=True, config={"displayModeBar":False})
    st.plotly_chart(ch_discount(df), use_container_width=True, config={"displayModeBar":False})
    section("🔻 Profit Drains — Bottom 10 Sub-Categories")
    bt = df.groupby("Sub-Category").agg(
        Sales=("Sales","sum"), Profit=("Profit","sum"), Orders=("Order ID","count")
    ).nsmallest(10,"Profit").reset_index()
    bt["Margin"] = (bt["Profit"]/bt["Sales"]*100).round(1).astype(str)+"%"
    bt["Sales"]  = bt["Sales"].apply(fmt_k)
    bt["Profit"] = bt["Profit"].apply(fmt_k)
    st.dataframe(bt, use_container_width=True, hide_index=True)
 
def tab_geo(df):
    st.plotly_chart(ch_geo(df), use_container_width=True, config={"displayModeBar":False})
    c1,c2 = st.columns(2)
    with c1:
        seg = df.groupby("Segment").agg(Sales=("Sales","sum"), Profit=("Profit","sum")).reset_index()
        fig = px.bar(seg, x="Segment", y=["Sales","Profit"], barmode="group",
                     color_discrete_sequence=[C["cyan"],C["green"]])
        st.plotly_chart(theme(fig,"Revenue & Profit by Segment",300),
                        use_container_width=True, config={"displayModeBar":False})
    with c2:
        st.plotly_chart(ch_scatter_profit(df), use_container_width=True, config={"displayModeBar":False})
    section("📍 Top 15 States by Revenue")
    sg = df.groupby("State").agg(
        Sales=("Sales","sum"), Profit=("Profit","sum"), Orders=("Order ID","nunique")
    ).nlargest(15,"Sales").reset_index()
    sg["Margin"] = (sg["Profit"]/sg["Sales"]*100).round(1).astype(str)+"%"
    sg["Sales"]  = sg["Sales"].apply(fmt_k)
    sg["Profit"] = sg["Profit"].apply(fmt_k)
    st.dataframe(sg, use_container_width=True, hide_index=True)
 
def tab_forecast(df, ms):
    ms_json = ms.to_json()
    with st.spinner("Training forecast models…"):
        best_model, best_name, model_results = train_models(ms_json)
    section("🏆 Model Leaderboard")
    comp = [{"Model":n,"RMSE":f"${r['rmse']:,.0f}","MAE":f"${r['mae']:,.0f}",
              "R²":f"{r['r2']:.4f}","Best":"✅" if n==best_name else ""}
            for n,r in model_results.items()]
    st.dataframe(pd.DataFrame(comp), use_container_width=True, hide_index=True)
    insight_box(f"""
<span style="font-family:'JetBrains Mono',monospace;font-size:0.6rem;
             color:{C['violet']};text-transform:uppercase;letter-spacing:0.1em;">
  🤖 Selected Model</span><br>
<b>{best_name}</b> selected via lowest holdout RMSE.
Features: year, month, year-month composite index.""", C["violet"])
    n_months = st.slider("Forecast Horizon (months)", 3, 24, 6, key="fcast_n")
    future_df = make_forecast(best_model, ms_json, n_months)
    st.plotly_chart(ch_forecast(ms, future_df), use_container_width=True, config={"displayModeBar":False})
    section("📅 Forecast Detail")
    disp = future_df[["date","pred"]].copy()
    disp["date"] = disp["date"].dt.strftime("%b %Y")
    disp["pred"] = disp["pred"].apply(fmt_k)
    disp.columns = ["Month","Predicted Revenue"]
    st.dataframe(disp, use_container_width=True, hide_index=True)
 
def tab_customers(df):
    n_k = st.select_slider("Cluster Count", options=[3,4,5,6], value=4, key="k_n")
    with st.spinner("Running K-Means + PCA…"):
        cdf = run_clustering(df.to_json(), n_k)
    c1,c2 = st.columns(2)
    with c1: st.plotly_chart(ch_cluster(cdf), use_container_width=True, config={"displayModeBar":False})
    with c2: st.plotly_chart(ch_pca(cdf), use_container_width=True, config={"displayModeBar":False})
    section("👥 Cluster Profiles")
    prof = cdf.groupby("Cluster").agg(
        Customers=("Customer ID","count"), Avg_Revenue=("Total_Sales","mean"),
        Avg_Profit=("Total_Profit","mean"), Avg_Orders=("Num_Orders","mean"),
        Avg_Discount=("Avg_Discount","mean")
    ).reset_index()
    ic = prof["Avg_Revenue"].idxmax(); ip = prof["Avg_Profit"].idxmin()
    prof["Label"] = prof.index.map(lambda i: "🌟 Champions" if i==ic else ("⚠️ At-Risk" if i==ip else f"📦 Segment {i}"))
    prof["Avg_Revenue"]  = prof["Avg_Revenue"].apply(fmt_k)
    prof["Avg_Profit"]   = prof["Avg_Profit"].apply(fmt_k)
    prof["Avg_Discount"] = (prof["Avg_Discount"]*100).round(1).astype(str)+"%"
    prof["Avg_Orders"]   = prof["Avg_Orders"].round(1)
    st.dataframe(prof[["Label","Customers","Avg_Revenue","Avg_Profit","Avg_Orders","Avg_Discount"]],
                 use_container_width=True, hide_index=True)
    section("🏅 Top 15 Customers by Revenue")
    tc = df.groupby(["Customer ID","Customer Name","Segment"]).agg(
        Sales=("Sales","sum"), Profit=("Profit","sum"), Orders=("Order ID","nunique")
    ).nlargest(15,"Sales").reset_index()
    tc["Margin"] = (tc["Profit"]/tc["Sales"]*100).round(1).astype(str)+"%"
    tc["Sales"]  = tc["Sales"].apply(fmt_k)
    tc["Profit"] = tc["Profit"].apply(fmt_k)
    st.dataframe(tc[["Customer Name","Segment","Sales","Profit","Margin","Orders"]],
                 use_container_width=True, hide_index=True)
 
def tab_advanced(df):
    section("🔍 Anomaly Detection — Isolation Forest")
    iso = IsolationForest(contamination=0.05, random_state=42)
    scores = iso.fit_predict(df[["Sales","Profit"]].values)
    n_anom = (scores==-1).sum()
    st.plotly_chart(ch_anomaly(df), use_container_width=True, config={"displayModeBar":False})
    insight_box(f"⚠️ <b>{n_anom}</b> anomalous orders detected ({n_anom/len(df)*100:.1f}% of dataset). "
                "Review for pricing errors, fraud, or unusual returns.", C["red"])
    df2 = df.copy(); df2["Flag"] = scores
    anom_tbl = df2[df2["Flag"]==-1][["Order ID","Customer Name","Sales","Profit","Category","State"]].head(20).copy()
    anom_tbl["Sales"]  = anom_tbl["Sales"].apply(fmt_k)
    anom_tbl["Profit"] = anom_tbl["Profit"].apply(fmt_k)
    st.dataframe(anom_tbl, use_container_width=True, hide_index=True)
 
    section("🧪 Statistical Tests — Regional Sales (t-Test)")
    regions = df["Region"].unique()
    rows = []
    for i,r1 in enumerate(regions):
        for r2 in regions[i+1:]:
            t,p = stats.ttest_ind(df[df["Region"]==r1]["Sales"],df[df["Region"]==r2]["Sales"])
            rows.append({"Region A":r1,"Region B":r2,"t-stat":round(t,3),
                         "p-value":round(p,4),"Significant":"✅" if p<0.05 else "❌"})
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
    st.markdown(f"<div style='color:{C['muted']};font-size:0.77rem;margin-top:0.4rem;'>"
                "p &lt; 0.05 → statistically significant difference in mean sales.</div>",
                unsafe_allow_html=True)
 
    c1,c2 = st.columns(2)
    with c1: st.plotly_chart(ch_corr(df), use_container_width=True, config={"displayModeBar":False})
    with c2: st.plotly_chart(ch_violin(df), use_container_width=True, config={"displayModeBar":False})
 
    section("📊 Descriptive Statistics")
    desc = df[["Sales","Profit","Quantity","Discount","profit_margin","ship_lag"]].describe().T.round(3)
    st.dataframe(desc, use_container_width=True)
 
def tab_data(df):
    section("🔎 Data Explorer & Export")
    c1,c2,c3 = st.columns([3,1,1])
    with c1:
        q = st.text_input("", placeholder="Search product, customer, city…",
                          label_visibility="collapsed", key="search_q")
    with c2:
        sc = st.selectbox("", ["Sales","Profit","Quantity","Discount"],
                          label_visibility="collapsed", key="sort_c")
    with c3:
        ns = st.selectbox("", [100,250,500,1000], label_visibility="collapsed", key="n_show")
 
    disp = df.copy()
    if q.strip():
        mask = (disp["Product Name"].str.contains(q,case=False,na=False) |
                disp["Customer Name"].str.contains(q,case=False,na=False) |
                disp["City"].str.contains(q,case=False,na=False))
        disp = disp[mask]
    disp = disp.sort_values(sc, ascending=False)
    st.markdown(f"<div style='font-family:\"JetBrains Mono\",monospace;font-size:0.7rem;"
                f"color:{C['muted']};margin-bottom:0.5rem;'>{len(disp):,} records</div>",
                unsafe_allow_html=True)
    st.dataframe(disp.head(ns), use_container_width=True, hide_index=True)
    csv = disp.to_csv(index=False).encode("utf-8")
    st.download_button("⬇ Export Filtered CSV", csv, "retailiq_export.csv", "text/csv")
 
 
# ════════════════════════════════════════════════════════════════════
# UPLOAD PAGE
# ════════════════════════════════════════════════════════════════════
def render_upload_page(u):
    render_topbar(u)
    st.markdown("<div style='height:10vh'></div>", unsafe_allow_html=True)
    _, col, _ = st.columns([1,2,1])
    with col:
        st.markdown(f"""
<div style="text-align:center;margin-bottom:2rem;">
  <div style="font-size:3rem;margin-bottom:0.75rem;">📂</div>
  <div style="font-family:'Plus Jakarta Sans',sans-serif;font-weight:800;font-size:1.6rem;
              letter-spacing:-0.03em;margin-bottom:0.5rem;">Upload Your Dataset</div>
  <div style="color:{C['muted']};font-size:0.85rem;line-height:1.65;max-width:400px;margin:0 auto;">
    Upload a Superstore-format CSV to unlock the full analytics suite.
  </div>
</div>""", unsafe_allow_html=True)
        f = st.file_uploader("", type=["csv"], label_visibility="collapsed")
        if f:
            raw = f.read()
            with st.spinner("Processing dataset…"):
                st.session_state["df_raw"]   = load_data(raw)
                st.session_state["df_bytes"] = raw
            st.rerun()
 
 
# ════════════════════════════════════════════════════════════════════
# MAIN
# ════════════════════════════════════════════════════════════════════
def main():
    st.set_page_config(
        page_title="Retail IQ — Enterprise Analytics",
        page_icon="📊", layout="wide",
        initial_sidebar_state="expanded",
    )
    inject_css()
 
    if not current_user():
        render_auth_page(); st.stop()
 
    u = current_user()
 
    if "df_raw" not in st.session_state:
        render_upload_page(u); st.stop()
 
    df_raw = st.session_state["df_raw"]
    df = render_sidebar(df_raw)
 
    if len(df) == 0:
        st.warning("No data matches current filters. Adjust the sidebar filters.")
        st.stop()
 
    ms = build_monthly(df.to_json())
    render_topbar(u)
 
    tabs = st.tabs([
        "📊 Overview",
        "📦 Products",
        "🌍 Geo & Segments",
        "🤖 ML Forecast",
        "👥 Customers",
        "🧬 Advanced Analytics",
        "💬 AI Assistant",
        "🗄️ Data Explorer",
    ])
 
    with tabs[0]: tab_overview(df, ms)
    with tabs[1]: tab_products(df)
    with tabs[2]: tab_geo(df)
    with tabs[3]: tab_forecast(df, ms)
    with tabs[4]: tab_customers(df)
    with tabs[5]: tab_advanced(df)
    with tabs[6]: render_chatbot(df, ms)
    with tabs[7]: tab_data(df)
 
 
if __name__ == "__main__":
    main()
 


