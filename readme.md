As the title says, we're going to talk about Netflix, Oscars, and Slop.

*This is a written out version (and technical version) of the presentation that's posted above. If you want a deep dive into what I did to get the data I concluded with and read about the connections being made as the project was being done, continue. If not, the the presentation tries to give what is only needed to understand the conclusions!*

## Backstory
A couple of months ago I read an article talking about how Netflix was pivoting from doing award winning movies to content that requires less attention to follow. This concept has become something called "Ambient TV" which is a show or movie that doesn't really require the viewers attention to follow what's happening, which means you can do something else while playing the content. The biggest piece of ambient TV was a show called "Emily in Paris", which is what was brought up every time the topic of "ambient TV" and "Netflix" came up.

The reason this became such a topic for Netflix was because at the time of those articles coming out, COVID 19 pushed everyone to stay inside, which pushed people into watching things on streaming platforms like Netflix or YouTube or Hulu, etc. This content became the answer to the question "what do I watch". Because if you can just put something like "Emily in Paris" on and do other things, you will do that instead of searching for something to watch. It's the same concept as putting on a YouTube video while you're eating or doing work.

Now that it's been a couple of years since the concept of Ambient TV was on Netflix's radar, how has the content output of Netflix changed in 4 years. Well that's what we're here to answer.

**Questions: Did Netflix's movie output grow in the last few years? Have the rating averages gone lower year over year for Netflix Original Movies? Has Netflix even made a movie in the last 4 years that won an Oscar or Emmy? What genre has had an increase in movies made over the last few years?**

## Dataset Hunt
Alright now time to look for a data set (or data sets) that we will use for this project.
The main thing I want is a database that displays the names of shows or movies on Netflix (made specifically by Netflix) and a review database that gives me their score. The year of release would also be nice. I may have to do some SQL magic to join them together and export it that way.

Oh wait, there's an imdb data set of Netflix original movies. Hmm...I would still like to do the SQL thing as practice.
Ok so new plan: I do analysis on this data set, and then see if there is anything new we can take from the SQL hacked dataset that will be made.
Or what I can potentially do is use this data set for movies only, and then use the tv shows on the big data set as the challenge. Yeah, I'll do that.

## Process of Cleaning
I'm going to use excel for this portion because there are only 585 inputs of data, which is perfectly manageable by excel.
So the data provides a sort of code, the title of the movie, the imdb rating, the runtime of the movie, the year it was made, the genre, how many votes it got on imdb (which I assume is how many people rated the movie), the exact release date, and the director.

So immediately from here, I want to get rid of a few things. I want to get rid of the created and modified dates, because that just doesn't give us anything. I want to get rid of the URL, but I want to check if I can do something like allow the user to open up the individual imdb page when clicking on it, or something. The Title type is gone because they're all movies. I also want to get rid of release date and director, because we only want the year and director doesn't really matter to us atm. I also want to get rid of the original title because we just want to see what is seen as a US Netflix user.

Now here is the hard part of this, the description. There is a description column in this data set and it's strange. It starts out showing "English/Twi" then "English/Korean", then "Hindi". This made me think "oh it specifies the language it was specifically made for, right?" Looking a little further we will start getting dates and then language followed by a date. All of it is really weird but I can take some liberties and then see how the data tracks later on. What I'm going to do is assume every blank (or every cell that specifies a date only) is made by an American for an American audience.
That being said, we have to clean this up now. I replaced every "Hindi - *date*" with just "Hindi", same with other languages, and replaced every blank cell in the description column with "English (US)"

There is now an interesting problem I have to solve. I want to use the genres column and see if there is an uptick in a certain genre. The issue is that the genres column has multiple genres in the same cell, divided by a column. Now I can just go find all the unique genres, make a set of columns for it and say true or false for each genre for each movie, but that would be too much work. So let's see if we can automate it!

## Process of Cleaning Part B: Genres with Python
I'm going to be using python for this because it just seems the most straight forward to use. I'm going to include snippets of code I feel are necessary but you can find the commented out code in the github repo so I don't get too in the weeds.

After getting access to the column I wanted, I looped through all of them to find unique genres.
From there, I wanted to create new columns in the data sheet named 'is_*genre*' so it can easily be filled with True or False values.

Now for the most interesting part: filling up the data. So first, we need to go through each row in the data. We first verify if the row has a value in the 'Genres' column is a string (so we can do things to the string without python freaking out). We then get the genres in the row and split them by comma, same as before. Then we loop through each genre in the unique genres, and check if the genre we have is in the genres we have in the row. If yes, that cell will hold the value of True. If not, False.

```Python
for index, row in data.iterrows():

    if isinstance(row['Genres'], str):

        genres_in_row = [genre.strip() for genre in row['Genres'].split(',')]

        for genre in unique_genres:

            if genre in genres_in_row:

                data.at[index, f'is_{genre}'] = 'True'

            else:

                data.at[index, f'is_{genre}'] = 'False'
```

Finally, we save the excel file and check.

Now we have new columns added that tells us if a movie is a drama, a war, an action, adventure, etc. Now this is data we can mess around with and see if something is happening.

## Final Analysis
Aright now that we have all the python finished, we can get to the excel and see what the data says.

After making some pivot tables and seeing what they can imply, it's very interesting.

### Question 1: Did Netflix's movie output grow in the last few years.
Quite the opposite actually. It's gone down a pretty significant amount. Almost close to the output of Netflix in 2016. Granted, the data is currently until June of this year, but even if we only take 2023 as the last one, it's still lower than the output from 2018.

This could imply a difference in priority to more TV shows rather than actual movies. Shows like "Is it Cake" are extremely cheap to make relative to movies, so that would be my current guess.

### Question 2: Have the rating averages gone down?
No, HOWEVER there is a clear indicator that the ratings are around the same level because so many less people have seen them. 
If we take the sum of how many ratings were given to every movie within the year, we can see that in 2022 and 2023, the sum has been going down from 2021. Now if we take the current year, it's even lower than 2023. This can be a considerable amount of factors. Maybe people aren't consuming movies as much. Maybe people aren't using IMDB as much and prefer something like Rotten Tomato or letterboxd. It could also mean that the movies Netflix is currently releasing doesn't have the critical acclaim power to push more critics and users to watch it. There isn't something like "The Irishman" which was released in 2019, and was also the year that had the most number of reviews from IMDB users.

### Question 3: Has Netflix even done a movie that won an award?
They have made movies that have gotten nominated, but it wasn't some spectacle that Netflix was clearly super proud of and wanted to tell everyone about. The last one was "Maestro" in 2023. It did win some awards but not at the big award shows like the emmys or the oscars.

### Question 4: Has there been a change in movies based on Genres?
No, actually. Despite there being less movies and less critically acclaimed movies, the spread of genres is pretty similar to every other year. The top genres being Drama, Romance, Thriller, and Comedy. It's been consistent just with less movies year over year.
One could interpret this as Netflix actually making less movies but their spread is the same because they know that is what works for them, even if the quality and critical acclaim is lower.