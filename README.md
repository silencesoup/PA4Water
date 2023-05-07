<!--
 * @Author: Wenyu Ouyang
 * @Date: 2023-05-06 08:25:20
 * @LastEditTime: 2023-05-07 11:16:59
 * @LastEditors: Wenyu Ouyang
 * @Description: Try to build a personal assistant for water science and engineering
 * @FilePath: \PA4Water\README.md
 * Copyright (c) 2023-2024 Wenyu Ouyang. All rights reserved.
-->
# PA4Wate

This is still a developing project for using AI tools to help research and projects for water science and engineering.

## Introduction

We intend to build a personal assistant for water science and engineering, like an expert in this field.

It can help us to do some routine work, such as summarizing a research paper (pdf file). 

It can also help us to do some complex work, such as to be a software interface that could call some water-related models to do some calculations when necessary.

Now we just copy some code from [a GitHub repository](https://github.com/EnkrateiaLucca/summarization_with_langchain) and try to summarize a pdf file.

More work is still in progress and need more guys to join us.

The following technologies are used now but not fully explored jet:

- LangChain: a powerful tool for working with Large Language Models, for more information, please refer to [this blog](https://towardsdatascience.com/a-gentle-intro-to-chaining-llms-agents-and-utils-via-langchain-16cd385fca81)
- Gradio: quickly build a web interface

## Install

```bash
mamba env create -f environment.yml
```

Then copy the "config.py" file and rename it to "config_private.py"。

Set the value of the API_KEY variable in it. 

```Python
# Replace your_api_key with your actual OpenAI API key
API_KEY=your_api_key
```

## Run

Open a terminal and activate the environment you created in the previous step. Then run the following command:

```bash
conda activate PA
python pdf_summarization_app.py
```

## Development

If you want to develop this project and use VSCode as you editor, you can add a .env file in root directory and add the following content in it:

```bash
PYTHONPATH=./pa4water:./tests:${PYTHONPATH}
```

Then set environment variables in the ".vscode/setting.json" file.

```json
{
    "terminal.integrated.env.linux": { "PYTHONPATH": "${workspaceFolder}"},
    "terminal.integrated.env.windows": { "PYTHONPATH": "${workspaceFolder}"},
    "terminal.integrated.env.osx": { "PYTHONPATH": "${workspaceFolder}"},
    "python.envFile": "${workspaceFolder}/.env",
}
```