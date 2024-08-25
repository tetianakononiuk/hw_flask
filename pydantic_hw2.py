import json
from pydantic import BaseModel, EmailStr, Field, field_validator, ValidationError


class Address(BaseModel):
    city:str = Field(..., min_length=2)
    street: str = Field(..., min_length=3)
    house_number: int = Field(..., gt=0)


class User(BaseModel):
    name: str = Field(..., pattern="^[A-Za-z]{2,}$")
    age: int = Field(..., ge=0, le=120)
    email: EmailStr
    is_employed: bool
    address: Address

    @field_validator('age')
    def check_age_and_employment(cls, age, values):

        if 'is_employed' and age < 18:
            raise ValueError('User under 18 cannot be employed')
        return age

def process_user_data(json_data: str):
    try:
        user_data = json.loads(json_data)
        user = User.model_validate(user_data)
        return user.json()
    except ValidationError as e:
        return f'Ошибка валидации: {e}'


json_input = '''
{
    "name": "John",
    "age": 25,
    "email": "john.doe@example.com",
    "is_employed": true,
    "address": {
        "city": "Berlin",
        "street": "Main Street",
        "house_number": 101
    }
}
'''

invalid_json_age = '''{
      "name": "Alice",
      "age": 17,
      "email": "alice@example.com",
      "is_employed": true,
      "address": {
         "city": "Paris",
         "street": "Champs-Élysées",
         "house_number": 10
     }
 }'''


invalid_json_name = '''{
      "name": "B",
      "age": 25,
      "email": "bob@example.com",
      "is_employed": false,
      "address": {
      "city": "London",
      "street": "Baker Street",
         "house_number": 221
      }
  }'''

print(process_user_data(json_input))
print(process_user_data(invalid_json_age))
print(process_user_data(invalid_json_name))





