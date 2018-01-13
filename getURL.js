var AWS = require('aws-sdk');
var s3 = new AWS.S3();

exports.handler = (event, context, callback) => {
  var params = {Bucket: 'privatecqw', Key: 'index.html', Expires: 6000};
  var url = s3.getSignedUrl('getObject', params);
  var resp = {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*"
        },
        "body": url
    };
  callback(null, resp);
};

