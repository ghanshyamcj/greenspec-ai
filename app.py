import pandas as pd
import streamlit as st

st.set_page_config(page_title="GreenSpec AI", page_icon="🌱")

# ---------------------------------------------------------------
# Data source
# To read straight from your Google Sheet: in Sheets go to
# File > Share > Publish to web > choose the sheet > CSV, then paste
# the link below. Leave it empty to use materials.csv in this folder.
# The sheet must keep the same 4 columns in the same order.
# ---------------------------------------------------------------
SHEET_CSV_URL = ""

# How much each factor counts towards the final score (adds up to 1)
WEIGHTS = {"carbon": 0.4, "recycling": 0.3, "energy": 0.3}


@st.cache_data
def load_materials():
    df = pd.read_csv(SHEET_CSV_URL or "materials.csv")
    df.columns = ["material", "carbon", "recycling", "energy"]
    df["material"] = df["material"].str.strip()
    return df.set_index("material")


def sustainability_score(carbon, recycling, energy):
    """Return a score from 1 to 10 where higher means greener.

    In the sheet, a HIGH carbon or energy number is BAD, so those two are
    flipped (11 - value) first. Recycling is already "higher is better".
    """
    parts = {
        "Low carbon": 11 - carbon,
        "Recyclability": recycling,
        "Low energy": 11 - energy,
    }
    total = (
        parts["Low carbon"] * WEIGHTS["carbon"]
        + parts["Recyclability"] * WEIGHTS["recycling"]
        + parts["Low energy"] * WEIGHTS["energy"]
    )
    return round(total, 1), parts


materials = load_materials()

st.title("🌱 GreenSpec AI")
st.write("Enter your product details to check how sustainable it is.")

with st.form("product_form"):
    product_name = st.text_input("Product name", placeholder="e.g. Water bottle")
    material = st.selectbox("Material it is made from", materials.index.tolist(),
                            index=None, placeholder="Choose a material")
    manufacturing = st.text_input("How it is manufactured", placeholder="e.g. Injection moulding")
    country = st.text_input("Country it is sold in", placeholder="e.g. UAE")

    submitted = st.form_submit_button("Submit")

if submitted:
    if not all([product_name.strip(), material, manufacturing.strip(), country.strip()]):
        st.error("Please fill in all four fields.")
    else:
        row = materials.loc[material]
        score, parts = sustainability_score(row["carbon"], row["recycling"], row["energy"])

        # Saved so later steps (AI suggestions, regulations) can use it
        st.session_state["product"] = {
            "name": product_name.strip(),
            "material": material,
            "manufacturing": manufacturing.strip(),
            "country": country.strip(),
            "score": score,
        }

        st.subheader(f"Results for {product_name.strip()}")
        st.write(f"**Material:** {material} · **Made by:** {manufacturing} · **Sold in:** {country}")

        if score >= 7:
            label = "🟢 Good"
        elif score >= 4.5:
            label = "🟡 Average"
        else:
            label = "🔴 Poor"
        st.metric("Sustainability score", f"{score} / 10", label, delta_color="off")

        st.write("**Score breakdown** (higher is better for all three)")
        chart = pd.DataFrame({"Score (1-10)": parts})
        st.bar_chart(chart)
