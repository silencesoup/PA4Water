import os

from langchain import OpenAI
import toolbox

config = toolbox.get_conf('API_KEY')
os.environ["OPENAI_API_KEY"] = config[0]
# initialize LLM
llm = OpenAI(temperature=0)