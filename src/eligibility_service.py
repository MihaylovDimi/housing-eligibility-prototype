"""
Module: eligibility_service.py
Business logic for the Housing Register eligibility pre-check.
"""


class ValidationError(Exception):
    """Raised when user input is missing, of the wrong type or out of range."""


class EligibilityResult:
    """Holds the outcome of an eligibility check."""

    def __init__(self, is_eligible: bool, message: str):
        self.is_eligible = is_eligible
        self.message = message


class HousingEligibilityChecker:
    """Validates applicant data and checks it against the council's basic criteria."""

    @classmethod
    def validate_inputs(cls, age, years_resident, income) -> None:
        """Check types and ranges of the inputs. Raise ValidationError on bad data."""
        if not isinstance(age, int) or isinstance(age, bool):
            raise ValidationError("Invalid format: age must be a whole number")
        if age < 0:
            raise ValidationError("Invalid age: age cannot be negative")
        if age > 120:
            raise ValidationError("Invalid age: age exceeds the maximum allowed value")

        if not isinstance(years_resident, int) or isinstance(years_resident, bool):
            raise ValidationError("Invalid format: years of residence must be a whole number")
        if years_resident < 0:
            raise ValidationError("Invalid period: years of residence cannot be negative")
        if years_resident > age:
            raise ValidationError("Invalid period: years of residence cannot exceed age")

        if not isinstance(income, (int, float)) or isinstance(income, bool):
            raise ValidationError("Invalid format: income must be a number")
        if income < 0:
            raise ValidationError("Invalid income: annual income cannot be negative")

    @classmethod
    def evaluate_eligibility(cls, age, years_resident, income) -> EligibilityResult:
        """Validate the inputs first, then check each rule in turn."""
        cls.validate_inputs(age, years_resident, income)

        if age < 18:
            return EligibilityResult(False, "Not eligible: applicant must be at least 18 years old")

        if years_resident < 3:
            return EligibilityResult(
                False, "Not eligible: at least 3 years of residence in the borough is required"
            )

        if income > 30000:
            return EligibilityResult(
                False, "Not eligible: annual household income exceeds the £30,000 limit"
            )

        return EligibilityResult(True, "Eligible: you meet the basic criteria to apply")
