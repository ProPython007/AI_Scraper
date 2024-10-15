import time
import streamlit as st
from selenium import webdriver
from parse import parse_with_ollama
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from scrape import extract_body_content, clean_body_content, split_dom_content



# Settings:
## Extra CSS:
st.set_page_config(page_title='SrapeMeAI', page_icon=':computer:', layout='wide')
hide_st_style = '''
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
    </style>
'''
st.markdown(hide_st_style, unsafe_allow_html=True)
st.title('ScrapeMeAI')


# Initialize Selenium WebDriver
def create_browser():
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")  # Uncomment this line to run in headless mode
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver


url = st.text_input("Enter Starting URL (default: google)")
if st.button("Open Browser"):
    driver = create_browser()
    st.session_state.driver = driver  # Store the driver in the session state
    if not url:
        url = "https://www.google.com"
    driver.get(url)  # You can change this to the desired URL
    st.success("Browser Opened! Navigate to Your Desired Website!")

# Button to get content
if st.button("Scrape Content"):
    st.write('Scraping...')
    if "driver" in st.session_state:
        time.sleep(1)  # Wait for a moment to ensure the page is fully loaded
        html_content = st.session_state.driver.page_source  # Get the HTML content
        st.session_state.driver.quit()  # Close the browser
        clean_content = clean_body_content(extract_body_content(html_content))
        st.session_state.dom_content = clean_content
        st.success("Content Retrieved!")
        
        with st.expander('View DOM Content'):
            st.text_area('DOM Content', clean_content, height=300)
    else:
        st.warning("Please Open The Browser First!")


if 'dom_content' in st.session_state:
    parse_description = st.text_area('Describe what you want to parse?')
    
    if st.button('Parse Content'):
        if parse_description:
            st.write('Parsing the content...')
            
            dom_chunks = split_dom_content(st.session_state.dom_content)
            parsed_result = parse_with_ollama(dom_chunks, parse_description)
            st.write(parsed_result)