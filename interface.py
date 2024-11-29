import sqlite3
db = sqlite3.connect('harkkatyo.db')
cur = db.cursor()


# Starting functions

def initializeDB():
    try:
        f = open("create_commands.sql", "r")
        commandstring = ""
        for line in f.readlines():
            commandstring+=line
        cur.executescript(commandstring)
        f.close()


        f = open("insert_commands.sql", "r")
        commandstring = ""
        for line in f.readlines():
            commandstring+=line
        cur.executescript(commandstring)
        f.close()
    except sqlite3.OperationalError:
        print("Database exists, skip initialization")
    except:
        print("No SQL file to be used for initialization") 

def main():
    initializeDB()
    print("Welcome! Let's start!")
    userName = start()
    userInput = -1
    while(userInput != "0"):
        print()
        print("\nMenu options:")
        print("1. Listen to music")
        print("2: Add content")
        print("3: Delete content")
        print("4: user options")
        print(("5: Update content"))
        print("0: End program")
        userInput = input(f"What do you want to do {userName}? ")
        if userInput == "1":
            listeningMenu(userName)
        if userInput == "2":
            addingMenu(userName)
        if userInput == "3":
            deletionMenu(userName)
        if userInput == "4":
            userName = userOptionsMenu(userName)
        if userInput == "5":
            modifyContentMenu(userName)
        if userInput == "0":
            print("Ending software...")    
    db.close()    
    return

def start():
    print()
    userName = None
    while True:
        option = input("Type 1 if you want to create a new user and 2 if you want to sign in: ")
        if option == "1":
            print()
            userName= input("Username: ")
            Age = input("Age: ")
            Followers = input("Followers: ")
            t1 = "insert into User (Name,Age,Followers) values("
            t2 = "'"+userName+"',"+Age+","+Followers+");"
            q = t1 + t2
            try:
                cur.execute(q)
                db.commit()
                print(f"Welcome {userName}!")
                break
            except sqlite3.IntegrityError:
                print("The age must be more than 14.")
            except:
                print("Try again. Check that you gave the right information.")
        elif option == "2":
            userName = changeAccount(userName)
            break
    return userName

def changeAccount(orginal):
    print()
    while True:
        print("Users:")
        q1 = "SELECT Name FROM USER;"
        try:
            for row in cur.execute(q1):
                print(row[0])
        except:
            print("Something went wrong")
        userName = input("Username: ")
        try:
            q2 = "SELECT * FROM User WHERE Name ='"+userName+"';"
            cur.execute(q2)
            x = cur.fetchone()
            userID = str(x[0])
            if userID is None:
                print(f"No user named {userName}")
                return orginal
            else:
                print(f"Welcome {userName}!")
                return userName
        except:
            print("Something went wrong.")


# Menus

def listeningMenu(userName): 
    while True:
        print()
        print("Listening Menu")
        print("1: All songs")
        print("2: My listened songs")
        print("3: Songs by artist")
        print("4: Most listened songs")
        print("5: Artists on playlists")
        print("6: My playlists")
        print("0: Main menu")
        userInput = input(f"What do you want to do {userName}? ")
        if userInput == "1":
            select_all_songs()
            listenSong(userName)
        elif userInput == "2":
            songs_listened_by_user(userName)
        elif userInput == "3":
            artist_information()
            print()
            songs_by_selected_artist(userName)
        elif userInput == "4":
            most_listened_songs(userName)
        elif userInput == "5":
            artists_on_playlist()
        elif userInput == "6":
            my_playlists(userName,True)
        elif userInput == "0":
            break
        else:
            print("Try again")
    return

def addingMenu(userName):
    while True:
        print()
        print("Adding menu")
        print("1: Add song")
        print("2: Add artist")
        print("3: Create Playlist")
        print("4: Add to Playlist")
        print("0: Main menu")
        userInput = input(f"What do you want to do {userName}? ")
        if userInput == "1":
            add_song()
        elif userInput == "2":
            add_artist()
        elif userInput == "3":
            createPlaylist(userName)
        elif userInput == "4":
            addToPlayList(userName)
        elif userInput == "0":
            break
        else:
            print("Try again")
    return

