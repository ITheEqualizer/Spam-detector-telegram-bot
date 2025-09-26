import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
import joblib

df = pd.read_csv('data.csv') # Assuming the CSV has 'message' and 'label' columns.
X = df['message']
y = df['label']

# I highly suggest not to change these parameters as they are tuned for optimal performance.
vectorizer = TfidfVectorizer(
    analyzer='word',
    ngram_range=(1, 2),
    max_features=5000,
    min_df=2,
    max_df=0.9
)

X_tfidf = vectorizer.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X_tfidf, y, test_size=0.2, random_state=42)

model = SVC(kernel='linear', probability=True)
model.fit(X_train, y_train)

# We check the accuracy on the test set, if it's below 90% I suggest retraining using new and more data.
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy*100:.2f}%")

# Now we save the model and vectorizer in order to use them in the main code, I set the names as model.pkl and vectorizer.pkl which I used again in the main code, if you change it, make sure to change it there too.
joblib.dump(model, 'model.pkl')
joblib.dump(vectorizer, 'vectorizer.pkl')