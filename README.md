1. Overview
   
   The Bank Account Creation enables users to seamlessly open new bank accounts digitally through a secure and automated backend system.It simplifies the onboarding process by allowing customers to submit essential information such as name, contact details, identification numbers (Aadhaar, PAN), and preferred account type.

   Once submitted, the API performs necessary validations — such as checking for duplicate accounts, verifying ID formats, and ensuring a minimum deposit amount — before creating a new account record.

   It then generates a unique account number, links it to the corresponding customer profile, and returns confirmation details including IFSC code, customer ID, and account creation timestamp.

2. Endpoint
   
    POST /api/accounts/create/
   
3. Description
   
	Creates a new bank account for an existing or new customer.The API validates user information (name, ID, email, etc.), assigns an account number, and stores account details in the database.

4. Request Body

     {
      
      "customer_name": "XYZ ",
      
      "email": "xyz@example.com",
      
      "phone_number": "9876543210",
      
      "address": "No.45, Anna Nagar, Chennai",
      
      "account_type": "Savings",
      
      "initial_deposit": 5000,
      
      "branch_code": "CHN001",
      
      "aadhar_number": "123456789012",
      
      "pan_number": "ABCDE1234F"
      
    }

5. Sample successful response

      {
      
        "message": "Account created successfully.",
        
        "account_number": "SBI0001",
        
        "ifsc_code": "BANK0001234",
        
        "customer_id": "CUST98765",
        
        "created_at": "2025-10-15 10:34:21"
        
      }


6. Sample error responses

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
        





			
			





