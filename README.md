# YOUR PROJECT TITLE: MyBookShelf

#### Video Demo: [Watch Here](https://www.youtube.com/watch?v=Budv6iHtVNo)
#### Description:
MyBookShelf is a web application designed to help book enthusiasts manage their personal book collections digitally. It integrates with the Google Books API to allow users to search for books, add them to their personal library, and view detailed information about each title. The application supports individual user accounts, enabling users to maintain personalized libraries securely.

### Key Features
- **User Authentication:** Implements a secure login and registration system to manage individual user accounts.
- **Search Functionality:** Users can search for books based on title, author, ISBN, and other criteria using the Google Books API, which returns comprehensive results including book cover images, publication details, and more.
- **Personal Library:** Users can save their favorite books to their personal library for easy access at any time. This feature allows them to quickly retrieve their favorite reads and maintain a collection of books they are interested in.
- **Book Details:** Provides detailed information for each book, such as synopsis, author bio, publication date, and additional metadata provided by the Google Books API.
- **Mobile Responsive:** Designed to provide a consistent and accessible user experience across various devices, ensuring that users can manage their library on the go.

### Technologies Used
- **Frontend:** HTML5, CSS3, Bootstrap for responsive design, and JavaScript for dynamic interactions.
- **Backend:** Flask, a lightweight WSGI web application framework in Python, used to handle requests, server-side logic, and interactions with the Google Books API.
- **Database:** SQLite, a lightweight disk-based database to store user data and book information.
- **APIs:** Google Books API, which provides the data used to search for books and retrieve metadata.

This project was an opportunity to explore web development using Flask and integrating third-party APIs. It posed challenges such as managing user sessions, interacting with external APIs, and ensuring responsive design, all of which were addressed during development.

### Setup and Installation
The following instructions will guide you through setting up and running the MyBookShelf application on your local machine. These steps assume you have a basic understanding of command line operations and Python environments.

#### Prerequisites
- **Python:** The application is written in Python, so you'll need Python 3.7 or later installed on your computer. You can download it from [python.org](https://www.python.org/downloads/).
- **Git:** To clone the project repository, you'll need Git installed. If you don't have Git, you can download it from [git-scm.com](https://git-scm.com/downloads).
- **Pip:** Ensure that pip is installed, as it will be used to install the Python packages needed for the application.

#### Step-by-step Installation

1. **Clone the repository:**
   Use Git to clone the project's repository into a directory of your choice on your local machine:
   ```bash
   git clone https://github.com/WeebOppa/MyBookShelf.git
   cd MyBookShelf

2. **Setup a virtual environment (optional but recommended):**
   It's a good practice to use a virtual environment to isolate package dependencies. To set up a virtual environment, run:
   ```bash
   python -m venv venv
   # Activate the virtual environment
   # On Windows:
   venv\Scripts\activate
   # On macOS and Linux:
   source venv/bin/activate

3. **Install dependencies:**
   Once your virtual environment is activated, you can install the project dependencies listed in requirements.txt:
   ```bash
   pip install -r requirements.txt

4. **Environment Configuration:**
    Set up the necessary environment variables. You'll need to provide your own API key for the Google Books API. This should be added to your environment variables or directly into your configuration file:
    ```bash
    export GOOGLE_BOOKS_API_KEY='your_api_key_here'

5. **Initialize the database:**
    Before running the application, you need to set up the database:
    ```bash
    flask db upgrade

6. **Run the Flask application:**
    Now, you're ready to run the application. Execute the following command to start the Flask
    ```bash
    flask run
    This command will start the local server on http://127.0.0.1:5000/, and you can access the web application by navigating to this URL in your web browser.
