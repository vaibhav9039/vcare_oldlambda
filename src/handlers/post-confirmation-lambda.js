var AWS = require('aws-sdk');

exports.handler = (event, context, callback) => {

    var cognitoIdentityServiceProvider = new AWS.CognitoIdentityServiceProvider();
    console.log('event', event);
    console.log('group:', event.request.userAttributes['custom:group']);
    var params = {

        //GroupName: event.GroupName != null ? event.GroupName : 'patient', 

        GroupName: event.request.userAttributes['custom:group'],

        //GroupName: event.request.clientMetadata.groupName != null ? event.request.clientMetadata.groupName : 'patient', 

        //GroupName: event.GroupName != null ? event.GroupName : 'patient',

        UserPoolId: event.userPoolId,
        Username: event.userName
    };


    // if request has userattribute group passed as value then it will add the user to the group.
    //if(event.request.clientMetadata.groupName) {
    //  if(event.request.userAttributes.group) {
    if (event.request.userAttributes['custom:group']) {

        cognitoIdentityServiceProvider.adminAddUserToGroup(params, function (err, data) {

            if (err) {
                callback(err) // error 
            }

            callback(null, event); // success
        });
    }
};
