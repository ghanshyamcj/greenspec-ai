import streamlit as st

st.set_page_config(page_title="GreenSpec AI", page_icon="🌱")

# Must match the Material column in everyday_materials_scores.xlsx exactly
MATERIALS = [
    "Steel", "Plastic (PET)", "Glass", "Aluminium", "Concrete",
    "Paper/Cardboard", "Wood", "Copper", "Brick", "Ceramic",
    "Rubber", "Cotton fabric", "Wool", "Asphalt", "Gypsum (drywall)",
]

st.title("🌱 GreenSpec AI")
st.write("Enter your product details to check how sustainable it is.")

with st.form("product_form"):
    product_name = st.text_input("Product name", placeholder="e.g. Water bottle")
    material = st.selectbox("Material it is made from", MATERIALS, index=None,
                            placeholder="Choose a material")
    manufacturing = st.text_input("How it is manufactured", placeholder="e.g. Injection moulding")
    country = st.text_input("Country it is sold in", placeholder="e.g. UAE")

    submitted = st.form_submit_button("Submit")

if submitted:
    if not all([product_name.strip(), material, manufacturing.strip(), country.strip()]):
        st.error("Please fill in all four fields.")
    else:
        # Saved so later steps (score, AI suggestions, regulations) can use it
        st.session_state["product"] = {
            "name": product_name.strip(),
            "material": material,
            "manufacturing": manufacturing.strip(),
            "country": country.strip(),
        }
        st.success("Product submitted!")
        st.write(f"**Product:** {product_name}")
        st.write(f"**Material:** {material}")
        st.write(f"**Manufacturing:** {manufacturing}")
        st.write(f"**Country:** {country}")
