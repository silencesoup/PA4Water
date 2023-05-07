"""
Author: Wenyu Ouyang
Date: 2023-05-06 09:01:36
LastEditTime: 2023-05-06 10:58:01
LastEditors: Wenyu Ouyang
Description: Summarize your PDF file using LangChain and the OpenAI API.
FilePath: \PA4Water\pdf_summarization_app.py
Copyright (c) 2023-2024 Wenyu Ouyang. All rights reserved.
"""
import gradio as gr
from langchain import OpenAI, PromptTemplate
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain.document_loaders import PyPDFLoader
import os
import toolbox

config = toolbox.get_conf('API_KEY')
os.environ["OPENAI_API_KEY"] = config[0]
# initialize LLM
llm = OpenAI(temperature=0)
text_splitter = CharacterTextSplitter()

def summarize_pdf(pdf_file_path, custom_prompt=""):
    """
    Takes a PDF file path and an optional custom prompt as input. It loads the PDF using the PyPDFLoader and splits the content into smaller parts.
    The load_summarize_chain function is then called to create a summarization chain. 
    Finally, the chain is run on the input text to generate the summary.
    """
    loader = PyPDFLoader(pdf_file_path)
    docs = loader.load_and_split()
    chain = load_summarize_chain(llm, chain_type="map_reduce")
    summary = chain.run(docs)
    if custom_prompt!="":
        prompt_template = custom_prompt + """

        {text}

        SUMMARY:"""
        PROMPT = PromptTemplate(template=prompt_template, input_variables=["text"])
        chain = load_summarize_chain(llm, chain_type="map_reduce", 
                                    map_prompt=PROMPT, combine_prompt=PROMPT)
        custom_summary = chain({"input_documents": docs},return_only_outputs=True)["output_text"]
    else:
        custom_summary = ""
    
    return summary, custom_summary


def custom_summary(pdf_file_path, custom_prompt):
    loader = PyPDFLoader(pdf_file_path)
    docs = loader.load_and_split()
    prompt_template = custom_prompt + """

    {text}

    SUMMARY:"""
    PROMPT = PromptTemplate(template=prompt_template, input_variables=["text"])
    chain = load_summarize_chain(llm, chain_type="map_reduce", 
                                map_prompt=PROMPT, combine_prompt=PROMPT)
    return chain({"input_documents": docs},return_only_outputs=True)["output_text"]
    

def main():
    """sets up the Gradio Interface, defining the input and output elements used in the interface to facilitate user interactions for entering a PDF file path.
    """
    input_pdf_path = gr.inputs.Textbox(label="Enter the PDF file path")
    input_custom_prompt = gr.inputs.Textbox(label="Enter your custom prompt")
    output_summary = gr.outputs.Textbox(label="Summary")
    output_custom_summary = gr.outputs.Textbox(label="Custom Summary")

    iface = gr.Interface(
        fn=summarize_pdf,
        inputs=[input_pdf_path,input_custom_prompt],
        outputs=[output_summary,output_custom_summary],
        title="PDF Summarizer",
        description="Enter the path to a PDF file and get its summary.",
    )
    
    iface.launch()

if __name__ == "__main__":
    main()