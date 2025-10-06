 **Application Functionality Description**  

 **1. Listing Management:**  
- **Creating a listing:** Users enter property details, including title, description, location, price, number of rooms, and housing type (apartment, house, etc.).  
- **Editing a listing:** Users can modify any information in an existing listing.  
- **Deleting a listing:** Users can remove their listing from the database.  
- **Managing listing availability:** Toggle listing status (active/inactive) to temporarily hide or make it visible again.  

 **2. Search and Filtering:**  
- **Keyword search:** Users enter keywords to search within listing titles and descriptions.  
- **Filtering by parameters:**  
  - Price (set minimum and maximum price).  
  - Location (specify city or district in Germany).  
  - Number of rooms (define a range).  
  - Housing type (apartment, house, studio, etc.).  
- **Sorting results:**  
  - Sort by price (ascending/descending).  
  - Sort by listing date (newest/oldest).  

 **3. User Authentication and Authorization:**  
- **User registration:** Users enter their details to create an account (name, email, password).  
- **Login:** Users enter email and password to access their account.  
- **Access control:**  
  - **Tenant:** Can browse and filter listings.  
  - **Landlord:** Can create, edit, and delete their listings.  

 **4. Booking System:**  
- **Booking creation:** Users can book a property for specific dates.  
- **Viewing bookings:** Users can see their active and completed bookings.  
- **Booking cancellation:** Users can cancel a booking before a specified deadline.  
- **Booking confirmation:** Landlords can approve or reject booking requests.  

 **5. Ratings and Reviews:**  
- **Leaving reviews:** Users who have booked a listing can leave a review and rating.  
- **Viewing reviews:** Users can see all reviews for a specific listing.  

 **✨ Additional Features:**  
- **Sorting by popularity:** Sort by number of views or reviews.  
- **Search history:**  
  - Store search keywords in a database.  
  - Display the most popular searches first.  
- **Listing view history:**  
  - Save user views of specific listings.  
  - Display the most viewed listings first.  

---

 **Technical Requirements**  
✅ **Django:** Use Django for core application logic, database management, and API creation.  
✅ **MySQL:** Main database for storing listings and user data.  

 **Additional Technologies:**  
✅ **Docker:** Use Docker for application containerization.  
✅ **AWS:** Deploy the application on AWS using services like EC2 (virtual servers) and other required tools.  

