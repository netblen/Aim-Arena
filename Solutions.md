# Issue: Data Not Saving to scores Properly

## Problem Characterization
**Unexpected Behavior:** The endpoint /add_score is supposed to add the new score into the scores dictionary. On the other hand, this application sometimes overwrites scores in the same position and sometimes does nothing.

**Expected Behaviour:** A newly added score in the score list of the matching game and nothing else is changed in the scores dictionary.

**Discovery:** It came into view when looking into the `/add_score` endpoint that was implemented with the addition of a few scores for different games.

## Root Cause Investigation
**Underlying Cause:** The problem here had to do with the mismatch in format between the incoming score value and what was expected. Furthermore, there was no kind of validation on whether the game key actually existed in the scores dictionary; thus, failures occurred in the instance of invalid keys being introduced.

**Incorrect Assumptions:** The application assumed that all of its input data was already formatted and validated from the client side.

**Dependencies Involved:** Request.json object and routing mechanism of Flask.

## Resolution
**Fix Implemented:**
1. Added a conditional that checked if the game key existed in the scores dictionary before appending.
2. Ensured that the score value was of a valid type, either integer or float.
3. Improved error messages allow for better debugging when wrong information is provided.

**Adjustments Applied:**
Now, the code checks if the game's name exists and if the score data is valid.

## Prevention
**Prevention Strategies:**
Properly validate all the input materials both on client and server-side and log thorough error messages to help debug issues.

**Lessons Learned:**
Use meaningful error messages to debug easily and enhance my developer experience.

**Warning Signs:**
Lack of proper error messages can be critical issues