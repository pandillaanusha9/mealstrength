import streamlit as st
import pandas as pd
from datetime import date
import plotly.graph_objects as go

from auth import register, login
from utils import load_data, add_feedback, load_menu, save_menu

# ---------------- CONFIG ----------------
st.set_page_config(page_title="MealStrength", layout="centered")

# ---------------- SESSION ----------------
if "user" not in st.session_state:
    st.session_state["user"] = None

# ---------------- LOGIN / SIGNUP ----------------
if st.session_state["user"] is None:

    st.title("🍽️ MealStrength Login")

    mode = st.radio("Choose", ["Login", "Signup"])

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if mode == "Login":
        if st.button("Login"):
            if login(username, password):
                st.session_state["user"] = username
                st.rerun()
            else:
                st.error("Invalid credentials")

    else:
        if st.button("Create Account"):
            if register(username, password):
                st.success("Account created!")
            else:
                st.error("User already exists")

# ---------------- MAIN APP ----------------
else:

    st.title("🍽️ MealStrength Dashboard")
    st.write(f"Welcome **{st.session_state['user']}**")

    if st.button("Logout"):
        st.session_state["user"] = None
        st.rerun()

    menu = st.sidebar.radio("Navigation", ["Menu", "Feedback", "Analytics"])

    data = load_data()
    df = pd.DataFrame(data)

    user_df = df[df["mess_name"] == st.session_state["user"]] if not df.empty else pd.DataFrame()

    # ---------------- MENU (AUTO-SAVE NOTEPAD STYLE) ----------------
    if menu == "Menu":

        st.title("📋 Menu")

        menu_data = load_menu()

        col1, col2, col3 = st.columns(3)

        # Breakfast
        with col1:
            st.subheader("🍳 Breakfast")

            b = st.text_area(
                "Breakfast",
                value=menu_data.get("breakfast", ""),
                key="breakfast"
            )

            menu_data["breakfast"] = b
            save_menu(menu_data)

        # Lunch
        with col2:
            st.subheader("🍛 Lunch")

            l = st.text_area(
                "Lunch",
                value=menu_data.get("lunch", ""),
                key="lunch"
            )

            menu_data["lunch"] = l
            save_menu(menu_data)

        # Dinner
        with col3:
            st.subheader("🍽️ Dinner")

            d = st.text_area(
                "Dinner",
                value=menu_data.get("dinner", ""),
                key="dinner"
            )

            menu_data["dinner"] = d
            save_menu(menu_data)

    # ---------------- FEEDBACK ----------------
    elif menu == "Feedback":

        st.title("📝 Feedback")

        meal = st.selectbox("Meal", ["Breakfast", "Lunch", "Dinner"])
        taste = st.slider("Taste ⭐", 1, 5)
        hygiene = st.slider("Hygiene 🧼", 1, 5)
        comment = st.text_area("Comment")

        if st.button("Submit Feedback"):
            add_feedback({
                "mess_name": st.session_state["user"],
                "date": str(date.today()),
                "meal": meal,
                "taste": taste,
                "hygiene": hygiene,
                "comment": comment
            })

            st.success("Feedback submitted successfully!")
            st.balloons()

    # ---------------- ANALYTICS (FULL DYNAMIC MONTHLY SYSTEM) ----------------
    elif menu == "Analytics":

        st.title("📊 Monthly Analytics")

        if not user_df.empty:

            user_df["date"] = pd.to_datetime(user_df["date"])

            # Create dynamic month-year field
            user_df["month_year"] = user_df["date"].dt.strftime("%Y-%B")

            # Sort months properly (old → new order)
            available_months = sorted(
                user_df["month_year"].unique(),
                key=lambda x: pd.to_datetime(x.split("-")[0] + "-" + x.split("-")[1])
            )

            selected_month = st.selectbox(
                "Select Month",
                available_months[::-1]  # latest first
            )

            month_df = user_df[user_df["month_year"] == selected_month]

            st.subheader(f"📅 {selected_month}")

            if not month_df.empty:

                # -------- CURVE GRAPH --------
                fig = go.Figure()

                fig.add_trace(go.Scatter(
                    x=month_df.index,
                    y=month_df["taste"],
                    mode="lines+markers",
                    name="Taste"
                ))

                fig.add_trace(go.Scatter(
                    x=month_df.index,
                    y=month_df["hygiene"],
                    mode="lines+markers",
                    name="Hygiene"
                ))

                fig.update_layout(
                    title=f"Performance Curve - {selected_month}",
                    xaxis_title="Reviews",
                    yaxis_title="Rating",
                    template="plotly_dark"
                )

                st.plotly_chart(fig, use_container_width=True)

                # -------- REVIEWS TABLE --------
                st.subheader("📋 Reviews")

                st.dataframe(
                    month_df[["date", "meal", "taste", "hygiene", "comment"]]
                )

            else:
                st.info("No data for selected month")

        else:
            st.info("No feedback available yet")
