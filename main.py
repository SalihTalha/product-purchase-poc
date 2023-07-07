import streamlit as st
from chatgpt import query
import pandas as pd


payment = {
    'One-Time': 1,
    'Per-Year': 10,
    'Per-Month': 120
}


@st.cache_resource()
def load_model():
    print("Load model started")
    from sklearn.model_selection import train_test_split
    # from sklearn.tree import DecisionTreeClassifier
    from sklearn.ensemble import RandomForestClassifier

    X = pd.read_csv('X.csv').drop(["Unnamed: 0"], axis=1)
    y = pd.read_csv('Y.csv').drop(["Unnamed: 0"], axis=1)
    print(X)
    print(y)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    # decision_tree = DecisionTreeClassifier()
    random_forest = RandomForestClassifier()

    # decision_tree.fit(X_train, y_train)
    random_forest.fit(X_train, y_train)

    return random_forest


def predict(model, X):
    prediction = model.predict(X)[0]
    print(prediction)
    return prediction


def generate_output_text(decision, name, price, rating, payment_option, comment_count, per_user, free_version, free_trial,
                         maintenance, implementation, savings):
    message = "There is a software program I am considering to buy. "
    message += f"Its called {name}." if name else ""
    message += f"It has {comment_count} comments and it has the rating {rating} out of 5."
    message += f"It costs me {price} dollars {payment_option}."
    if per_user:
        message += f"This cost is per user."

    message += f"It will make me save {savings} dollars per month."

    if free_version:
        message += f"There is also a free version of this software."
    if free_trial:
        message += f"There is a free trial for this software."

    message += comments

    if decision:
        message += "Why should I buy this software?"
    else:
        message += "Why shouldn't I buy this software?"

    message += "Could you please summarize it in a few sentences. Be confident and make it a legal text."

    output = query(message)

    return output

# Streamlit UI
st.title("Input Form")
st.write("Enter the following inputs:")

# Input fields
name = st.text_area("Name")
price = st.number_input("Price ($)", step=1)
options = ["Per-Year", "Per-Month", "One-Time"]  # Options for the dropdown selector
payment_option = st.selectbox("Payment Option", options)

implementation = st.number_input("Implementation Costs ($)", step=1)
maintenance = st.number_input("Monthly Maintenance Costs ($)", step=1)
savings = st.number_input("Potential Monthly Cost Savings ($)", step=1)

rating = st.number_input("Rating", step=0.1, min_value=0.0, max_value=5.0)


comment_count = st.number_input("Comment Count", step=1)
per_user = st.checkbox("Per User")
free_version = st.checkbox("Free Version")
free_trial = st.checkbox("Free Trial")
comments = st.text_area("Your Comments About The Product")

# Generate output text on button click
if st.button("Generate Output"):
    cost = price * payment[payment_option]
    cost += maintenance * 120 + implementation

    X = pd.DataFrame([{
        'price': price,
        'rating': rating,
        'comment_count': comment_count,
        'per_user': per_user,
        'free_version': free_version,
        'free_trial': free_trial,
        'total_price': cost - savings * 120
    }])

    model = load_model()
    prediction = predict(model, X)

    output = generate_output_text(prediction, name, price, rating, payment_option, comment_count, per_user, free_version,
                                  free_trial, maintenance, implementation, savings)
    st.text_area("Output", value=output, height=200)