def deletionMenu(userName):
    while True:
        print()
        print("Delete menu")
        print("1: Delete song")
        print("2: Delete artist")
        print("3: Delete Playlist")
        print("4: Delete from playlist")
        print("0: Main menu")
        userInput = input(f"What do you want to do {userName}? ")
        if userInput == "1":
            delete_song()
        elif userInput == "2":
            delete_Artist()
        elif userInput == "3":
            deletePlaylist(userName)
        elif userInput == "4":
            deleteFromPlaylist(userName)
        elif userInput == "0":
            break
        else:
            print("Try again")
    return

def userOptionsMenu(userName):
    while True:
        print()
        print("User options")
        print("1: Change user")
        print("2: Delete User")
        print("0: Main menu")
        userInput = input(f"What do you want to do {userName}? ")
        if userInput == "1":
            userName = changeAccount(userName)
            return userName
        elif userInput == "2":
            userName = delete_User(userName)
            return userName
        elif userInput == "0":
            break
        else:
            print("Try again")
    return userName

def modifyContentMenu(userName):
    while True:
        print()
        print("Uppdate menu")
        print("1: Modify song")
        print("2: Modify artist")
        print("0: Main menu")
        userInput = input(f"What would you like to do {userName}? ")
        if userInput == "1":
            modify_song(userName)
        elif userInput == "2":
            modify_artist(userName)
        elif userInput == "0":
            break
        else:
            print("Try again")
    return 


# Adding functions

def add_song():
    print()
    artist_information()
    print()
    print("Add a song from existing artist.")
    Artist_name = input("Artist name: ")   
    try:
        q1 = "SELECT * from Artist where Name ='"+Artist_name+"';"
        cur.execute(q1)
        x = cur.fetchone()
        Artist_id = str(x[0])
        try:
            Song_Name = input("Song name: ")
            release_year = input("Release year: ")
            t1 = "INSERT INTO Song (Name,Release_year,FK_ArtistID) values("
            t2 = f"'{Song_Name}',{release_year},{Artist_id});"
            q2 = t1+t2
            cur.execute(q2)
            db.commit()
            print("Song added succesfully!")
        except sqlite3.IntegrityError:
            try:
                q3 = f"SELECT * FROM Song WHERE Name = '{Song_Name}';"
                cur.execute(q3)
                x = cur.fetchone()
                str(x[0])
                print(f"Song called {Song_Name} already exists.")
            except:
                print(f"Check the year.") 
    except:
        print("No such artist. Add a song from existing artist.")
        
def add_artist():
    print()
    Artist_name = input("Artist name: ")
    fsr = input("First song released: ")
    nat = input("Nationality: ")
    t1 = "insert into Artist (Name,First_Song_Released,nationality) values"
    t2 = "('"+Artist_name+"',"+fsr+",'"+nat+"');"
    q = t1+t2
    try:
        cur.execute(q)
        db.commit()
        print("Artist added succesfully!")
    except sqlite3.IntegrityError: 
        try:
            q3 = f"SELECT * FROM Artist WHERE Name = '{Artist_name}';"
            cur.execute(q3)
            x = cur.fetchone()
            str(x[0])
            print(f"Artist {Artist_name} already exists.")
        except:
            print(f"Check the year.") 
    except:
        print("Something went wrong. Try again.")
    
def add_user():
    print()
    User_name = input("Username: ")
    Age = input("Age: ")
    Followers = input("Followers: ")
    t1 = "insert into User (Name,Age,Followers) values("
    t2 = "'"+User_name+"',"+Age+","+Followers+");"
    q = t1 + t2
    try:
        cur.execute(q)
        db.commit()
        print("User added succesfully!")
    except:
        print("Try again")
    return

def createPlaylist(userName):
    print()
    Name = input("What would you like to name your list? ")
    q1 = "SELECT * FROM User WHERE Name ='"+userName+"';"
    try:
        cur.execute(q1)
        x = cur.fetchone()
        Admin = str(x[0])
        if Admin is None:
            print("No such user.")
        else:
            q2 = "INSERT INTO Playlist (Name,Administrator) values("
            q3 = "'"+Name+"',"+Admin+");"
            q4 = q2 +q3
            cur.execute(q4)
            db.commit()
            print("List created succesfully!")
    except sqlite3.OperationalError:
        print("Something went wrong.")

