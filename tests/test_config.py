"""
Author: Wenyu Ouyang
Date: 2023-05-07 10:05:11
LastEditTime: 2023-05-07 11:26:25
LastEditors: Wenyu Ouyang
Description: Test functions
FilePath: \PA4Water\tests\test_config.py
Copyright (c) 2023-2024 Wenyu Ouyang. All rights reserved.
"""
import os
from langchain import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import PALChain
import pytest
import sys
from pathlib import Path


sys.path.append(str(Path(__file__).parent.parent))
from pa4water import toolbox


@pytest.fixture(scope="session", autouse=True)
def config():
    config = toolbox.get_conf("API_KEY")
    os.environ["OPENAI_API_KEY"] = config[0]


def test_generic_chain():
    # one prompt, one response
    prompt = PromptTemplate(
        input_variables=["product"],
        template="What is a good name for a company that makes {product}?",
    )
    print(prompt.format(product="podcast player"))
    llm = OpenAI(
        model_name="text-davinci-003", temperature=0.9  # default model
    )  # temperature dictates how whacky the output should be
    llmchain = LLMChain(llm=llm, prompt=prompt)
    llmchain.run("podcast player")


def test_utility_chain():
    llm = OpenAI(model_name="text-davinci-003", temperature=0.9)
    palchain = PALChain.from_math_prompt(llm=llm, verbose=True)
    palchain.run(
        "If my age is half of my dad's age and he is going to be 60 next year, what is my current age?"
    )
