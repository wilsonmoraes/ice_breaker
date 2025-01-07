import re

from dotenv import load_dotenv
from langchain.prompts.prompt import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

from third_parties.linkedin import scrape_linkedin_profile

if __name__ == "__main__":
    load_dotenv()

    print("Hello LangChain")

    summary_template = """
    given the Linkedin information {information} about a person I want you to create in portuguese:
    1. A short summary
    2. two interesting facts about them
    """

    summary_prompt_template = PromptTemplate(
        input_variables=["information"], template=summary_template
    )

    llm = ChatOpenAI(temperature=0, model_name="gpt-4o-mini")

    chain = summary_prompt_template | llm
    linkedin_data = scrape_linkedin_profile(
        linkedin_profile_url="https://www.linkedin.com/in/alexandre-mota-a8119896/"
    )
    parser = StrOutputParser()

    res = parser.parse(chain.invoke(input={"information": linkedin_data}))
    match = re.search(r"content='(.*?)'", str(res), re.DOTALL)
    formatted_output = match.group(1)
    print(formatted_output)
