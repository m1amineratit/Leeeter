/api/cards/

{
  "card_type": "personel", 
  "page_name": "Youssef Ratit",
  "page_url": "youssef-ratit",
  "accept_terms": true,
  "receive_newsletter": false
}


/api/pages/
{
  "card": 1,
  "name": "My New Page",
  "slug": "my-new-page",
  "description": "This is the best page ever."
}


/api/posts/
{
  "user": 1,
  "title": "First Post",
  "content": "This is the content of the post.",
  "page": 1
}

/api/businesses/
{
  "page": 1,   
  "whatsapp_number": "+1234567890",
  "email": "contact@example.com"
}

/api/contacts/
{
  "page": 1,      
  "whatsapp_number": "+1234567890",
  "email": "contact@example.com"
}

/api/locations/

{
  "page": 1,
  "country": "Morocco",
  "city": "Casablanca",
  "location_address": "123 Main Street"
}

/api/hours/

{
  "page": 1,
  "hour": "09:00:00"  
}

/api/socials/

{
  "page": 1,
  "platform": "Facebook",
  "url": "https://facebook.com/my-page"
}

/api/faqs/

{
  "page": 1,
  "question": "What are your working hours?",
  "answer": "We are open from 9am to 6pm."
}

/api/connections/

{
  "page": 1,
  "label": 1,  
  "active": "active"
}

/api/send_email

{
  "subject": "Hello Subscribers",
  "message": "This is a test email.",
  "to_email": "subscriber@example.com"
}

/api/add_label

{
  "page_id": 1,
  "label": "VIP",
  "subscriber_id": 3
}

/api/broadcast_message

{
  "page_id": 1,
  "subject": "Big Sale!",
  "content": "Don't miss our big sale this weekend."
}

/api/credits/add/

{
  "amount": 100
}


/api/credits/use/

{
  "amount": 20
}

/api/credits/history

GET

http://127.0.0.1:8000/api/credits/history

/api/credits/balance

GET

http://127.0.0.1:8000/api/credits/balance
