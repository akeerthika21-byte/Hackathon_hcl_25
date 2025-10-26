1. Overview
   
   The Bank Account Creation enables users to seamlessly open new bank accounts digitally through a secure and automated backend system.It simplifies the onboarding process by allowing customers to submit essential information such as name, contact details, identification numbers (Aadhaar, PAN), and preferred account type.

   Once submitted, the API performs necessary validations — such as checking for duplicate accounts, verifying ID formats, and ensuring a minimum deposit amount — before creating a new account record.

   It then generates a unique account number, links it to the corresponding customer profile, and returns confirmation details including IFSC code, customer ID, and account creation timestamp.

2. Endpoint
   
    POST /api/accounts/create/
   
3. Description
   
	Creates a new bank account for an existing or new customer.The API validates user information (name, ID, email, etc.), assigns an account number, and stores account details in the database.

4. Tech Stack - Python, Django, MySQL

5. Request Body

     {
      
      "customer_id": 1,
      
      "account_type": "Savings",
      
      "initial_deposit": 5000,
      
      "branch_code": "CHN001",
   
    }

7. Sample successful response

      {
      
        "message": "Account created successfully.",
        
        "account_number": "SBI0001",
        
        "ifsc_code": "BANK0001234",
        
        "customer_id": "CUST98765",
        
        "created_at": "2025-10-15 10:34:21"
        
      }


8. Sample error responses

    Status: 400 Bad request 

        {
        
        "error": "Invalid Aadhaar number format."
        
        }

    Status: 500 Internal server error

        {
        
         "error": "Something went wrong while creating the account"
         
        }

9. Database
    
    Customer table
	
        Customer_id	: Int (PK)
        
        first_name : varchar(100)
        
        last_name : varchar(100)
        
        email : varchar(150)
        
        phone_number : varchar(10)

   		address : varchar(255)
        
        aadhar_number : varchar(12)
        
        pan_number : varchar(10)
        
        created_at : Datetime


    Bank Account table

        account_id : Int (PK)
        
        account_no : varchar(20)
        
        customer_id : Int (FK)
        
        account_type : varchar(50)
        
        branch_name : varchar(100)
        
        balance : Decimal(12,2)
        
        status: varchar(20)
        
        created_at : Datetime

    Transaction table

        transaction_id : Int (PK)
        
        account_id : Int(FK)
        
        transaction_type : varchar(20)
        
        amount : decimal(12,2)
        
        transaction_date : Datetime
   
Test case:

Test successful account creation

•	Input: Valid customer_id, account_type='Savings', initial_deposit=5000, branch_name='Main Branch'

•	Expected: Status 200 OK, message "Account created successfully", valid account_number in response

Test missing required fields

•	Input: Missing one or more fields (e.g., no branch_name)

•	Expected: Status 400 BAD REQUEST, message "All fields are required."

Test invalid customer ID (non-numeric)

•	Input: customer_id='abc'

•	Expected: Status 400 BAD REQUEST, message "Invalid customer ID."

Test non-existent customer

•	Input: customer_id not found in database

•	Expected: Status 404 NOT FOUND, message "Customer not found"

Test invalid account type

•	Input: account_type='Fixed'

•	Expected: Status 400 BAD REQUEST, message "Invalid account type"

Test deposit below minimum amount

•	Input: initial_deposit=500

•	Expected: Status 400 BAD REQUEST, message "Minimum initial deposit is ₹1000.00."

Test invalid deposit value (string instead of number)

•	Input: initial_deposit='abc'

•	Expected: Status 400 BAD REQUEST, message "Invalid deposit amount."

Test account number uniqueness

•	Input: Same customer_id, different request

•	Expected: New, unique 12-digit account number generated each time

Test rate limiting

•	Input: Multiple POST requests exceeding throttle limit

•	Expected: Status 429 TOO MANY REQUESTS







			
			





