# Scenario: 
When patient arrives at the clinic, nurse must register the patient in the system and record patient vital signs. If patient vital signs are abnormal, doctor must diagnose patient. If necessary, nurse gives treatment prescribed by doctor, patient takes treatment, unless patient refuses treatment.

# Roles:
- Doctor 
- Nurse
- Patient

# Activity:
- Patient arrives at the clinic 
- Nurse register the patient in system
- Nurse records patients vital signs
- Doctor diagnoses patient 
- Nurse gives treatment
- Patient takes treatment

# Rules:
- Nurse must register patient and record their vital signs when they arrive
- Doctor must diagnose if patient has abnormal vital signs. 
- Nurse should only give treatment if nessacary 
- Patient takes treatment unless they refuse. 

# DCR explaination 
The process is very linear, but for most activities another activity has to have been performed, that’s why we use condition-arrows. Diagnosing is pending, since the doctor only needs to diagnose the patient if vital signs are abnormal. Therefore for "diagnose the patient" we have added an include-arrow. Take treatment is also pending since a patient can choose to refuse treatment (habeas corpus), therefore we have included an exclude-arrow between "take treatment" and "refuses treatment". All activities are assigned to a role. 