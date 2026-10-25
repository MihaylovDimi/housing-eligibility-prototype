Feature: Housing Register eligibility check
  As a resident of the borough
  I want to enter my age, years of residence and annual household income
  So that I can find out straight away whether I can apply to join the Housing Register

  @successful @normal
  Scenario: Resident who meets all criteria is eligible
    Given the resident is 25 years old
    And the resident has lived in the borough for 4 years
    And the annual household income is 22000 pounds
    When the details are submitted for checking
    Then the resident should be shown as eligible
    And the message should contain "Eligible: you meet the basic criteria to apply"

  @alternative @boundary
  Scenario: Resident with less than 3 years of residence is not eligible
    Given the resident is 30 years old
    And the resident has lived in the borough for 2 years
    And the annual household income is 18000 pounds
    When the details are submitted for checking
    Then the resident should be shown as not eligible
    And the message should contain "at least 3 years of residence in the borough is required"

  @invalid
  Scenario: Negative age is rejected by input validation
    Given the resident is -5 years old
    And the resident has lived in the borough for 3 years
    And the annual household income is 15000 pounds
    When the details are submitted for checking
    Then a validation error should be raised
    And the error message should be "Invalid age: age cannot be negative"
