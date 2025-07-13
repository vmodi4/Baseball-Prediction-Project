import streamlit as st
import pandas as pd
import numpy as np

message  = st.chat_message("Assistant")
message.write("Hello human")
message.bar_chart(np.random.randn(30, 3))


