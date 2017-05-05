# This file contains our code for Neo4j data Analysis.
import py2neo
from py2neo import Graph,Node,Relationship

py2neo.authenticate("localhost:7474","neo4j","neo4j1")
graph = Graph("http://localhost:7474/db/data/")

# Once we have received the cleaned data we have to import the data in Neo4j using py2neo.
# We have to create nodes for users and airlines.
# In this we have to take the file as the node name and then assign every column value to the property of the nodes.
graph.run("""LOAD CSV WITH HEADERS FROM 'file:///userData.csv' AS User
            Create (user1:User{userName:User.authorname,airName:User.airlinename,
            recommended:User.recommended,revContent:User.reviewcontent,rat_overall:User.ratingoverall,
            positiveWordCount:User.poswdcnt,negativeWordCount:User.negwdcnt,sentiment:User.lsentiment})""")
# Query for the Airline node
graph.run("""LOAD CSV WITH HEADERS FROM 'file:///flightData.csv' AS Airline
             create(air1:Airline{airlinename:Airline._id,username:Airline.aname,
             airrating:Airline.arating,stdv:Airline.stdr,airinflight:Airline.arinflight,
             aircabstf:Airline.arcstf,airseat:Airline.arstcmft})""")
# Creating the relationship between user and Airline. Both the nodes have the property as airline name
# Match both the nodes on the basis of these properties and make a relationship.
graph.run("""Match(u:User),(a:Airline)where u.airName =a.airlinename Create (u)-[:to]->(a)""")
# Create a relation between every user to every user. As the users are related with each other as well.
graph.run("""match (a:User), (b:User) where a.userName = b.userName Create (a)-[:user_linking]->(b)""")
# Now we have to delete the self relationship.
graph.run("""match(a:User)-[r:user_linking]->(a:User) delete r""")

# Query 2.2 This query checks which airlines the user has rated. We are checking only for those users who have rated atleast 2 airlines.
# We are taking the maximum rating the user has provided to a particular airline. Making a collection of airline name and the maximum
# rating. This way we can what is the maximum rating a common user has given to all the competitors.     
results = graph.run("""match (a:Airline)<-[:to]-(u:User{recommended:"1"})
                    with distinct a.airlinename as name, max(u.rat_overall) as ratMax, u.userName as user
                    with user, collect([name,ratMax]) as Competition
                    where size(Competition)>1
                    return user, Competition
                    limit 100""")
for result in results:
    print (result)

# Query 2.4 In this query we are checking for an airlines and all the user that have provided ratings for it. This gives us the common airlines for the users
# and then we check all the ratings that all the users have given to common airlines. We are also incorporating the rating and sentiment these users have for
# Other airlines as well. 
results = graph.run("""match (a:Airline)<-[:to]-(u:User)
                    with a,u
                    match (u)-[:user_linking]->(u1:User)
                    with a,u,u1
                    match (u1)-[:to]->(b:Airline)
                    where a.airlinename <> b.airlinename
                    return a.airlinename as Airline,a.airrating as AirlineRating,
                    collect(distinct [u.userName,u.rat_overall]) as UserReviewed,
                     collect(distinct[u1.userName,b.airlinename,u1.sentiment,u1.rat_overall]) as CompetitorRatingAndSentiment
                     limit 100""")
for result in results:
    print(result)
