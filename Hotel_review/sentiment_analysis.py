import pandas as pd
import re
import string

dataframe = pd.read_csv('train.csv')

dataframe.describe().transpose()
count = dataframe.isnull().sum().sort_values(ascending=False)
percentage = (dataframe.isnull().sum() / len(dataframe) * 100).sort_values(ascending=False)
missing_data = pd.concat([count, percentage], axis=1, keys=['Count', 'Percentage'])

dataframe.drop(columns=['User_ID', 'Browser_Used', 'Device_Used'], inplace=True)


def text_clean(text):
    text = text.lower()
    text = re.sub('\[.*?\]', "", text)
    text = re.sub('[%s]' % re.escape(string.punctuation), "", text)
    text = re.sub(r'\w*\d\w*', '', text)
    text = re.sub('[‘’“”…]', '', text)
    text = re.sub('\n', '', text)
    return text


text_cleaning=lambda x : text_clean(x)

dataframe['cleaned_description'] = pd.DataFrame(dataframe['Description'].apply(text_cleaning))

from sklearn.model_selection import train_test_split

Independent_var = dataframe['cleaned_description']
Dependent_var = dataframe['Is_Response']

IV_train, IV_test, DV_train, DV_test = train_test_split(Independent_var, Dependent_var, test_size = 0.1, random_state = 225)

# print('IV_train :', len(IV_train))
# print('IV_test :', len(IV_test))
# print('DV_train :', len(DV_train))
# print('DV_test:', len(DV_test))


from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib

tvec = TfidfVectorizer()
clf2 = LogisticRegression(solver = "lbfgs")


from sklearn.pipeline import Pipeline

model = Pipeline([('vectorizer',tvec),('classifier',clf2)])

model.fit(IV_train, DV_train)


from sklearn.metrics import confusion_matrix

predictions = model.predict(IV_test)

confusion_matrix(predictions, DV_test)

joblib.dump(model,"sentiment_analysis.joblib")

reviews = ["This cloth was average","Not fit for me","Some clothes are damaged"]

result = model.predict(reviews)
predicted_results=[]
results=''.join(result)

for i in range(0,len(results),8):
    result=results[i:i+8]
    predicted_results.append(result)

for queries,prediction in zip(reviews,predicted_results):
    print(queries,"-----",prediction)

