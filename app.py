import streamlit as st
import smtplib
from langchain.prompts import PromptTemplate
from langchain_community.llms import CTransformers
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email(sender_email, receiver_email,App_password, subject, body):
    try:
        # Set up SMTP server

        with smtplib.SMTP('smtp.gmail.com', 587) as smtp_server:
            smtp_server.starttls()
            smtp_server.login(sender_email, App_password)
            # Create email message
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = receiver_email
            msg['Subject'] = subject

            msg.attach(MIMEText(body, 'plain'))

            # Send the email
            smtp_server.sendmail(sender_email, receiver_email, msg.as_string())

        st.success("Email Sent Successfully!")
    except Exception as e:
        st.error(f"Error Sending Email: {e}")

# Function to get the response back
def getLLMResponse(form_input, email_sender, email_recipient, email_style):
    # llm = OpenAI(temperature=.9, model="text-davinci-003")

    # Wrapper for Llama-2-7B-Chat, Running Llama 2 on CPU

    # Quantization is reducing model precision by converting weights from 16-bit floats to 8-bit integers,
    # enabling efficient deployment on resource-limited devices, reducing model size, and maintaining performance.

    # C Transformers offers support for various open-source models,
    # among them popular ones like Llama, GPT4All-J, MPT, and Falcon.

    # C Transformers is the Python library that provides bindings for transformer models implemented in C/C++ using the GGML library

    llm = CTransformers(model='models/llama-2-7b-chat.ggmlv3.q8_0.bin',
                        # https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGML/tree/main
                        model_type='llama',
                        config={'max_new_tokens': 256,
                                'temperature': 0.01},

                        )

    # Template for building the PROMPT
    template = """
    Write a email with {style} style and includes topic :{email_topic}.\n\nSender: {sender}\nRecipient: {recipient}
    \n\nEmail Text:

    """

    # Creating the final PROMPT
    prompt = PromptTemplate(
        input_variables=["style", "email_topic", "sender", "recipient"],
        template=template, )

    # Generating the response using LLM
    response = llm.invoke(
        prompt.format(email_topic=form_input, sender=email_sender, recipient=email_recipient, style=email_style))
    print(response)

    return response


st.set_page_config(page_title="Generate Emails",
                   page_icon='📧',
                   layout='centered',
                   initial_sidebar_state='collapsed')
st.header("Generate Emails 📧")

form_input = st.text_area('Enter the email topic', height=275)

# Creating columns for the UI - To receive inputs from user
col1, col2, col3 = st.columns([10, 10, 5])
with col1:
    email_sender = st.text_input('Sender Name',key='Sender Name')
with col2:
    email_recipient = st.text_input('Recipient Name',key='Recipient Name')
with col3:
    email_style = st.selectbox('Writing Style',
                               ('Formal', 'Appreciating', 'Not Satisfied', 'Neutral'),
                               index=0)
submit = st.button("Generate")
send_button = st.button("Send Email")
# When 'Generate' button is clicked, execute the below code
generate_response = ""
sender_email = "mysteryverse9@gmail.com"

if submit:
    generate_response = getLLMResponse(form_input, email_sender, email_recipient, email_style)
    st.write(generate_response)

# Execute the below code only once
if send_button:

    receiver_email = st.text_input("Please enter the recipient's email address:")
    subject = form_input
    generate_response = getLLMResponse(form_input, email_sender, email_recipient, email_style)
    body = generate_response
    App_password = "dgwl zypu jegs xwiq"

    send_email(email_sender, receiver_email , App_password, subject, body)