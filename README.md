<!DOCTYPE html>
<html>
    <body>
        <h2>Naitam's Spotify Web Page</h2>
        <img src="https://storage.googleapis.com/pr-newsroom-wp/1/2020/03/Header.png"/>
    </body>
</html>

### Summary
For this project I used the AWS Cloud9 IDE to set up and edit all of my code. This IDE allowed me to preview and use the browser extention to view the progress of my application and make the necessary changes. It also allowed me to create my local repository and link it with the remote Github repository. The main backend portion of this app was coded in Python using dependencies such as Flask and requests. The main source of my data is attained using the spotify top-tracks API. I used GET requests to query the data that I needed to display on the website. I used a similar method using the Genius API to get the lyrics of each song. The website was created using HTML/CSS and was deployed using Heroku.

### Technical issues faced
+ Being able to understand the spotify API and be able to gather the data that I wanted was a big initial struggle and many of my initial queries attempts failed in this process. I found a youtube tutorial, which I followed and then I quickly understood how the whole authorization and query process works for spotify.
+ I had problems with the cloud9 IDE, since it was my first time using this environment, I was unable to figure out a solution to the website previews. There were many times where I'd change something in the code, but the website would not update the changes I made, and it was hard the judge if it was my code or the IDE. Eventually, many students came across this issue and I started using the ctrl+shift+R method to refresh the website everytime I changed somthing, and this gave me an instant feedback and I was able to debug/fix my code efficiently.
+ I had a major bottleneck because I began the project using lists to store the json formated data. so when it came to using the Genius API the data that I wanted to use was just not cooperative and I had a lot of formating issues. After many troubleshooting attempts later, I decided to use the flask fucntion to dynamically fetch the data ever reload for a single artist instead of getting all the data for all artists in at once. This way the data is stored in variables and not lists, and it's much faster and easier to use and pass on to the html file.

### Known problem
+ When the song is searched in the Genius API, it doesn't always gaurantee the correct verion or song because I take in the url of the first result. The song title I have uss from the spotify api can tend to have a different from the genius title which can result in an incorrect search.
+ On the home page the preview url player is always showing, so it takes away from the asthetics of the webpage
+ Same problem with the header "Naitam's Spotify Project" on the home page. I tried adding JS fucntion using it on the button with onclick but it didn't seem to clear out even with that attempt.

### What would you do to improve your project in the future? 
+ I would like to have a more information about the artist.
+ I'd like to fix the header and the preview url player issues to make the app seem cleaner
+ I'd also like to add maybe music video's so that there's a visual for the user.