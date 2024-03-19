// Dependencies
const AWS = require("aws-sdk");
import { CognitoUserPoolTriggerHandler } from 'aws-lambda';
import { randomDigits } from 'crypto-secure-random-digit';
import { SNS } from 'aws-sdk';

//import { CreateAuthChallengeTriggerHandler } from 'aws-lambda';
//import { SES } from 'aws-sdk';

//const ses = new SES();


// Set region
//AWS.config.update({ region: "ap-south-1" });
AWS.config.update({ region: "ap-southeast-1" });

/**
 * Generate passwordless sign-in OTP and send to user
 * @param {AWS Lambda Event} event
 */
exports.handler = async (event) => {
    let secretLoginCode;
    //if (event.request.session && event.request.session.length && event.request.session.slice(-1)[0].challengeName == "SRP_A" || event.request.session.length == 0) {
    if (!event.request.session || !event.request.session.length) {
        // Generate a new secret login code and send it to the user
        //secretLoginCode = Date.now().toString().slice(-4);
        secretLoginCode = randomDigits(4).join('');
        try {
            if ("phone_number" in event.request.userAttributes) {

                var setSMSTypePromise = new AWS.SNS({ apiVersion: "2010-03-31" })
                    .setSMSAttributes({
                        attributes: {
                            DefaultSMSType: "Transactional",
                        },

                    })
                    .promise();
                var params = {
                    Message: secretLoginCode,
                    PhoneNumber: event.request.userAttributes.phone_number,
                };
                console.log(params);
                // Create promise and SNS service object
                var publishTextPromise = new AWS.SNS({ apiVersion: "2010-03-31" })
                    .publish(params)
                    .promise();
                const result = await publishTextPromise;
                console.log("SMS DELIVERED");
            }

        } catch (error) {
            // Handle SMS Failure
            console.log(error);
        }
    } else {
        // re-use code generated in previous challenge
        const previousChallenge = event.request.session.slice(-1)[0];
        secretLoginCode =
            previousChallenge.challengeMetadata.match(/CODE-(\d*)/)[1];
    }

    // Add the secret login code to the private challenge parameters
    // so it can be verified by the "Verify Auth Challenge Response" trigger
    event.response.privateChallengeParameters = { secretLoginCode };

    // Add the secret login code to the session so it is available
    // in a next invocation of the "Create Auth Challenge" trigger
    event.response.challengeMetadata = `CODE-${secretLoginCode}`;
    console.log(secretLoginCode);
    return event;
};

