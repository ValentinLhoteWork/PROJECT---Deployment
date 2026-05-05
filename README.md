###  Live API:
https://vallho-getaround-api-hf.hf.space

### Documentation:
https://vallho-getaround-api-hf.hf.space/docs

### Predict endpoint:
POST https://vallho-getaround-api-hf.hf.space/predict

## Website Streamlit

### Overview page 

<img width="2495" height="1443" alt="overview page" src="https://github.com/user-attachments/assets/3fb53a80-c7d9-445e-9668-859a59882ec8" />

### Revenue Impact

<img width="2505" height="1337" alt="Revenue_impact" src="https://github.com/user-attachments/assets/645994c5-dde4-43c1-bbee-471a23ac2650" />


Threshold simulation

<img width="2512" height="1391" alt="Thredhold_simulation" src="https://github.com/user-attachments/assets/d49e728f-570a-4acc-8820-a95533a589fc" />

Late_checkout_analysis
<img width="2531" height="1465" alt="Late_checkout_analysis" src="https://github.com/user-attachments/assets/ebdbe836-7642-4aa2-88f9-d24ddeb251d2" />


API
<img width="2487" height="1488" alt="image" src="https://github.com/user-attachments/assets/c888d601-9555-48de-8695-a17170beb611" />



# PROJECT - Deployment
## Getaround Analysis 🚗


<img width="1206" height="443" alt="image" src="https://github.com/user-attachments/assets/803abe75-1ce3-43f4-bdd3-8b1686edc764" />


GetAround is the Airbnb for cars. You can rent cars from any person for a few hours to a few days! Founded in 2009, this company has known rapid growth. In 2019, they count over 5 million users and about 20K available cars worldwide.

As Jedha's partner, they offered this great challenges:
Context

When renting a car, our users have to complete a checkin flow at the beginning of the rental and a checkout flow at the end of the rental in order to:

    Assess the state of the car and notify other parties of pre-existing damages or damages that occurred during the rental.
    Compare fuel levels.
    Measure how many kilometers were driven.

The checkin and checkout of our rentals can be done with three distinct flows:

    📱 Mobile rental agreement on native apps: driver and owner meet and both sign the rental agreement on the owner’s smartphone
    Connect: the driver doesn’t meet the owner and opens the car with his smartphone
    📝 Paper contract (negligible)

Project 🚧

For this case study, we suggest that you put yourselves in our shoes, and run an analysis we made back in 2017 🔮 🪄

When using Getaround, drivers book cars for a specific time period, from an hour to a few days long. They are supposed to bring back the car on time, but it happens from time to time that drivers are late for the checkout.

Late returns at checkout can generate high friction for the next driver if the car was supposed to be rented again on the same day : Customer service often reports users unsatisfied because they had to wait for the car to come back from the previous rental or users that even had to cancel their rental because the car wasn’t returned on time.
Goals 🎯

In order to mitigate those issues we’ve decided to implement a minimum delay between two rentals. A car won’t be displayed in the search results if the requested checkin or checkout times are too close from an already booked rental.

It solves the late checkout issue but also potentially hurts Getaround/owners revenues: we need to find the right trade off.

Our Product Manager still needs to decide:

    threshold: how long should the minimum delay be?
    scope: should we enable the feature for all cars?, only Connect cars?

In order to help them make the right decision, they are asking you for some data insights. Here are the first analyses they could think of, to kickstart the discussion. Don’t hesitate to perform additional analysis that you find relevant.

    Which share of our owner’s revenue would potentially be affected by the feature?
    How many rentals would be affected by the feature depending on the threshold and scope we choose?
    How often are drivers late for the next check-in? How does it impact the next driver?
    How many problematic cases will it solve depending on the chosen threshold and scope?

Web dashboard

First build a dashboard that will help the product Management team with the above questions. You can use streamlit or any other technology that you see fit.
Machine Learning - /predict endpoint

In addition to the above question, the Data Science team is working on pricing optimization. They have gathered some data to suggest optimum prices for car owners using Machine Learning.

I should provide at least one endpoint /predict. The full URL would look like something like this: https://your-url.com/predict.

This endpoint accepts POST method with JSON input data and it should return the predictions. We assume inputs will be always well formatted. It means you do not have to manage errors. We leave the error handling as a bonus.

Input example:

{
  "input": [[7.0, 0.27, 0.36, 20.7, 0.045, 45.0, 170.0, 1.001, 3.0, 0.45, 8.8], [7.0, 0.27, 0.36, 20.7, 0.045, 45.0, 170.0, 1.001, 3.0, 0.45, 8.8]]
}

The response should be a JSON with one key prediction corresponding to the prediction.

Response example:

{
  "prediction":[6,6]
}

Documentation page

I need to provide the users with a documentation about my API.

It has to be located at the /docs of your website. If we take the URL example above, it should be located directly at https://your-url.com/docs).

This small documentation should at least include:

    An h1 title: the title is up to you.
    A description of every endpoints the user can call with the endpoint name, the HTTP method, the required input and the expected output (you can give example).

To complete this project, it should deliver:

    A dashboard in production (accessible via a web page for example)
    The whole code stored in a Github repository. You will include the repository's URL.
    An documented online API on Hugging Face server (or any other provider you choose) containing at least one /predict endpoint that respects the technical description above. We should be able to request the API endpoint /predict using curl:

$ curl -i -H "Content-Type: application/json" -X POST -d '{"input": [[7.0, 0.27, 0.36, 20.7, 0.045, 45.0, 170.0, 1.001, 3.0, 0.45, 8.8]]}' http://your-url/predict

Or Python:

import requests

response = requests.post("https://your-url/predict", json={
    "input": [[7.0, 0.27, 0.36, 20.7, 0.045, 45.0, 170.0, 1.001, 3.0, 0.45, 8.8]]
})
print(response.json())
