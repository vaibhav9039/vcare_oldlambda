exports.handler = async (event, context, callback) => {

    // user is not registered
    if (event.request.userNotFound) {
        event.response.issueToken = false;
        event.response.failAuthentication = true;

        throw new Error("User does not exist");
    } else if (event.request.session.length == 1 &&
        event.request.session[0].challengeName == 'SRP_A'
    ) {
        event.response.issueTokens = false;
        event.response.failAuthentication = false;
        event.response.challengeName = 'PASSWORD_VERIFIER';
    } else if (
        event.request.session.length >= 3 &&
        event.request.session.slice(-1)[0].challengeResult === false
    ) {
        // wrong OTP even After 3 sessions?
        event.response.issueToken = false;
        event.response.failAuthentication = true;
        throw new Error("Invalid OTP");
    } else if (
        event.request.session &&
        event.request.session.length > 0 &&
        event.request.session.slice(-1)[0].challengeResult === true
    ) {
        // correct OTP!
        event.response.issueTokens = true;
        event.response.failAuthentication = false;
    } else {
        // not yet received correct OTP
        event.response.issueTokens = false;
        event.response.failAuthentication = false;
        event.response.challengeName = "CUSTOM_CHALLENGE";

        throw new Error("OTP not yet received");
    }
    // Return to Amazon Cognito
    callback(null, event);
};