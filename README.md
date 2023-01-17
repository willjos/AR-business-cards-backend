# AR-business-cards-backend

Repo containing API for AR-business-cards project.

## BASE URL

'https://ar-business-cards-backend.herokuapp.com/'

## Endpoints

'/' - GET request that displays raw JSON of all users database entries currently - this will be changed to a welcome message on for final product.

'/getUserQR' - GET request that takes query parameter 'username', returns raw JSON of provided user's card ids. These will be converted into QR codes that can be scanned to access the AR business cards.

'/view-card/<int:id>' - POST request that takes path parameter id and receives a username in the request body, returns raw JSON of the business card data associated with the corresponding card id from the database. This information will be converted into an AR business card that can be viewed by the user. An entry is also added to the collected table in the collected where all scans of cards are recorded for users.

'/view-collection' - POST request that receives a username and returns raw JSON about all of the cards that user has scanned that are not their own

'/create-card' - POST request that receives JSON containing username, title, colour, and content values and adds a card entry to the database. This will be used to store all business cards that are created by users.

'/edit-card/<int:id>' - PATCH request that takes path parameter id, and edits the content of the card based on JSON data supplied by the frontend.

'/register-user' - POST request that receives JSON containing username and password. This will add a new user to the database (usernames must be unique).

'/login' - POST request that receives JSON containing username and password. This will check if the username and password match an existing user entry in the database and either allow or deny permission to the site.
