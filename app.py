import os
from typing import Optional, Tuple
from threading import Lock

import gradio as gr

from query_model import get_model
import openai
            
def set_openai_api_key(api_key: str):
    """Set the api key and return chain.
    If no api_key, then None is returned.
    """
    if api_key:
        os.environ["OPENAI_API_KEY"] = api_key
        chain = get_model()
        os.environ["OPENAI_API_KEY"] = ""
        return chain


class ChatWrapper:

    def __init__(self):
        self.lock = Lock()

    def __call__(
        self, api_key: str, inp: str, history: Optional[Tuple[str, str]], chain
    ):
        """Execute the chat functionality."""
        self.lock.acquire()
        try:
            history = history or []
            # If chain is None, that is because no API key was provided.
            if chain is None:
                history.append((inp, "Please paste your encrypted key to use"))
                return history, history
            # Set OpenAI key
            import openai
            openai.api_key = api_key
            # Run chain and append input.
            output = chain({"question": inp})["answer"]
            history.append((inp, output))
        except Exception as e:
            raise e
        finally:
            self.lock.release()
        return history, history

chat = ChatWrapper()

block = gr.Blocks(css=".gradio-container {font-weight: bold; \
background-image: url('https://png.pngtree.com/png-vector/20230728/ourmid/pngtree-aster-clipart-purple-chrysanthemum-drawing-cartoon-vector-png-image_6798181.png'); background-size: 20%; \
background-color: pink} footer {visibility: hidden} #ex {background-color:white; padding: 5px;}")

with block:
    with gr.Row():
        gr.Markdown("<h1 style='font-family: noto-san; font-size: 60px;'><center>Utsumi Bunzō </center></h1>")

        openai_api_key_textbox = gr.Textbox(
            placeholder="Paste your special key (sk-...)",
            show_label=False,
            lines=1,
            type="password",
        )

    gr.HTML("<br> <br>")
    chatbot = gr.Chatbot(label="Bunzō")

    with gr.Row():
        message = gr.Textbox(
            label="Talk to Bunzō",
            placeholder="Ask questions",
            lines=1,
        )
        submit = gr.Button(value="Send", variant="secondary")

    gr.Examples(
        examples=[
            "Who are you?",
            "How do you feel?",
            "What are some important things to you?",
        ],
        inputs=message,
        elem_id= "ex"
    )


    gr.HTML("<br> <br> <br> <br> <br> <br> <br> <br>\
    <center><strong> Copyright @ Sammy Kao 2023</strong></center>")

    state = gr.State()
    agent_state = gr.State()


    submit.click(chat, inputs=[openai_api_key_textbox, message, state, agent_state], outputs=[chatbot, state])
    submit.click(lambda x: gr.update(value=""), None, [message], queue=False)
    message.submit(chat, inputs=[openai_api_key_textbox, message, state, agent_state], outputs=[chatbot, state])
    message.submit(lambda x: gr.update(value=""), None, [message], queue=False)

    openai_api_key_textbox.change(
        set_openai_api_key,
        inputs=[openai_api_key_textbox],
        outputs=[agent_state],
    )
    

block.launch(debug=True)