import streamlit as st
from transformers import pipeline
import torch

pipe = pipeline("text-generation", model="TinyLlama/TinyLlama-1.1B-Chat-v1.0", torch_dtype=torch.bfloat16, device_map="auto")

def returnUserResponse(prompt):
    return f"<|user|>{prompt}\n</s>\n<|assistant|>"

def returnAssistantResponse(response):
    return f"{response}\n</s>\n"


# Ensure session state variables are initialized
if "inference_messages" not in st.session_state:
    st.session_state["inference_messages"] = [
        {
            "role": "system",
            "content": "You are a friendly mental therapist.",
        }
    ]

st.title("Free Tiny Therapist🧑‍⚕️")

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({"role": "assistant", "content": "Hi, I'm here to listen. Feel free to share anything you'd like. Please note, I am running on CPU, so it may take a bit of time for me to respond"})



for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# user input
if user_prompt := st.chat_input("Your prompt"):
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    st.session_state["inference_messages"].append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    # generate responses
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        prompt = pipe.tokenizer.apply_chat_template(st.session_state["inference_messages"], tokenize=False, add_generation_prompt=True)
        print("prompt ",prompt)
        outputs = pipe(prompt, max_new_tokens=100, do_sample=True, temperature=0.7, top_k=50, top_p=0.95)
        response=outputs[0]["generated_text"]
        print("reponse ",response)
        start = response.rfind("<|assistant|>") 
        assistant_response = response[start + len("<|assistant|>"):]

        full_response=assistant_response
        st.session_state["inference_messages"].append({"role": "assistant", "content": full_response})
        print("messages ",st.session_state["inference_messages"])

        message_placeholder.markdown(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})