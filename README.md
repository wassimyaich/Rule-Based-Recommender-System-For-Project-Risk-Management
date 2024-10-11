# Rule_Based-Recommender_System-For-Project_Risk_Management
This project aims to assist project managers by facilitating the risk management task through a web application which is used to provide recommendations based on the search string entered by the user.
This involved the use of NLP (Natural Language Processing) techniques to automatically generate an ontology from the documents and from which the application can generate recommendations.

# How to run
-Download the final_ontology.owl and place it under "C:\users\username\Desktop"  
-Create a folder named "Dev" anywhere in your local disk  
-Open PowerShell or cmd and navigate to the folder's path   
-Run command: python -m venv "path to folder" or simply '.'  
-Download the folder "project" and "requirements.txt"  available in the files section above, and place it under "Dev"  
-Run command: pip install -R requirements.txt (preferably restart PowerShell/cmd after this step)  
-Run command: .\Scripts\Activate  
-Run command: python manage.py runserver  
-Open navigator and enter url: localhost:8000/sendRequest  

# Note
-Python version == 3.8  
-if you want to re-generate the rdf graph (ontology), simply download the processes folder, place it under your jupyter workspace then download the   final_project_risk_management.ipynb and place it in the same location, finally make sure all the necessary packages mentioned in the "imports" section are available and run the notebook.  

# acknowledgement
This work was accomplished thanks to the efforts of all the collaboratos:  
-Wassim Yaich  https://www.linkedin.com/in/wassim-yaich-a6a042201/ 
-Yessine Khanfir  https://www.linkedin.com/in/yessine-khanfir-b5b509177/  
-Yassine Ben Nacef  https://www.linkedin.com/in/bennacef-mohamedyassine-732b4b202/  
-Sarra Ferchichi  https://www.linkedin.com/in/sarra-ferchichi-822a491ba/  
-Mayssa Zaouali https://www.linkedin.com/in/mayssa-zaouali-9288421bb/
