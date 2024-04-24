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

### Setup and Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/WeebOppa/MyBookShelf.git

2. Install the required packages:
   ```bash
   pip install -r requirements.txt

3. Run the Flask application::
   ```bash
   flask run

This project was an opportunity to explore web development using Flask and integrating third-party APIs. It posed challenges such as managing user sessions, interacting with external APIs, and ensuring responsive design, all of which were addressed during development.
