import streamlit as st  # Import Streamlit for building the web app
from langchain_community.document_loaders import WebBaseLoader  # Import for loading web-based documents
from chains import Chain  # Import the custom Chain class for LLM operations
from portfolio import Portfolio  # Import the Portfolio class for querying portfolio links
from utils import clean_text  # Import a utility function to clean raw web text

# Page-wide settings - MUST be the first Streamlit command
st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")

# Function to create the main Streamlit app
def create_streamlit_app(llm, portfolio, clean_text):
    # Page title with emoji icon and style
    st.title("📧 Cold Mail Generator")
    
    # Add some description text with better styling using custom HTML and CSS
    st.markdown("""
    <style>
    .intro-text {
        font-size: 18px;
        color: #4F4F4F;
        text-align: center;
        margin-bottom: 30px;
    }
    </style>
    <div class="intro-text">
        Generate personalized cold emails to match job descriptions with your skills.
    </div>
    """, unsafe_allow_html=True)

    # URL input with wider text box and placeholder
    url_input = st.text_input("🔗 Enter a Job URL to Analyze:", placeholder="e.g., https://jobs.nike.com/job/...", max_chars=200)
    
    # Display the URL entered by the user if available
    if url_input:  # Check if user entered a URL
        st.markdown(f"<div style='color:green;'>URL entered: <b>{url_input}</b></div>", unsafe_allow_html=True)
    
    # Add submit button with a little padding for generating the cold email
    submit_button = st.button("🚀 Generate Email")
    
    # Show loading spinner when processing the email generation
    if submit_button:
        with st.spinner('Analyzing the job post and generating an email...'):
            try:
                # Load the job data from the URL using WebBaseLoader
                loader = WebBaseLoader([url_input])
                data = clean_text(loader.load().pop().page_content)  # Clean the raw page content
                
                # Load the portfolio and extract job information from the job page
                portfolio.load_portfolio()
                jobs = llm.extract_jobs(data)
                
                # Display the subheader for the email generation result
                st.subheader("Generated Email")
                
                # Display email output for each extracted job
                for job in jobs:
                    skills = job.get('skills', [])  # Extract skills from the job data
                    links = portfolio.query_links(skills)  # Query portfolio links based on skills
                    email = llm.write_mail(job, links)  # Generate the cold email using the LLM
                    
                    # Code block for email, styled as markdown
                    st.code(email, language='markdown')

            except Exception as e:
                # If an error occurs, display an error message to the user
                st.error(f"An error occurred: {e}")

# Custom CSS for global styling, including layout width adjustments and custom button/text input styles
st.markdown("""
    <style>
    .stButton button {
        background-color: #4CAF50;
        color: white;
        font-size: 16px;
        padding: 10px 24px;
        border-radius: 12px;
    }

    .stTextInput>div>input {
        border-radius: 8px;
        padding: 10px;
        font-size: 16px;
    }

    .stMarkdown {
        background-color: #f9f9f9;
        padding: 10px;
        border-left: 5px solid #0366d6;
        border-radius: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# Main execution block
if __name__ == "__main__":
    chain = Chain()  # Instantiate the Chain class to handle LLM and job extraction
    portfolio = Portfolio()  # Instantiate the Portfolio class for handling portfolio links
    
    # Call the main Streamlit app function with required objects
    create_streamlit_app(chain, portfolio, clean_text)




