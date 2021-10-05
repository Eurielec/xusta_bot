# XUSTA BOT

Eurielec's Telegram bot.


## Features

* **/getImage**: Sends an image looking at the door.
* **/getVideo**: Sends a gif looking at the door.
* **/getSalseo**: Sends a gif with panning from the door to the sofa and back.
* **/getNevera**: Sends a gif with panning from the door to the microwave and back.
* **/test**: Sends "Hi!" to test if the bot is up.
* **/getId**: Sends the chat.id of the current chat (group's id if called in a group, your's if called privately).
* **/getTurn**: Sends who has to take the trash out.
* **/turnDone**: Marks current turn as done and sends a picture of the trash so people can check.
* **/turnUndo**: Marks current turn as not done (in case the picture sent by turnDone wasn't the expected result).  
* **others**: Undocumented or for admins only (you can read them in the code, but you mainly won't have access to those).

> Every time an access to the camera occurs, the server will notice people by beeping (depends on if the camera will move or not)

### New features

Do you want to contribute?

#### I have an idea and I know how to code

Cool! You know the steps:
1. Clone the repository.
2. Create a new branch to make your changes and implement your code.
3. Test your code in your server, or take down the master deployment temporary (remember to restart when finished!).
4. Commit your changes and make a merge request!
5. Wait for approval and deployment. You are all set.

#### I have an idea but don't know how to code
Please feel free to open an issue if you have an idea (even if you don't know how to code!)


## Deployment instructions

1.  Read the `docker-compose.yml` and create `.env` according to your needs (f.i HOST, CAM_PASSWORD, GODMODE).
2.  Build and deploy the image with `docker-compose up -d --build`

> We need --privileged to access the piezzo buzzer for camera access beeps.


## Considerations

1.  The server and the camera need to be in the same network, otherwise modify the camera module accordingly.
2.  The camera module has been designed specifically for one WANSCAM model. Please modify it if the camera gets changed.
3.  The batallon module has been designed specifically to operate on a spreadsheet. Please modify it if sheet's name changes.
    > Make sure you got `secreto.json` file

4.  We are using Traefik as reverse proxy. If you want to change it, please do so.


## Troubleshooting

*   The bot doesn't answer at all?
    1.  Check the port mapping (container and nginx).
    2.  Make sure HTTPS is used from NGINX/Traefik to the outside world. The container is an HTTP webhook.
    3.  None of the above? Use tshark inside and outside the container and see if Telegram is reaching your server.

*   Others
  Please contact **@d3vv3** on Telegram for help.


## Known bugs

*   There is no output logs (reason unknown yet).
*   Found a bug? Feel free to open an issue!
