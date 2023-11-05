Here is a detailed explantion of Staff in main.py:
## Summary
The Staff class is a model class that represents staff members. It provides methods for retrieving, creating, updating, and deleting staff records in a Redis database.

### Example Usage
```
# Retrieve all staff members
all_staff = Staff.all()

# Count the number of staff members
staff_count = Staff.count()

# Count the number of available staff members
available_staff_count = Staff.count_available()

# Count the number of staff members by occupation
count_by_occupation = Staff.count_by_occupation('occupation')

# Count the number of available staff members by occupation
count_by_occupation_available = Staff.count_by_occupation_available('occupation')

# Create a new staff member
new_staff = Staff(username='john', full_name='John Doe', contact_number='123456789', occupation='developer', domain='IT', current_location='New York', current_status='available')
new_staff.save()

# Get a staff member by primary key
staff_member = Staff.get('staff_id')

# Update a staff member
staff_member.username = 'johndoe'
staff_member.save()

# Get a random available staff member
random_staff = Staff.random_available(1)

# Delete a staff member
Staff.delete('staff_id')
```
### Code Analysis
Main functionalities
The main functionalities of the Staff class are:

- Retrieving all staff members
- Counting the number of staff members
- Counting the number of available staff members
- Counting the number of staff members by occupation
- Counting the number of available staff members by occupation
- Creating a new staff member
- Getting a staff member by primary key
- Updating a staff member
- Getting a random available staff member
- Deleting a staff member
### Methods
- all(): Retrieves all staff members and returns a list of formatted staff records.
- count(): Counts the number of staff members and returns the count.
- count_available(): Counts the number of available staff members and returns the count.
- count_by_occupation(domain: str): Counts the number of staff members by occupation and returns the count.
- count_by_occupation_available(domain: str): Counts the number of available staff members by occupation and returns the count.
- format(pk: str): Formats a staff record based on the primary key and returns a dictionary with the formatted fields.
- create(staff: Staff): Creates a new staff member and saves it to the Redis database.
- get(pk: str): Retrieves a staff member by primary key and adds the staff record to a Redis stream.
- update(pk: str, staff: Staff): Updates a staff member's fields and saves the changes to the Redis database.
- random_available(value: int): Retrieves a random available staff member based on the specified value and returns the staff member or a message if no available staff members are found.
- delete(pk: str): Deletes a staff member from the Redis database.
#### Fields
The Staff class has the following fields:

- username: The username of the staff member.
- full_name: The full name of the staff member.
- contact_number: The contact number of the staff member.
- occupation: The occupation of the staff member.
- domain: The domain of the staff member.
- current_location: The current location of the staff member.
- current_status: The current status of the staff member.

----

Here is a detailed explantion of consumer.py:

## Summary
The code snippet is a while loop that continuously checks for new messages in a Redis stream. If a new message is found, it checks if the number of available staff is different from the number specified in the message. If they are different, it assigns a random available staff member to the message and updates their status in the database. If an error occurs during the process, it adds the message to a separate Redis stream called 'request_waiting'.

### Example Usage
```
# Assuming there is a new message in the Redis stream 'emergency_request'
# with the following data:
# {
#   'staff_assigned': 3,
#   'pk': '12345'
# }

# The code snippet will check if the number of available staff is different from 3.
# If it is different, it will assign a random available staff member to the message
# and update their status in the database.
# If an error occurs during the process, it will add the message to the 'request_waiting' stream.
```
### Code Analysis
#### Inputs
- redis: Redis connection object.
- random_available: Function that returns a - random available staff member.
- count_available: Function that returns the - count of available staff members.
- key: Name of the Redis stream to read from.
- group: Name of the consumer group for the stream.
#### Flow
- Create a consumer group named 'staff_group' for the Redis stream 'emergency_request'.
- Enter a while loop that continuously checks for new messages in the stream.
- Read the messages from the stream using the xreadgroup command.
- If there are new messages:
    - Iterate over each message.
        - Extract the message data from the message object.
        - Check if the number of available staff is different from the number specified in the message.
    - If they are different:
        - Assign a random available staff member to the message.
        - Update the staff member's status in the database.
    - If an error occurs during the process, add the message to the 'request_waiting' stream.
- If an exception occurs during the process, print the error message.
- Sleep for 1 second before checking for new messages again.