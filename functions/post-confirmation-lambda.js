var AWS = require('aws-sdk');

exports.handler = (event, context, callback) => {
    var cognitoIdentityServiceProvider = new AWS.CognitoIdentityServiceProvider();
    console.log('event', event);
    console.log('group:', event.request.userAttributes['custom:group']);
    var params = {
        GroupName: event.request.userAttributes['custom:group'],
        UserPoolId: event.userPoolId,
        Username: event.userName
    };
    if (event.request.userAttributes['custom:group']) {
        cognitoIdentityServiceProvider.adminAddUserToGroup(params, function (err, data) {
            if (err) {
                callback(err);
            }
            callback(null, event);
        });
    }
};
