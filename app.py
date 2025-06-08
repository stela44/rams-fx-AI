import streamlit as st
from PIL import Image
import openai
import io
import base64

# Load your OpenAI key from Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Streamlit page settings
st.set_page_config(page_title="Forex Chart Analyzer", layout="centered")

st.title("📈 Forex Screenshot Analyzer")

st.markdown(
    "Upload a screenshot of your forex chart, and get the **Pair**, **Timeframe**, **Signal**, **Reason**, and **Caution**."
)

# Upload image
uploaded_file = st.file_uploader("Upload your chart screenshot", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Chart", use_column_width=True)

    with st.spinner("Analyzing chart..."):
        # Convert image to base64 string
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()

        # Call OpenAI GPT-4 with Vision to analyze chart
        response = openai.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=[
                {"role": "system", "content": "You are a professional forex trading assistant."},
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Analyze this forex chart screenshot and extract:\\n- Pair\\n- Timeframe\\n- Signal (Buy/Sell)\\n- Reason\\n- Caution"
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{img_str}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=500
        )

        # Show result
        result = response.choices[0].message.content
        st.markdown("### 🧾 Analysis Result")
        st.markdown(result)
