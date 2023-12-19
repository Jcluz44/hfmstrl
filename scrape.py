# Import subprocess to run pip commands
import subprocess
import sys

# Function to install required packages
def install_packages():
    subprocess.check_call([sys.executable, "-m", "pip", "install", "streamlit"])
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
    subprocess.check_call([sys.executable, "-m", "pip", "install", "beautifulsoup4"])
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests-html"])

# Run the install function
install_packages()

# Import necessary libraries
import streamlit as st
from bs4 import BeautifulSoup
from requests_html import HTMLSession

# Streamlit app layout
def streamlit_app():
    st.title("Audio Transcription Scraper")

    # Input field for the URL
    url = st.text_input("Enter the URL of the website to scrape:")

    # Button to start scraping
    if st.button("Scrape") and url:
        scraped_data = scrape_website(url)
        if scraped_data:
            st.write(scraped_data)
        else:
            st.error("No transcription found or unable to scrape the website.")

# Function to scrape the website
def scrape_website(url):
    session = HTMLSession()
    response = session.get(url)

    if response.status_code == 200:
        response.html.render()
        soup = BeautifulSoup(response.content, 'html.parser')
        transcription_container = soup.find(class_="transcription-container")

        if transcription_container:
            return transcription_container.get_text(strip=True)
    return None

# Main execution for Streamlit app
if __name__ == "__main__":
    streamlit_app()
