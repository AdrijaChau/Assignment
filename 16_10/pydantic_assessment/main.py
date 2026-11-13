import json


from typing import Literal

from pathlib import Path

from pydantic import BaseModel, ValidationError, Field, TypeAdapter


# Pydantic model

class Registration(BaseModel):
    registration_id: str

    name: str

    email: str

    age: int = Field(gt=18)

    ticket_type: Literal["Standard", "Premium", "VIP"]

    amount: float = Field(gt=0)


json_data = Path("registration.json").read_text()

registrations = json.loads(json_data)

print("___Valid Registrations___")

for registration in registrations:

    try:

        valid_registration = Registration.model_validate(registration)

        print(valid_registration)

    except ValidationError as e:

        reg_id = registration.get('registration_id')

        print(f"\n Validation Error for Registration ID:  {reg_id}")

        for error in e.errors():
            field_name = error["loc"][0] if error["loc"] else "global"

            error_msg = error.get("msg", "unknown")

            print(f"{field_name}: {error_msg}")

            valid_dict = valid_registration.model_dump()

            print(valid_dict)

            valid_json_string = valid_registration.model_dump_json()

            print(valid_json_string)

            all_valid_dict = []

            all_valid_dict.append(valid_registration.model_dump())

            with open("valid_registration.json", "w") as f:
                json.dump(all_valid_dict, f, indent=4)