def addToPlayList(userName):
    print()
    select_all_songs()
    print()
    songName = input(f"Which song would you like to add {userName}? ")
    print()
    b = my_playlists(userName,False)
    if b is True:
        print()
        listName = input("Which playlist would you like to add to? ")
        try:
            q1 = "SELECT * FROM Song WHERE Name ='"+songName+"';"
            q2 = "SELECT * FROM Playlist WHERE Name ='"+listName+"';"
            cur.execute(q1)
            x = cur.fetchone()
            songID = str(x[0])
            cur.execute(q2)
            y = cur.fetchone()
            listID = str(y[0])
            q3 = f"insert into add_songs values({songID},{listID})"
            cur.execute(q3)
            db.commit()
            print("Song added succesfully!")
        except:
            print("Something went wrong. Check that you gave right information.")

def listenSong(userName):
    print()
    songName = input(f"Which song would you like to listen {userName} (Give Name)? ")
    q1 = "SELECT * FROM User WHERE Name ='"+userName+"';"
    q2 = "SELECT * FROM Song WHERE Name ='"+songName+"';"
    try:
        cur.execute(q1)
        x = cur.fetchone()
        userID = str(x[0])
        cur.execute(q2)
        y = cur.fetchone()
        songID = str(y[0])
        q3 = "INSERT INTO Listeners VALUES("+songID+","+userID+");"
        cur.execute(q3)
        print(f"Playing {songName}")
        db.commit()
    except:
        print("No such song.")
    return


# Deletion functions

def delete_song():
    print()
    select_all_songs()
    Song_Name = input("Song name: ")
    q1 = f"SELECT * FROM Song WHERE Name ='{Song_Name}'"
    q2 = f"DELETE FROM Song where Name = '{Song_Name}';"
    try:
        cur.execute(q1)
        x = cur.fetchone()
        str(x[0])
        cur.execute(q2)
        db.commit()
        print("Deletion succesfull.")
    except:
        print("No such song.")

def delete_Artist():
    artist_information()
    print()
    Artist_Name = input("Artist name: ")
    q1 = "SELECT * from Artist where Name ='"+Artist_Name+"';"
    try:
        cur.execute(q1)
        x = cur.fetchone()
        Artist_id = str(x[0])
        q2 = "DELETE FROM Artist where ArtistID = "+Artist_id+";"
        cur.execute(q2)
        db.commit()
        print("Deletion succesfull.")
    except:
        print("No such artist.")
    
def delete_User(userName):
    print()
    userInput = input("Are you sure you want to delete this user? (1: Yes, 0: No) ")
    if userInput == "1":
        q = f"DELETE FROM User where Name = '{userName}';"
        try:
            cur.execute(q)
            db.commit()
            print("User deleted succesfully.")
            userName = start()
        except:
            print("Something went wrong.")
        return userName

def deletePlaylist(userName):
    print()
    b = my_playlists(userName,False)
    if b == False:
        return
    print()
    Name = input(f"What playlist would you like delete {userName}? ")
    q1 = f"SELECT * FROM Playlist WHERE Name = '{Name}';"
    q2 = f"DELETE FROM Playlist WHERE Name = '{Name}';"
    try:
        cur.execute(q1)
        x = cur.fetchone()
        str(x[0])
        cur.execute(q2)
        db.commit()
        print("Deletion succesfull!")
    except:
        print("No such playlist.")
    return

def deleteFromPlaylist(userName):
    print()
    b = my_playlists(userName,False)
    if b == False:
        return
    print()
    listName = input(f"From what Playlist would you like to delete? ") 
    print()
    b = songs_in_playlist(listName)
    if b == False:
        return
    print()
    songName = input(f"What song would you like to delete {userName}? ")
    q1 = "SELECT * FROM Song WHERE Name ='"+songName+"';"
    q2 = "SELECT * FROM Playlist WHERE Name ='"+listName+"';"
    try:
        cur.execute(q1)
        x = cur.fetchone()
        songID = str(x[0])
        cur.execute(q2)
        y = cur.fetchone()
        listID = str(y[0])
        q3 = f"DELETE FROM Add_Songs WHERE FK_SongID={songID} AND FK_PlaylistID={listID};"
        cur.execute(q3)
        db.commit()
        print("Song deleted succesfully!")
    except:
        print("Something went wrong. Check that you gave right information.")
    return


