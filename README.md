# simple_hook
my simple and ugly ci/cd with github webhooks

in github settings -> webhooks 

add Payload URL to your server: `http://url:5000/webhook`

choose content type: `application/json`

add your secret key

add .env in project folder like [example](example.env)

run app
