<a href="https://docs.aws.amazon.com/lambda/latest/dg/with-s3-example.html">Follow this guide</a>
<h4>Reference this as you work through the guide</h4>
Create 2 S3 buckets instead of 1.
Add <code>           "Action": [
              "s3:*",
              "s3-object-lambda:*"
            ]</code> in place of the actions the guide uses
On the lambda screen, go Configuration -> Triggers -> add a trigger for each
