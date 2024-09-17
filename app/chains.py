import os
from langchain_groq import ChatGroq  # Import the ChatGroq class for handling LLM interactions.
from langchain_core.prompts import PromptTemplate  # Import for creating prompts for the LLM.
from langchain_core.output_parsers import JsonOutputParser  # Import to handle JSON output parsing.
from langchain_core.exceptions import OutputParserException  # Import to handle exceptions in case the output parsing fails.
from dotenv import load_dotenv  # Import for loading environment variables from a .env file.

# Load environment variables (specifically GROQ_API_KEY) from a .env file.
load_dotenv()

# Define a class `Chain` which will encapsulate the logic for job extraction and email writing.
class Chain:
    def __init__(self):
        # Initialize the LLM (ChatGroq) using the API key from environment variables.
        self.llm = ChatGroq(temperature=0, groq_api_key=os.getenv("GROQ_API_KEY"), model_name="llama-3.1-70b-versatile")

    # Function to extract job postings from the given cleaned text.
    def extract_jobs(self, cleaned_text):
        # Define a prompt template for job extraction with specific keys to be returned.
        prompt_extract = PromptTemplate.from_template(
            """
            ### SCRAPED TEXT FROM WEBSITE:
            {page_data}
            ### INSTRUCTION:
            The scraped text is from the career's page of a website.
            Your job is to extract the job postings and return them in JSON format containing the following keys: `role`, `experience`, `skills` and `description`.
            Only return the valid JSON.
            ### VALID JSON (NO PREAMBLE):
            """
        )
        # Chain the prompt with the LLM to generate the extraction request.
        chain_extract = prompt_extract | self.llm
        # Invoke the LLM with the cleaned page data to get the job extraction.
        res = chain_extract.invoke(input={"page_data": cleaned_text})
        try:
            # Parse the output using the JSON parser to ensure valid JSON format.
            json_parser = JsonOutputParser()
            res = json_parser.parse(res.content)
        except OutputParserException:
            # Raise an exception if the output cannot be parsed as JSON (e.g., if it's too large).
            raise OutputParserException("Context too big. Unable to parse jobs.")
        # Return the result; if it's not a list, wrap it in a list.
        return res if isinstance(res, list) else [res]

    # Function to write a cold email for a given job posting and portfolio links.
    def write_mail(self, job, links):
        # Define a prompt template for writing a cold email based on the job description.
        prompt_email = PromptTemplate.from_template(
            """
            ### JOB DESCRIPTION:
            {job_description}

            ### INSTRUCTION:
            
            I am  Neeraj Reddy, currently pursuing masters in information technology and analytics. I am on the lookout for an full time opportunity where I wanted to apply my data engineer skills and passion for developing impactful data solutions to tackle real-world business challenges.
            I had 2 years of experience in architecting the data into relational data marts and led the development of various ETL pipelines and data visualization for multiple projects, including building batch and real-time data pipelines using AWS & Azure services.
            I had Hands-on experience with Python, SQL, Data Warehouses, Data Modeling, CI/CD pipelines, Spark, PySpark, and cloud data engineering that have reduced data processing latency and improved operational efficiency.
            Also I had a year of experience in Volvo trucks as a product analyst where I studied the market dynamics of new growth segments in construction business across geographies leveraging SAS for identifying potential customers. I analyzed the granularity of the data across the business and map the best potential customers in the vast sea of opportunities.
            Over My experience, I have empowered numerous enterprises with tailored solutions, fostering scalability, 
            process optimization, cost reduction, and heightened overall efficiency. 
            
            Your job is to write a cold email to the recuriting manager regarding the job mentioned above describing the capability of my data engineering skills
            in fulfilling their needs.
            
            Also add the most relevant ones from the following links to showcase Neeraj's portfolio: {link_list}
            Remember you are Neeraj Reddy, Data Engineer.
            Do not provide a preamble.
            ### EMAIL (NO PREAMBLE):

            """
        )
        # Chain the prompt with the LLM to generate the email request.
        chain_email = prompt_email | self.llm
        # Invoke the LLM with the job description and portfolio links to generate the email.
        res = chain_email.invoke({"job_description": str(job), "link_list": links})
        # Return the generated email content.
        return res.content

# Main block to print the GROQ_API_KEY for validation or debugging purposes.
if __name__ == "__main__":
    print(os.getenv("GROQ_API_KEY"))
