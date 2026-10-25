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
    def evaluate_eligibility(cls, age, years_resident, income) -> EligibilityResult:
        """Check each rule in turn and return the first one that fails."""
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