# Executing quaries

def songs_by_selected_artist(userName):
    try:
        print()
        f = open("songs_by_selected_artist.sql", "r")
        commandstring = ""
        for line in f.readlines():
            commandstring+=line
        Artist_name = input("Artist name: ")
        q1 = "SELECT * from Artist where Name ='"+Artist_name+"';"
        cur.execute(q1)
        x =cur.fetchone()
        ArtistId = str(x[0])
        commandstring = commandstring.replace("1",ArtistId)
        print("Songname")
        for row in cur.execute(commandstring):
            print(row[0])
        f.close()
        print()
        listenSong(userName)
    except:
        print("No such artist.")
    
def songs_listened_by_user(userName):
    print()
    try:
        f = open("songs_listened_by_user.sql", "r")
        commandstring = ""
        for line in f.readlines():
            commandstring+=line
        q1 = f"SELECT * FROM User WHERE Name ='{userName}';"
        cur.execute(q1)
        x =cur.fetchone()
        userId = str(x[0])
        q2 = f"SELECT * FROM Listeners WHERE FK_UserID ={userId};"
        cur.execute(q2)
        y =cur.fetchone()
        str(y[0])
        commandstring = commandstring.replace("2",userId)
        print("Songname")
        for row in cur.execute(commandstring):
            print(row[0])
        f.close()
        listenSong(userName)
    except:
        print("No listened songs.")
    return

def most_listened_songs(userName):
    print()
    try:
        q = "SELECT x,name FROM most_listened_songs;"
        print("Listeningtimes; Songname")
        for row in cur.execute(q):
            print(f"{row[0]}; {row[1]}")
        listenSong(userName)
    except:
        print("Something went wrong.")

def artist_information():
    print()
    print("Artist infromations")
    try:
        q = "SELECT * FROM Artist_information;"
        print("Name; First released song (year); Nationality")
        for row in cur.execute(q):
            print(f"{row[0]}; {row[1]}; {row[2]}")
    except:
        print("Something went wrong.")
   
def artists_on_playlist():
    print()
    q = "SELECT * FROM artists_on_playlists;"
    try:
        print("Playlist; Song; Artist")
        for row in cur.execute(q):
            print(f"{row[0]}; {row[1]}; {row[2]}")
        listen_to_playlist()
    except:
        print("Something went wrong.")

def my_playlists(userName,b):
    print()
    try:
        f = open("all_playlists.sql", "r")
        commandstring = ""
        for line in f.readlines():
            commandstring+=line
        q1 = f"SELECT * from User where Name ='{userName}';"
        cur.execute(q1)
        x =cur.fetchone()
        admin = str(x[0])
        commandstring = commandstring.replace("2",admin)
        print("My playlists")
        f.close()
        try:
            cur.execute(commandstring)
            test = cur.fetchone()
            str(test[0])
            for row in cur.execute(commandstring):
                print(row[0]) 
            if b is True:
                listen_to_playlist()
        except:
            print("You have no playlists.")
            return False
    except:
        print("Something went wrong.")
        return False
    return True

def select_all_songs():
    print()
    try:
        f = open("select_all_songs.sql", "r")
        commandstring = ""
        for line in f.readlines():
            commandstring+=line
        print("Songname; Release year; Artist")
        for row in cur.execute(commandstring):
            print(f"{row[0]}; {row[1]}; {row[2]}")
        print()
    except:
        print("Something went wrong.")
    return
  
def listen_to_playlist():
    print()
    Name = input("What playlist would you like to listen (Name)? ")
    try:
        q = f"SELECT * FROM Playlist WHERE Name = '{Name}';"
        cur.execute(q)
        x = cur.fetchone()
        listID= str(x[0])
        print(f"Playing {Name}")
    except:
        print("No such playlist.")

def songs_in_playlist(Name):
    print()
    try:
        f = open("songs_in_playlist.sql", "r")
        commandstring = ""
        for line in f.readlines():
            commandstring+=line
        q1 = "SELECT * from Playlist WHERE Name ='"+Name+"';"
        f.close()
        cur.execute(q1)
        x =cur.fetchone()
        listId = str(x[0])
        commandstring = commandstring.replace("1",listId)
        cur.execute(commandstring)
        x = cur.fetchone()
        try:
            str(x[0])
        except:
            print("The list is empty.")
            return False
        print(f"Songs in the Playlist {Name}")
        for row in cur.execute(commandstring):
            print(row[0])
        return True
    except:
        print("No such list.")
        return False



