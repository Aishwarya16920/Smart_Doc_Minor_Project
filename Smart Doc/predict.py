# Importing libraries
import numpy as np
import pandas as pd
from scipy.stats import mode
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
import random

# Reading the training data
data_path="Diseases.csv"
data=pd.read_csv(data_path)

# Encoding the target value (prognosis column) into numerical value using LabelEncoder
encoder = LabelEncoder()
data["prognosis"] = encoder.fit_transform(data["prognosis"])

# Training the models
X = data.iloc[:,:-1]
Y= data.iloc[:, -1]
X_train, X_test, y_train, y_test =train_test_split(X, Y, test_size = 0.2, random_state = 24)
# print(f"Train: {X_train.shape}, {y_train.shape}")
# print(f"Test: {X_test.shape}, {y_test.shape}")

# Training and testing SVM Classifier
svm_model = SVC()
svm_model.fit(X_train, y_train)
preds = svm_model.predict(X_test)
# print(f"Accuracy on train data by SVM Classifier: {accuracy_score(y_train, svm_model.predict(X_train))*100}")
# print(f"Accuracy on test data by SVM Classifier: {accuracy_score(y_test, preds)*100}")

# Training and testing Naive Bayes Classifier
nb_model = GaussianNB()
nb_model.fit(X_train, y_train)
preds = nb_model.predict(X_test)
# print(f"Accuracy on train data by Naive Bayes Classifier: {accuracy_score(y_train, nb_model.predict(X_train))*100}")
# print(f"Accuracy on test data by Naive Bayes Classifier: {accuracy_score(y_test, preds)*100}")

# Training and testing Random Forest Classifier
rf_model = RandomForestClassifier(random_state=18)
rf_model.fit(X_train, y_train)
preds = rf_model.predict(X_test)
# print(f"Accuracy on train data by Random Forest Classifier: {accuracy_score(y_train, rf_model.predict(X_train))*100}")
# print(f"Accuracy on test data by Random Forest Classifier: {accuracy_score(y_test, preds)*100}")

# Training the models on whole data
final_svm_model = SVC()
final_nb_model = GaussianNB()
final_rf_model = RandomForestClassifier(random_state=18)
final_svm_model.fit(X, Y)
final_nb_model.fit(X, Y)
final_rf_model.fit(X, Y)

symptoms = X.columns.values

# Creating a symptom index dictionary to encode the input symptoms into numerical form
symptom_index = {}
for index, value in enumerate(symptoms):
	symptom = " ".join([i.capitalize() for i in value.split("_")])
	symptom_index[symptom] = index

data_dict = {
	"symptom_index":symptom_index,
	"predictions_classes":encoder.classes_
}

# Defining the Function Input: string containing symptoms separated by commmas Output: Generated predictions by models
def predictDisease(symptoms):
	symptoms = symptoms.split(", ")
	
	# creating input data for the models
	input_data = [0] * len(data_dict["symptom_index"])
	try:
		for symptom in symptoms:
			index = data_dict["symptom_index"][symptom]
			input_data[index] = 1
		# reshaping the input data and converting it
		# into suitable format for model predictions
		input_data = np.array(input_data).reshape(1,-1)
		
		# generating individual outputs
		rf_prediction = data_dict["predictions_classes"][final_rf_model.predict(input_data)[0]]
		nb_prediction = data_dict["predictions_classes"][final_nb_model.predict(input_data)[0]]
		svm_prediction = data_dict["predictions_classes"][final_svm_model.predict(input_data)[0]]
		
		# making final prediction by taking mode of all predictions
		final_prediction = mode([rf_prediction, nb_prediction, svm_prediction])[0][0]
        
		remedy=cure(final_prediction)
		return "You might have "+final_prediction+ ". "+remedy
    
	except KeyError:
		rpl=["Could you please re-phrase that? ",
            "I’m sorry, I don’t understand.",
            "Sorry, I didn’t get that.",
            "I can’t make head nor tail of what you’re saying.",
            "What does that mean?",
            "Can you try saying that again in a different way? I don't understand.",
            ][
		random.randrange(6)]
		return rpl

# Function to return an approriate treatment for the predicted disease
def cure(remedy):
	treatment = pd.read_csv("Treatment.csv",encoding='latin1')
	for rows in treatment.iterrows():
		medication=treatment.loc[treatment['Prognosis'] == remedy]
		pd.options.display.max_colwidth = 1000
		return medication['Treatment'].to_string(index=False)