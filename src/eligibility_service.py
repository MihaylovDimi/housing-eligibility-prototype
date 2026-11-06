"""Eligibility rules for the council Housing Register pre-check."""

from dataclasses import dataclass

MIN_AGE = 18
MAX_AGE = 120
MIN_YEARS_LOCAL = 3
MAX_HOUSEHOLD_INCOME = 30_000


class ValidationError(Exception):
    """Raised when an input has the wrong type or is out of range."""


@dataclass
class EligibilityResult:
    """The outcome of an eligibility check."""

    is_eligible: bool
    message: str


def is_whole_number(value):
    """Return True for whole numbers, but not for True or False."""
    return isinstance(value, int) and not isinstance(value, bool)


def validate_inputs(age, years_resident, income):
    """Raise ValidationError if any input is invalid."""
    if not is_whole_number(age):
        raise ValidationError("Invalid format: age must be a whole number")
    if age < 0:
        raise ValidationError("Invalid age: age cannot be negative")
    if age > MAX_AGE:
        raise ValidationError("Invalid age: age is above the maximum")

    if not is_whole_number(years_resident):
        raise ValidationError(
            "Invalid format: years of residence must be a whole number"
        )
    if years_resident < 0:
        raise ValidationError(
            "Invalid period: years of residence cannot be negative"
        )
    if years_resident > age:
        raise ValidationError(
            "Invalid period: years of residence cannot exceed age"
        )

    if isinstance(income, bool) or not isinstance(income, (int, float)):
        raise ValidationError("Invalid format: income must be a number")
    if income < 0:
        raise ValidationError("Invalid income: income cannot be negative")


def check_eligibility(age, years_resident, income):
    """Validate the inputs, then apply each rule in turn."""
    validate_inputs(age, years_resident, income)

    if age < MIN_AGE:
        return EligibilityResult(
            False,
            f"Not eligible: applicant must be at least {MIN_AGE} years old",
        )

    if years_resident < MIN_YEARS_LOCAL:
        return EligibilityResult(
            False,
            f"Not eligible: at least {MIN_YEARS_LOCAL} years of residence "
            "in the borough is required",
        )

    if income > MAX_HOUSEHOLD_INCOME:
        return EligibilityResult(
            False,
            "Not eligible: annual household income is above "
            f"£{MAX_HOUSEHOLD_INCOME:,}",
        )

    return EligibilityResult(
        True, "Eligible: you meet the basic criteria to apply"
    )