# Modification functions


def modify_song(userName):
    while True:
        print()
        print("Uppdate song information")
        print("1: Change songname")
        print("2: Change release year")
        print("0: Uppdate menu")
        userInput = input(f"What would you like to do {userName}? ")
        if userInput == "1":
            change_songname()
        elif userInput == "2":
            change_release_year()
        elif userInput == "0":
            break
        else:
            print("Try again")
    return 

def modify_artist(userName):
    while True:
        print()
        print("Uppdate artist information")
        print("1: Change name")
        print("2: Change first released song (year)")
        print("3: Change nationality")
        print("0: Update menu")
        userInput = input(f"What would you like to do {userName}? ")
        if userInput == "1":
            change_artistname()
        elif userInput == "2":
            change_first_song_released()
        elif userInput == "3":
            change_nationality()
        elif userInput == "0":
            return
        else:
            print("Try again")
    return 

def change_songname():
    print()
    select_all_songs()
    Song_Name = input("What song would yoi like to modify? ")
    try:
        q1 = f"SELECT * FROM Song WHERE Name = '{Song_Name}'"
        cur.execute(q1)
        x = cur.fetchone()
        str(x[0])
        try:
            newName = input("New name: ")
            q2 = f"UPDATE Song SET Name = '{newName}' WHERE Name = '{Song_Name}';"
            cur.execute(q2)
            db.commit()
            print("Update succesfull!")
        except:
            print("Something went wrong. Check you gave right values.")
    except:
        print("No such song.")

def change_release_year():
    print()
    select_all_songs()
    Song_Name = input("What song would you like to modify? ")
    try:
        q1 = f"SELECT * FROM Song WHERE Name = '{Song_Name}';"
        cur.execute(q1)
        x = cur.fetchone()
        str(x[0])
        try:
            newReleaseyear = input("What is the new release year? ")
            q1 = f"UPDATE Song SET Release_year = {newReleaseyear} WHERE Name = '{Song_Name}';"
            cur.execute(q1)
            db.commit()
            print("Update succesfull!")
        except:
            print("Something went wrong. Check that you gave right information.")
    except:
        print("No such song.")
    return
    
def change_artistname():
    print()
    artist_information()
    print()
    Name = input("What artist name would you like to change? ")
    try:
        q1 = f"SELECT * FROM Artist WHERE Name = '{Name}'"
        cur.execute(q1)
        x = cur.fetchone()
        str(x[0])
        try:
            newName = input("New artistname: ")
            q = f"UPDATE Artist SET Name='{newName}' WHERE Name = '{Name}'"
            cur.execute(q)
            db.commit()
            print("Update succesfull!")
        except:
            print("Something went wrong.")
    except:
        print("No such artist.")

def change_first_song_released():
    print()
    artist_information()
    print()
    Name = input("From which artist would you like to change the year? ")
    try:
        q1 = f"SELECT * FROM Artist WHERE Name = '{Name}'"
        cur.execute(q1)
        x = cur.fetchone()
        str(x[0])
        try:
            newR = input("New year when first song was released: ")
            q2 = f"UPDATE Artist SET First_Song_Released ={newR} WHERE Name = '{Name}'"
            cur.execute(q2)
            db.commit()
            print("Update succesfull!")
        except:
            print("Something went wrong. Check you gave the right informations.")
    except:
        print("No such artist.")
    return

def change_nationality():
    print()
    artist_information()
    print()
    Name = input("What artist name would you like to change? ")
    try:
        q1 = f"SELECT * FROM Artist WHERE Name = '{Name}'"
        cur.execute(q1)
        x = cur.fetchone()
        str(x[0])
        try:
            newNat = input("New nationality: ")
            q = f"UPDATE Artist SET nationality ='{newNat}' WHERE Name = '{Name}'"
            cur.execute(q)
            db.commit()
            print("Update succesfull!")
        except:
            print("Something went wrong. Check you gave the right informations.")
    except:
        print("No such artist.")
    return


main()