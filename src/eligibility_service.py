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

    def __repr__(self):
        return f"EligibilityResult(eligible={self.is_eligible}, message='{self.message}')"


class HousingEligibilityChecker:
    """Validates applicant data and checks it against the council's basic criteria."""

    MIN_AGE = 18
    MAX_AGE = 120
    MIN_YEARS_LOCAL = 3
    MAX_HOUSEHOLD_INCOME = 30000.0

    @classmethod
    def validate_inputs(cls, age, years_resident, income) -> None:
        """Check types and ranges of the inputs. Raise ValidationError on bad data."""
        if not isinstance(age, int) or isinstance(age, bool):
            raise ValidationError("Invalid format: age must be a whole number")
        if age < 0:
            raise ValidationError("Invalid age: age cannot be negative")
        if age > cls.MAX_AGE:
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
        """Return an EligibilityResult. Validation runs first, then each rule in turn."""
        cls.validate_inputs(age, years_resident, income)

        if age < cls.MIN_AGE:
            return EligibilityResult(
                False, f"Not eligible: applicant must be at least {cls.MIN_AGE} years old"
            )

        if years_resident < cls.MIN_YEARS_LOCAL:
            return EligibilityResult(
                False,
                f"Not eligible: at least {cls.MIN_YEARS_LOCAL} years of residence in the borough is required",
            )

        if income > cls.MAX_HOUSEHOLD_INCOME:
            return EligibilityResult(
                False,
                f"Not eligible: annual household income exceeds the £{cls.MAX_HOUSEHOLD_INCOME:,.0f} limit",
            )

        return EligibilityResult(True, "Eligible: you meet the basic criteria to apply")
