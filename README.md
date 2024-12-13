# ☁️ Cloud Computing C242-PS177 ☁️
Welcome to the cloud computing member repository. here we build the API backend and implement the backend for UrKins. 🔨☁️

## 🔎 Backend Overview 
This API is designed to predict skin conditions based on uploaded images. It leverages the power of Google Cloud Platform (GCP) to provide a robust and scalable solution. 

## 🔧 Cloud Infrastructure 🔧
The app utilizes various services provided by Google Cloud Platform. The process starts when the user uploads a skin image through the mobile application. Before accessing the prediction feature, the user needs to login first using a JWT-based authentication system. JWT (JSON Web Token) is an open standard for a compact and secure token representation to transfer information between two parties as JSON. After successful login, the user will get a JWT token that will be used to access features that require authentication, such as viewing prediction history. The uploaded image is then stored in Cloud Storage. Furthermore, the backend API built using Flask and Python will process the image and make predictions. The JWT authentication process ensures that only verified users can access certain data and features in the application. Prediction results are stored in Cloud SQL for tracking and analysis purposes. Using Cloud Run, the backend API can be run flexibly and scalably. The final prediction results are then displayed back to the user through their mobile app. The use of Google Cloud Platform allows this application to have high performance, good security, and excellent scalability.
