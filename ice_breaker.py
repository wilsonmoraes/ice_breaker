import re

from dotenv import load_dotenv
from langchain.prompts.prompt import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

from third_parties.linkedin import scrape_linkedin_profile
from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agend


def ice_break_with_agent(name: str) -> str:
    linkedin_profile_username = linkedin_lookup_agend(name)
    linkedin_data = scrape_linkedin_profile(
        linkedin_profile_url=linkedin_profile_username
    )

    summary_template = """
        given the Linkedin information {information} about a person I want you to create in portuguese:
        1. A short summary
        2. list the negative points of his profile
        """

    summary_prompt_template = PromptTemplate(
        input_variables=["information"], template=summary_template
    )

    llm = ChatOpenAI(temperature=0, model="gpt-4o-mini")

    chain = summary_prompt_template | llm

    parser = StrOutputParser()

    res = parser.parse(chain.invoke(input={"information": linkedin_data}))
    match = re.search(r"content='(.*?)'", str(res), re.DOTALL)
    formatted_output = match.group(1)
    return formatted_output


if __name__ == "__main__":
    load_dotenv()

    print("Hello LangChain")

    ice_break_agent_wilson = ice_break_with_agent(name="Wilson Moraes dos Santos")

    print(ice_break_agent_wilson)
