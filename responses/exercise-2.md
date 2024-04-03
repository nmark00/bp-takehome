# Exercise 2

## Business Process Description

The business process being modeled is the check-in process at a climbing gym. When a member arrives at the gym, they scan their membership card or provide their member ID to the front desk staff. The check-in process records the member's visit, including the date and time of their arrival, and any additional services or rentals they may have purchased during their visit.

## Fact Table: gym_check_ins

| Column Name | Type | Description |
| --- | --- | --- |
| check_in_id | int | Unique identifier for each check-in event |
| member_id | int | Foreign key referencing the member dimension |
| check_in_date | date | Date of the check-in event |
| check_in_time | time | Time of the check-in event |
| visit_duration | int | Duration of the visit in minutes |
| gear_rental_id | int | Foreign key referencing the gear rental dimension (if applicable) |
| locker_rental_id | int | Foreign key referencing the locker rental dimension (if applicable) |
| class_attended_id | int | Foreign key referencing the class attended dimension (if applicable) |

## Dimension: members

| Column Name | Type | Description |
| --- | --- | --- |
| member_id | int | Unique identifier for each member |
| first_name | varchar | Member's first name |
| last_name | varchar | Member's last name |
| email | varchar | Member's email address |
| phone | varchar | Member's phone number |
| membership_type | varchar | Type of membership (e.g., monthly, annual, student) |
| join_date | date | Date the member joined the gym |
| birth_date | date | Member's date of birth |
| gender | varchar | Member's gender |
| address | varchar | Member's address |
| city | varchar | Member's city |
| state | varchar | Member's state |
| zip_code | varchar | Member's zip code |
| country | varchar | Member's country |


The `gym_check_ins` fact table records each check-in event at the climbing gym, along with relevant details such as the member ID, check-in date and time, visit duration, and any additional services or rentals associated with the visit. The `members` dimension table provides additional information about each member, such as their name, contact details, membership type, and demographic information. This schema allows for analysis of gym usage patterns, member behavior, and the popularity of various services and rentals offered by the gym.